// Automatic layouts: turn {nodes, edges, ...} into positioned Excalidraw elements.
//
//   flow      — flowcharts, trees, mind maps, state machines, ER diagrams, free architecture graphs (dagre)
//   layers    — layered architecture (presentation / app / data …), one horizontal band per layer
//   swimlane  — cross-functional process: one horizontal lane per actor/system, steps ordered left → right
//   sequence  — participants on top, lifelines, time-ordered messages
//   timeline  — dated items along a horizontal axis
//
// Every renderer receives ctx = { S, P(x,y)→abs, fid, style(name, extra), ids } and returns the bbox it used.
'use strict';
const dagre = require('@dagrejs/dagre');
const { Scene, measure } = require('./lib');

const nodeSize = (n, fs, st) => {
  const s = Scene.autoSize(n.text ?? '', n.fontSize || fs, n.shape || st.shape || 'rectangle');
  return { w: n.w || Math.max(s.w, n.minW || 140), h: n.h || Math.max(s.h, 70) };
};

function makeNode(ctx, n, x, y, w, h, fs) {
  const st = ctx.style(n.style || 'process', { fontSize: n.fontSize || fs, shape: n.shape, dashed: n.dashed, align: n.align });
  st.frameId = ctx.fid;
  const el = ctx.S.box(n.text ?? '', x, y, w, h, st);
  if (n.id) ctx.ids[n.id] = el;
  return el;
}

function makeEdge(ctx, e, extra = {}) {
  const a = ctx.ids[e.from], b = ctx.ids[e.to];
  if (!a || !b) throw new Error(`edge ${e.from} → ${e.to}: unknown node`);
  const st = e.style ? ctx.style(e.style) : {};
  return ctx.S.arrow(a, b, {
    label: e.label, dashed: e.dashed, color: e.color || (e.style ? st.stroke : undefined), fontSize: e.fontSize || 14, frameId: ctx.fid,
    route: e.route || extra.route, via: extra.via, fromPoint: extra.fromPoint, toPoint: extra.toPoint,
    fromSide: e.fromSide || extra.fromSide, toSide: e.toSide || extra.toSide,
    startArrowhead: e.both ? 'arrow' : undefined, endArrowhead: e.arrowhead === false ? null : undefined,
  });
}

function groupBox(ctx, label, b, styleName = 'group', pad = 24, labelH = 30) {
  const st = ctx.style(styleName); st.frameId = ctx.fid;
  const r = ctx.S.box(null, b.x - pad, b.y - pad - labelH, b.w + 2 * pad, b.h + 2 * pad + labelH, st);
  if (label) ctx.S.text(label, r.x + 12, r.y + 8, { fontSize: 18, color: st.stroke === '#ced4da' ? '#495057' : st.stroke, frameId: ctx.fid });
  return r;
}

// ------------------------------------------------------------------ flow (dagre)
function flow(ctx, d) {
  const fs = d.fontSize || 20;
  const g = new dagre.graphlib.Graph({ compound: true, multigraph: true });
  g.setGraph({ rankdir: d.direction || 'TB', nodesep: d.nodesep ?? 60, ranksep: d.ranksep ?? 90, edgesep: 20, marginx: 0, marginy: 0 });
  g.setDefaultEdgeLabel(() => ({}));
  const sizes = {};
  for (const n of d.nodes) { const st = ctx.style(n.style || 'process'); sizes[n.id] = nodeSize(n, fs, st); g.setNode(n.id, { width: sizes[n.id].w, height: sizes[n.id].h }); }
  for (const gr of d.groups || []) {
    g.setNode('__g_' + gr.id, { paddingTop: 40 });
    for (const id of gr.nodes || d.nodes.filter((n) => n.group === gr.id).map((n) => n.id)) g.setParent(id, '__g_' + gr.id);
  }
  (d.edges || []).forEach((e, i) => {
    const lm = e.label ? measure(e.label, e.fontSize || 14) : { w: 0, h: 0 };
    g.setEdge(e.from, e.to, { width: lm.w + 10, height: lm.h + 6, labelpos: 'c', minlen: e.minlen || 1 }, 'e' + i);
  });
  dagre.layout(g);
  const [ox, oy] = ctx.P(d.x, d.y);
  // groups first so they sit underneath
  for (const gr of d.groups || []) {
    const c = g.node('__g_' + gr.id);
    groupBox(ctx, gr.label, { x: ox + c.x - c.width / 2 + 10, y: oy + c.y - c.height / 2 + 14, w: c.width - 20, h: c.height - 28 }, gr.style || 'group', 12, 24);
  }
  for (const n of d.nodes) {
    const v = g.node(n.id);
    makeNode(ctx, n, ox + v.x - v.width / 2, oy + v.y - v.height / 2, v.width, v.height, fs);
  }
  const route = d.edgeRoute || 'curved'; // curved (dagre path) | straight | orthogonal
  (d.edges || []).forEach((e, i) => {
    if (route === 'curved' && !e.route) {
      const pts = g.edge(e.from, e.to, 'e' + i).points.map((p) => [ox + p.x, oy + p.y]);
      makeEdge(ctx, e, { fromPoint: pts[0], toPoint: pts[pts.length - 1], via: pts.slice(1, -1) });
    } else makeEdge(ctx, e, { route: e.route || (route === 'orthogonal' ? 'orthogonal' : undefined) });
  });
  const G = g.graph();
  return { x: ox, y: oy, w: G.width, h: G.height };
}

// ------------------------------------------------------------------ layers (layered architecture)
function layers(ctx, d) {
  const fs = d.fontSize || 20;
  const gap = d.nodesep ?? 50, labelW = d.labelWidth ?? 180, pad = 30, layerGap = d.layerGap ?? 50;
  const byId = Object.fromEntries(d.nodes.map((n) => [n.id, n]));
  // order nodes inside each layer by the average position of their neighbours in the layer above
  // (barycenter heuristic) so edges cross less; d.keepOrder: true disables it
  const order = d.layers.map((L) => L.nodes || d.nodes.filter((n) => n.layer === L.id).map((n) => n.id));
  if (!d.keepOrder) {
    for (let i = 1; i < order.length; i++) {
      const prev = order[i - 1];
      const key = (id) => {
        const nb = (d.edges || []).flatMap((e) => (e.from === id ? [e.to] : e.to === id ? [e.from] : [])).map((x) => prev.indexOf(x)).filter((k) => k >= 0);
        return nb.length ? nb.reduce((s, k) => s + k, 0) / nb.length : Infinity;
      };
      const orig = order[i].slice();
      order[i] = orig.slice().sort((a, b) => key(a) - key(b) || orig.indexOf(a) - orig.indexOf(b));
    }
  }
  const layerOf = {};
  order.forEach((ids, i) => ids.forEach((id) => (layerOf[id] = i)));
  const rows = d.layers.map((L, li) => {
    const ns = order[li].map((id) => byId[id]);
    const sz = ns.map((n) => nodeSize(n, fs, ctx.style(n.style || 'process')));
    return { L, ns, sz, w: sz.reduce((s, z) => s + z.w, 0) + gap * Math.max(0, ns.length - 1), h: Math.max(...sz.map((z) => z.h), 60) };
  });
  const innerW = Math.max(...rows.map((r) => r.w));
  const [ox, oy] = ctx.P(d.x, d.y);
  let y = oy;
  const bandW = labelW + innerW + 2 * pad;
  const bandBottom = [];
  for (const r of rows) {
    const bh = r.h + 2 * pad;
    bandBottom.push(y + bh);
    const st = ctx.style(r.L.style || 'layer'); st.frameId = ctx.fid; st.square = false;
    ctx.S.box(null, ox, y, bandW, bh, st);
    ctx.S.text(r.L.label || '', ox + 16, y + bh / 2 - measure(r.L.label || '', 18).h / 2, { fontSize: 18, color: '#495057', frameId: ctx.fid });
    let x = ox + labelW + pad + (innerW - r.w) / 2;
    r.ns.forEach((n, i) => { makeNode(ctx, n, x, y + pad + (r.h - r.sz[i].h) / 2, r.sz[i].w, r.sz[i].h, fs); x += r.sz[i].w + gap; });
    y += bh + layerGap;
  }
  // decide which side each edge leaves/enters, then spread several edges on one side evenly
  const plan = (d.edges || []).map((e) => {
    const lf = layerOf[e.from], lt = layerOf[e.to];
    if (lf == null || lt == null) return { e, free: true };
    if (lf === lt) {
      const far = Math.abs(order[lf].indexOf(e.from) - order[lf].indexOf(e.to)) > 1;
      if (far) return { e, fs: 'bottom', ts: 'bottom', around: true };
      const right = order[lf].indexOf(e.to) > order[lf].indexOf(e.from);
      return { e, fs: right ? 'right' : 'left', ts: right ? 'left' : 'right' };
    }
    return lf < lt ? { e, fs: 'bottom', ts: 'top' } : { e, fs: 'top', ts: 'bottom' };
  });
  const ports = {};
  const addPort = (id, side, p, end) => (ports[id + ':' + side] = ports[id + ':' + side] || []).push({ p, end });
  plan.forEach((p) => { if (!p.free) { addPort(p.e.from, p.fs, p, 'from'); addPort(p.e.to, p.ts, p, 'to'); } });
  const pt = (el, side, off) => side === 'bottom' ? [el.x + el.width / 2 + off, el.y + el.height + 5] : side === 'top' ? [el.x + el.width / 2 + off, el.y - 5] : side === 'left' ? [el.x - 5, el.y + el.height / 2 + off] : [el.x + el.width + 5, el.y + el.height / 2 + off];
  for (const [key, list] of Object.entries(ports)) {
    const [id, side] = key.split(':');
    const el = ctx.ids[id];
    const horiz = side === 'top' || side === 'bottom';
    const span = (horiz ? el.width : el.height) * 0.7;
    const other = (it) => { const o = ctx.ids[it.end === 'from' ? it.p.e.to : it.p.e.from]; return horiz ? o.x + o.width / 2 : o.y + o.height / 2; };
    list.sort((u, v) => other(u) - other(v));
    list.forEach((it, i) => { const off = list.length === 1 ? 0 : -span / 2 + (span * i) / (list.length - 1); it.p[it.end + 'Pt'] = pt(el, side, off); });
  }
  for (const p of plan) {
    if (p.free) { makeEdge(ctx, p.e); continue; }
    if (p.around) {
      const ya = bandBottom[layerOf[p.e.from]] - 12;
      makeEdge(ctx, p.e, { fromPoint: p.fromPt, toPoint: p.toPt, via: [[p.fromPt[0], ya], [p.toPt[0], ya]], route: 'orthogonal' });
    } else makeEdge(ctx, p.e, { fromPoint: p.fromPt, toPoint: p.toPt, route: d.edgeRoute === 'orthogonal' ? 'orthogonal' : undefined, fromSide: p.fs, toSide: p.ts });
  }
  return { x: ox, y: oy, w: bandW, h: y - layerGap - oy };
}

// ------------------------------------------------------------------ swimlane
function swimlane(ctx, d) {
  const fs = d.fontSize || 20;
  // column order from a left→right dagre ranking of the whole graph
  const g = new dagre.graphlib.Graph({ multigraph: true });
  g.setGraph({ rankdir: 'LR' }); g.setDefaultEdgeLabel(() => ({}));
  const sizes = {};
  for (const n of d.nodes) { sizes[n.id] = nodeSize(n, fs, ctx.style(n.style || 'process')); g.setNode(n.id, { width: sizes[n.id].w, height: sizes[n.id].h }); }
  (d.edges || []).forEach((e, i) => g.setEdge(e.from, e.to, {}, 'e' + i));
  dagre.layout(g);
  const ranks = [...new Set(d.nodes.map((n) => (n.col != null ? n.col * 1000 : g.node(n.id).rank)))].sort((a, b) => a - b);
  const colOf = (n) => ranks.indexOf(n.col != null ? n.col * 1000 : g.node(n.id).rank);
  const colW = Math.max(...d.nodes.map((n) => sizes[n.id].w)) + (d.nodesep ?? 70);
  const labelW = d.labelWidth ?? 170, pad = 24;
  const [ox, oy] = ctx.P(d.x, d.y);
  const nCols = ranks.length;
  const width = labelW + nCols * colW + pad;
  let y = oy;
  for (const lane of d.lanes) {
    const ns = d.nodes.filter((n) => n.lane === lane.id);
    // stack nodes that share a column inside the lane
    const stacks = {};
    ns.forEach((n) => { const c = colOf(n); (stacks[c] = stacks[c] || []).push(n); });
    const laneH = Math.max(100, ...Object.values(stacks).map((s) => s.reduce((t, n) => t + sizes[n.id].h, 0) + (s.length + 1) * pad));
    const st = ctx.style(lane.style || 'lane'); st.frameId = ctx.fid; st.square = true;
    ctx.S.box(null, ox, y, width, laneH, st);
    ctx.S.text(lane.label || lane.id, ox + 14, y + laneH / 2 - measure(lane.label || lane.id, 18).h / 2, { fontSize: 18, color: '#495057', frameId: ctx.fid });
    ctx.S.line([[ox + labelW - 10, y], [ox + labelW - 10, y + laneH]], { color: '#ced4da', frameId: ctx.fid });
    for (const [c, s] of Object.entries(stacks)) {
      const total = s.reduce((t, n) => t + sizes[n.id].h, 0) + (s.length - 1) * pad;
      let ny = y + (laneH - total) / 2;
      for (const n of s) {
        const z = sizes[n.id];
        makeNode(ctx, n, ox + labelW + Number(c) * colW + (colW - z.w) / 2, ny, z.w, z.h, fs);
        ny += z.h + pad;
      }
    }
    y += laneH;
  }
  for (const e of d.edges || []) makeEdge(ctx, e, { route: d.edgeRoute || 'orthogonal' });
  return { x: ox, y: oy, w: width, h: y - oy };
}

// ------------------------------------------------------------------ sequence
function sequence(ctx, d) {
  const fs = d.fontSize || 18;
  const ps = d.participants;
  const sz = ps.map((p) => nodeSize({ ...p, text: p.text ?? p.id }, fs, ctx.style(p.style || 'actor')));
  const colW = Math.max(d.colWidth || 0, ...sz.map((z) => z.w + 80), 240);
  const step = d.step || 64;
  const [ox, oy] = ctx.P(d.x, d.y);
  const headH = Math.max(...sz.map((z) => z.h));
  const cx = {};
  ps.forEach((p, i) => {
    const x = ox + i * colW + (colW - sz[i].w) / 2;
    makeNode(ctx, { ...p, text: p.text ?? p.id }, x, oy + (headH - sz[i].h) / 2, sz[i].w, sz[i].h, fs);
    cx[p.id] = ox + i * colW + colW / 2;
  });
  let y = oy + headH + 50;
  const msgs = d.messages || [];
  for (const m of msgs) {
    if (m.note) {
      const over = [].concat(m.over || m.from || ps[0].id);
      const xs = over.map((id) => cx[id]);
      const x0 = Math.min(...xs) - colW / 2 + 20, x1 = Math.max(...xs) + colW / 2 - 20;
      const t = measure(m.note, 16);
      const st = ctx.style(m.style || 'note', { fontSize: 16, align: 'center' }); st.frameId = ctx.fid;
      ctx.S.box(m.note, x0, y - 10, x1 - x0, t.h + 24, st);
      y += t.h + 24 + 20;
      continue;
    }
    if (m.divider) {
      ctx.S.line([[ox, y], [ox + ps.length * colW, y]], { color: '#adb5bd', dashed: true, frameId: ctx.fid });
      ctx.S.text(m.divider, ox + 8, y - 26, { fontSize: 16, color: '#495057', frameId: ctx.fid });
      y += step * 0.7;
      continue;
    }
    const x1 = cx[m.from], x2 = cx[m.to];
    if (x1 == null || x2 == null) throw new Error(`sequence message ${m.from} → ${m.to}: unknown participant`);
    const lab = m.text ? (m.n != null ? `${m.n}. ` : '') + m.text : undefined;
    const lh = lab ? measure(lab, 14).h : 0;
    y += Math.max(0, lh - 18);
    if (x1 === x2) {
      // self-call: small loop to the right of the lifeline; label as free text beside the loop (a bound
      // label would sit on the loop's midpoint and hide it)
      ctx.S.arrow(null, null, { fromPoint: [x1, y], toPoint: [x1, y + 34], via: [[x1 + 50, y], [x1 + 50, y + 34]], route: 'orthogonal', fontSize: 14, dashed: m.dashed, color: m.color, frameId: ctx.fid });
      if (lab) { const t = ctx.S.text(lab, x1 + 60, y + 17, { fontSize: 14, frameId: ctx.fid }); t.y -= t.height / 2; }
      y += step + 20;
    } else {
      const ar = ctx.S.arrow(null, null, { fromPoint: [x1, y], toPoint: [x2, y], dashed: m.dashed || m.reply, color: m.color, frameId: ctx.fid });
      if (lab) { // label above the line, not on it
        const t = ctx.S.text(lab, 0, 0, { fontSize: 14, align: 'center', frameId: ctx.fid });
        t.x = (x1 + x2) / 2 - t.width / 2; t.y = y - t.height - 4;
      }
      void ar;
      y += step;
    }
  }
  const bottom = y + 10;
  ps.forEach((p) => ctx.S.line([[cx[p.id], oy + headH + 6], [cx[p.id], bottom]], { dashed: true, color: '#adb5bd', frameId: ctx.fid }));
  // send lifelines behind messages: give them indexes just above the participant boxes
  return { x: ox, y: oy, w: ps.length * colW, h: bottom - oy };
}

// ------------------------------------------------------------------ timeline
function timeline(ctx, d) {
  const fs = d.fontSize || 18;
  const items = d.items;
  const sz = items.map((it) => nodeSize({ ...it, text: it.text }, fs, ctx.style(it.style || 'milestone')));
  const gap = d.spacing || Math.max(...sz.map((z) => z.w)) * 0.75 + 30;
  const [ox, oy] = ctx.P(d.x, d.y);
  const maxH = Math.max(...sz.map((z) => z.h));
  const axisY = oy + maxH + 80;
  const x0 = ox, x1 = ox + gap * (items.length - 1) + sz[0].w;
  ctx.S.arrow(null, null, { fromPoint: [x0, axisY], toPoint: [x1 + 40, axisY], color: '#495057', frameId: ctx.fid });
  items.forEach((it, i) => {
    const cx = ox + sz[0].w / 2 + i * gap;
    const up = d.alternate === false ? true : i % 2 === 0;
    const z = sz[i];
    const by = up ? axisY - 60 - z.h : axisY + 60;
    makeNode(ctx, { ...it, id: it.id }, cx - z.w / 2, by, z.w, z.h, fs);
    ctx.S.line([[cx, up ? by + z.h : axisY], [cx, up ? axisY : by]], { color: '#adb5bd', frameId: ctx.fid });
    ctx.S.box(null, cx - 7, axisY - 7, 14, 14, { shape: 'ellipse', stroke: '#495057', bg: '#495057', frameId: ctx.fid });
    if (it.date) { const t = measure(it.date, 16); ctx.S.text(it.date, cx - t.w / 2, up ? axisY + 14 : axisY - 14 - t.h, { fontSize: 16, color: '#495057', frameId: ctx.fid }); }
  });
  return { x: ox, y: oy, w: x1 + 40 - ox, h: axisY + 60 + maxH - oy };
}

const RENDERERS = { flow, tree: (c, d) => flow(c, { direction: 'TB', ...d }), mindmap: (c, d) => flow(c, { direction: 'LR', ...d }), er: (c, d) => flow(c, { direction: 'LR', edgeRoute: 'straight', ...d }), state: flow, layers, swimlane, sequence, timeline };

function render(ctx, d) {
  const kind = d.diagram;
  const fn = RENDERERS[kind];
  if (!fn) throw new Error(`Unknown diagram type ${JSON.stringify(kind)}. Use one of: ${Object.keys(RENDERERS).join(', ')}`);
  if (d.title) {
    const [tx, ty] = ctx.P(d.x, d.y);
    ctx.S.text(d.title, tx, ty, { fontSize: d.titleSize || 28, frameId: ctx.fid });
    d = { ...d, y: (d.y || 0) + (d.titleSize || 28) * 1.25 + 30 };
  }
  const b = fn(ctx, d);
  console.log(`diagram ${kind}: ${Math.round(b.w)}×${Math.round(b.h)} at (${Math.round(b.x)},${Math.round(b.y)})`);
  return b;
}

module.exports = { render, RENDERERS };
