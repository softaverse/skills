// Core helpers for reading, editing and writing Obsidian Excalidraw (.excalidraw.md) files.
// CommonJS, no build step. Only dependency: lz-string.
'use strict';
const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const lz = require('lz-string');

const STATE_DIR = path.join(os.homedir(), '.cache', 'obsidian-excalidraw');
const BACKUP_DIR = path.join(STATE_DIR, 'backups');
const SNAPSHOT_DIR = path.join(STATE_DIR, 'last-written');

// ---------------------------------------------------------------- file I/O

const sha256 = (buf) => crypto.createHash('sha256').update(buf).digest('hex');
const hashFile = (p) => sha256(fs.readFileSync(p));

const DRAWING_RE = /```(compressed-json|json)\n([\s\S]*?)\n```/;

// Skeleton of a fresh Obsidian Excalidraw file (same layout the plugin writes).
const NEW_FILE_TEMPLATE = `---

excalidraw-plugin: parsed
tags: [excalidraw]

---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'


# Excalidraw Data

## Text Elements
%%
## Drawing
\`\`\`compressed-json
\`\`\`
%%`;

// A new, empty drawing that has not been written anywhere yet (hash null = "file must not exist").
function create(filePath) {
  return {
    path: filePath, src: NEW_FILE_TEMPLATE.replace('```compressed-json\n```', '```compressed-json\nX\n```'), format: 'compressed-json', hash: null, isNew: true,
    data: { type: 'excalidraw', version: 2, source: 'https://github.com/zsviczian/obsidian-excalidraw-plugin', elements: [], appState: { gridSize: null, viewBackgroundColor: '#ffffff' }, files: {} },
  };
}

function load(filePath) {
  const src = fs.readFileSync(filePath, 'utf8');
  const m = src.match(DRAWING_RE);
  if (!m) throw new Error(`No \`\`\`compressed-json or \`\`\`json drawing block in ${filePath}. Is it an Excalidraw file?`);
  const format = m[1];
  const raw = format === 'compressed-json' ? lz.decompressFromBase64(m[2].replace(/\s/g, '')) : m[2];
  if (!raw) throw new Error('Drawing block could not be decompressed');
  const data = JSON.parse(raw);
  if (!Array.isArray(data.elements)) throw new Error('Drawing JSON has no elements array');
  return { path: filePath, src, format, data, hash: sha256(Buffer.from(src, 'utf8')) };
}

// Rebuild the "## Text Elements" section from the live text elements so the
// markdown index never drifts from the JSON (the Obsidian plugin reads both).
function syncTextSection(src, elements) {
  const live = elements.filter((e) => e.type === 'text' && !e.isDeleted);
  const body = live.map((t) => `${t.rawText ?? t.originalText ?? t.text} ^${t.id}\n\n`).join('');
  const start = src.indexOf('## Text Elements\n');
  if (start === -1) return src; // plugin variant without the section: leave untouched
  const from = start + '## Text Elements\n'.length;
  // section ends at the next "%%" line or the next "## " heading
  const rest = src.slice(from);
  const endRe = /^(%%|## )/m;
  const em = rest.match(endRe);
  const to = em ? from + em.index : src.length;
  return src.slice(0, from) + body + src.slice(to);
}

function serialize(doc) {
  const json = JSON.stringify(doc.data);
  let block;
  if (doc.format === 'compressed-json') {
    block = lz.compressToBase64(json).match(/.{1,256}/g).join('\n\n');
  } else {
    block = JSON.stringify(doc.data, null, '\t');
  }
  let out = doc.src.replace(DRAWING_RE, () => '```' + doc.format + '\n' + block + '\n```');
  out = syncTextSection(out, doc.data.elements);
  return out;
}

function snapshotPathFor(target) {
  const key = sha256(path.resolve(target)).slice(0, 16);
  return path.join(SNAPSHOT_DIR, `${key}--${path.basename(target)}`);
}

// ---------------------------------------------------------------- geometry & text

// Excalifont-ish estimate: CJK / full-width ≈ 1em, everything else ≈ 0.6em, line height 1.25.
// Slightly generous on purpose — overflow is worse than a little slack.
function measure(text, fontSize) {
  const lines = String(text).split('\n');
  let w = 0;
  for (const l of lines) {
    let lw = 0;
    for (const ch of l) lw += (ch.codePointAt(0) > 0x2e80 ? 1 : 0.6) * fontSize;
    w = Math.max(w, lw);
  }
  return { w: Math.ceil(w), h: Math.ceil(lines.length * fontSize * 1.25) };
}

function bbox(e) {
  if (e.type === 'arrow' || e.type === 'line') {
    const xs = e.points.map((p) => e.x + p[0]);
    const ys = e.points.map((p) => e.y + p[1]);
    const x = Math.min(...xs), y = Math.min(...ys);
    return { x, y, w: Math.max(...xs) - x, h: Math.max(...ys) - y };
  }
  return { x: e.x, y: e.y, w: e.width, h: e.height };
}
const intersects = (a, b) => a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
const contains = (outer, inner) => inner.x >= outer.x && inner.y >= outer.y && inner.x + inner.w <= outer.x + outer.w && inner.y + inner.h <= outer.y + outer.h;

// ---------------------------------------------------------------- scene wrapper

const B62 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
const rid = (n) => { let s = ''; for (let i = 0; i < n; i++) s += B62[1 + crypto.randomInt(61)]; return s; };
const rseed = () => crypto.randomInt(1, 2 ** 31 - 1);

class Scene {
  constructor(doc) {
    this.doc = doc;
    this.els = doc.data.elements;
    this.now = Date.now();
    this.added = new Set();
    this.modified = new Set();
    this.deleted = new Set();
    this.warnings = [];
    const maxIx = this.live().map((e) => e.index).filter(Boolean).sort().pop() || 'a0';
    this._ixBase = maxIx + 'V';
    this._ixN = 0;
  }
  live() { return this.els.filter((e) => !e.isDeleted); }
  byId(id) { return this.els.find((e) => e.id === id); }
  warn(msg) { this.warnings.push(msg); }

  nextIndex() {
    let k;
    do { this._ixN++; k = B62[Math.floor(this._ixN / 62) % 62] + B62[this._ixN % 62]; } while (k.endsWith('0'));
    return this._ixBase + k;
  }
  bump(e) {
    e.version = (e.version || 1) + 1;
    e.versionNonce = rseed();
    e.updated = this.now;
    if (!this.added.has(e.id)) this.modified.add(e.id);
  }

  // ------------ lookup
  findText(q) {
    // q: { find?: exact text, contains?: substring, startsWith?: prefix, within?: {x:[a,b], y:[a,b]} }
    let c = this.live().filter((e) => e.type === 'text');
    if (q.find != null) c = c.filter((e) => e.text === q.find);
    if (q.contains != null) c = c.filter((e) => e.text.includes(q.contains));
    if (q.startsWith != null) c = c.filter((e) => e.text.startsWith(q.startsWith));
    if (q.within) {
      c = c.filter((e) => (!q.within.y || (e.y >= q.within.y[0] && e.y < q.within.y[1])) && (!q.within.x || (e.x >= q.within.x[0] && e.x < q.within.x[1])));
    }
    if (c.length !== 1) {
      const sample = c.slice(0, 5).map((e) => `  ${e.id} @(${Math.round(e.x)},${Math.round(e.y)}) ${JSON.stringify(e.text.slice(0, 40))}`).join('\n');
      throw new Error(`Text query ${JSON.stringify(q)} matched ${c.length} elements (need exactly 1).${sample ? '\n' + sample : ''}\nNarrow it with "within" or a longer "find".`);
    }
    return c[0];
  }
  findFrame(prefix) {
    const f = this.live().filter((e) => e.type === 'frame' && (e.name || '').startsWith(prefix));
    if (f.length !== 1) throw new Error(`Frame prefix ${JSON.stringify(prefix)} matched ${f.length} frames`);
    return f[0];
  }
  // A reference to a shape: local id from this spec, {find:...} text query (resolves to its container), or raw element id.
  resolve(ref, localIds) {
    if (typeof ref === 'string') {
      if (localIds && localIds[ref]) return localIds[ref];
      const e = this.byId(ref);
      if (e && !e.isDeleted) return e;
      throw new Error(`Unknown reference ${JSON.stringify(ref)}`);
    }
    if (ref && ref.frame) return this.findFrame(ref.frame);
    const t = this.findText(ref);
    return t.containerId ? this.byId(t.containerId) : t;
  }

  // ------------ element factories
  base(o) {
    return {
      angle: 0, strokeColor: '#1e1e1e', backgroundColor: 'transparent', fillStyle: 'solid', strokeWidth: 2,
      strokeStyle: 'solid', roughness: 1, opacity: 100, groupIds: [], frameId: null, index: this.nextIndex(),
      seed: rseed(), version: 1, versionNonce: rseed(), isDeleted: false, boundElements: [], updated: this.now,
      link: null, locked: false, ...o,
    };
  }
  push(e) { this.els.push(e); this.added.add(e.id); return e; }

  text(t, x, y, { fontSize = 20, color = '#1e1e1e', align = 'left', containerId = null, frameId = null } = {}) {
    const { w, h } = measure(t, fontSize);
    return this.push(this.base({
      id: rid(8), type: 'text', x, y, width: w, height: h, roundness: null, strokeColor: color, frameId,
      text: t, rawText: t, originalText: t, fontSize, fontFamily: 5, textAlign: align,
      verticalAlign: containerId ? 'middle' : 'top', containerId, autoResize: true, lineHeight: 1.25,
    }));
  }

  // Re-measure and re-center a bound text inside its container (rectangle) or on its arrow midpoint.
  place(t) {
    const { w, h } = measure(t.text, t.fontSize);
    t.width = w; t.height = h;
    const c = t.containerId && this.byId(t.containerId);
    if (!c) return;
    if (c.type === 'arrow') {
      const [mx, my] = Scene.pathMidpoint(c);
      t.x = mx - w / 2; t.y = my - h / 2;
    } else {
      t.x = t.textAlign === 'left' ? c.x + 12 : c.x + (c.width - w) / 2;
      t.y = c.y + (c.height - h) / 2;
      // usable area: diamonds/ellipses only fit text in their middle
      const k = c.type === 'diamond' ? 0.55 : c.type === 'ellipse' ? 0.72 : 1;
      if (w > c.width * k - 16 || h > c.height * k - 8) {
        this.warn(`OVERFLOW: text ${JSON.stringify(t.text.slice(0, 30))} needs ~${w}x${h}, box is ${Math.round(c.width)}x${Math.round(c.height)} — widen/heighten the box, add line breaks, or lower fontSize`);
      }
    }
  }

  box(t, x, y, w, h, st = {}) {
    const fontSize = st.fontSize || 20;
    const shape = st.shape || 'rectangle';
    if (t && (w == null || h == null)) {
      const s = Scene.autoSize(t, fontSize, shape);
      if (w == null) w = s.w;
      if (h == null) h = s.h;
    }
    const r = this.push(this.base({
      id: rid(21), type: shape, x, y, width: w, height: h,
      strokeColor: st.stroke || '#1e1e1e', backgroundColor: st.bg || 'transparent',
      strokeStyle: st.dashed ? 'dashed' : 'solid', strokeWidth: st.strokeWidth || 2,
      roundness: st.square || shape === 'diamond' ? (shape === 'diamond' ? { type: 2 } : null) : shape === 'ellipse' ? { type: 2 } : { type: 3 }, frameId: st.frameId || null,
    }));
    if (t) {
      const tx = this.text(t, x, y, { fontSize, color: st.textColor || '#1e1e1e', align: st.align || 'center', containerId: r.id, frameId: st.frameId || null });
      r.boundElements.push({ type: 'text', id: tx.id });
      this.place(tx);
    }
    return r;
  }

  // Absolute point halfway along an arrow/line path.
  static pathMidpoint(a) {
    const P = a.points.map((p) => [a.x + p[0], a.y + p[1]]);
    const seg = []; let total = 0;
    for (let i = 1; i < P.length; i++) { const l = Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]); seg.push(l); total += l; }
    let half = total / 2;
    for (let i = 1; i < P.length; i++) {
      if (half <= seg[i - 1] || i === P.length - 1) { const f = seg[i - 1] ? half / seg[i - 1] : 0; return [P[i - 1][0] + (P[i][0] - P[i - 1][0]) * f, P[i - 1][1] + (P[i][1] - P[i - 1][1]) * f]; }
      half -= seg[i - 1];
    }
    return P[0];
  }

  // Plain line (lifelines, axes, separators). points are absolute.
  line(points, o = {}) {
    const p0 = points[0];
    const pts = points.map((p) => [p[0] - p0[0], p[1] - p0[1]]);
    const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
    return this.push(this.base({
      id: rid(21), type: 'line', x: p0[0], y: p0[1], width: Math.max(...xs) - Math.min(...xs), height: Math.max(...ys) - Math.min(...ys),
      strokeColor: o.color || '#868e96', strokeStyle: o.dashed ? 'dashed' : 'solid', strokeWidth: o.strokeWidth || 2, roundness: null,
      points: pts, lastCommittedPoint: null, startBinding: null, endBinding: null, startArrowhead: null, endArrowhead: null, frameId: o.frameId || null,
    }));
  }

  // After a shape moved/resized: re-attach every arrow bound to it.
  // Two-point arrows are re-routed between the shapes' current sides; polylines keep their middle points
  // and only move the end that touches this shape.
  reroute(shape) {
    for (const be of shape.boundElements || []) {
      if (be.type !== 'arrow') continue;
      const ar = this.byId(be.id);
      if (!ar || ar.isDeleted) continue;
      const P = ar.points.map((p) => [ar.x + p[0], ar.y + p[1]]);
      const sId = ar.startBinding && ar.startBinding.elementId, eId = ar.endBinding && ar.endBinding.elementId;
      const sEl = sId && this.byId(sId), eEl = eId && this.byId(eId);
      if (P.length === 2 && sEl && eEl) {
        const [sa, sb] = Scene.autoSides(bbox(sEl), bbox(eEl));
        P[0] = Scene.sidePoint(bbox(sEl), sa); P[1] = Scene.sidePoint(bbox(eEl), sb);
      } else {
        const fix = (idx, el) => {
          const b = bbox(el), q = P[idx];
          const cx = Math.min(Math.max(q[0], b.x), b.x + b.w), cy = Math.min(Math.max(q[1], b.y), b.y + b.h);
          // snap to the nearest side of the new box
          const d = [['left', Math.abs(q[0] - b.x)], ['right', Math.abs(q[0] - b.x - b.w)], ['top', Math.abs(q[1] - b.y)], ['bottom', Math.abs(q[1] - b.y - b.h)]].sort((u, v) => u[1] - v[1])[0][0];
          P[idx] = d === 'left' ? [b.x - 5, cy] : d === 'right' ? [b.x + b.w + 5, cy] : d === 'top' ? [cx, b.y - 5] : [cx, b.y + b.h + 5];
        };
        if (sId === shape.id) fix(0, shape);
        if (eId === shape.id) fix(P.length - 1, shape);
      }
      ar.x = P[0][0]; ar.y = P[0][1];
      ar.points = P.map((p) => [p[0] - P[0][0], p[1] - P[0][1]]);
      const xs = ar.points.map((p) => p[0]), ys = ar.points.map((p) => p[1]);
      ar.width = Math.max(...xs) - Math.min(...xs); ar.height = Math.max(...ys) - Math.min(...ys);
      this.bump(ar);
      for (const lb of ar.boundElements || []) if (lb.type === 'text') { const t = this.byId(lb.id); if (t) { this.place(t); this.bump(t); } }
    }
  }

  // Size that comfortably fits text in a given shape.
  static autoSize(t, fontSize, shape = 'rectangle') {
    const m = measure(t, fontSize);
    let w = m.w + 40, h = m.h + 30;
    if (shape === 'diamond') { w = Math.ceil(m.w / 0.55) + 30; h = Math.ceil(m.h / 0.55) + 20; }
    if (shape === 'ellipse') { w = Math.ceil(m.w / 0.72) + 24; h = Math.ceil(m.h / 0.72) + 16; }
    return { w: Math.max(w, 60), h: Math.max(h, 50) };
  }

  static sidePoint(b, side, offset = 0) {
    switch (side) {
      case 'left': return [b.x - 5, b.y + b.h / 2 + offset];
      case 'right': return [b.x + b.w + 5, b.y + b.h / 2 + offset];
      case 'top': return [b.x + b.w / 2 + offset, b.y - 5];
      case 'bottom': return [b.x + b.w / 2 + offset, b.y + b.h + 5];
      default: throw new Error('Unknown side ' + side);
    }
  }
  static autoSides(a, b) {
    const ca = [a.x + a.w / 2, a.y + a.h / 2], cb = [b.x + b.w / 2, b.y + b.h / 2];
    const dx = cb[0] - ca[0], dy = cb[1] - ca[1];
    // prefer horizontal when the boxes don't overlap horizontally
    const hGap = Math.max(b.x - (a.x + a.w), a.x - (b.x + b.w));
    if (hGap > 0 && (Math.abs(dx) >= Math.abs(dy) * 0.5)) return dx > 0 ? ['right', 'left'] : ['left', 'right'];
    return dy > 0 ? ['bottom', 'top'] : ['top', 'bottom'];
  }

  // Arrow between two shapes (a/b may be null for a free arrow — then fromPoint/toPoint are required).
  // o.via: absolute intermediate points (polyline). o.route: 'straight' (default) | 'orthogonal' (right-angle path).
  arrow(a, b, o = {}) {
    const ba = a && bbox(a), bb = b && bbox(b);
    let [sa, sb] = a && b ? Scene.autoSides(ba, bb) : ['right', 'left'];
    if (o.fromSide) sa = o.fromSide;
    if (o.toSide) sb = o.toSide;
    const p1 = o.fromPoint || Scene.sidePoint(ba, sa, o.fromOffset || 0);
    const p2 = o.toPoint || Scene.sidePoint(bb, sb, o.toOffset || 0);
    let via = o.via || [];
    if (!via.length && o.route === 'orthogonal' && p1[0] !== p2[0] && p1[1] !== p2[1]) {
      const horizontalStart = sa === 'left' || sa === 'right';
      via = horizontalStart ? [[(p1[0] + p2[0]) / 2, p1[1]], [(p1[0] + p2[0]) / 2, p2[1]]] : [[p1[0], (p1[1] + p2[1]) / 2], [p2[0], (p1[1] + p2[1]) / 2]];
    }
    const pts = [p1, ...via, p2].map((p) => [p[0] - p1[0], p[1] - p1[1]]);
    const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
    const ar = this.push(this.base({
      id: rid(21), type: 'arrow', x: p1[0], y: p1[1], width: Math.max(...xs) - Math.min(...xs), height: Math.max(...ys) - Math.min(...ys),
      strokeColor: o.color || '#1e1e1e', strokeStyle: o.dashed ? 'dashed' : 'solid', strokeWidth: o.strokeWidth || 2,
      roundness: via.length && o.route === 'orthogonal' ? null : { type: 2 }, frameId: o.frameId || null,
      points: pts, lastCommittedPoint: null,
      startBinding: a ? { elementId: a.id, focus: 0, gap: 5 } : null, endBinding: b ? { elementId: b.id, focus: 0, gap: 5 } : null,
      startArrowhead: o.startArrowhead || null, endArrowhead: o.endArrowhead === undefined ? 'arrow' : o.endArrowhead, elbowed: false,
    }));
    for (const e of [a, b].filter(Boolean)) {
      e.boundElements = e.boundElements || [];
      e.boundElements.push({ type: 'arrow', id: ar.id });
      if (!this.added.has(e.id)) this.bump(e);
    }
    if (o.label) {
      const tx = this.text(o.label, 0, 0, { fontSize: o.fontSize || 14, color: o.color || '#1e1e1e', align: 'center', containerId: ar.id, frameId: o.frameId || null });
      ar.boundElements.push({ type: 'text', id: tx.id });
      this.place(tx);
    }
    return ar;
  }

  frame(name, x, y, w, h) {
    return this.push(this.base({ id: rid(21), type: 'frame', x, y, width: w, height: h, roundness: null, name }));
  }

  // ------------ edits
  setText(t, newText, o = {}) {
    t.text = t.rawText = t.originalText = newText;
    if (o.fontSize) t.fontSize = o.fontSize;
    if (o.color) t.strokeColor = o.color;
    this.place(t);
    this.bump(t);
  }
  styleContainer(c, st) {
    if (st.stroke) c.strokeColor = st.stroke;
    if (st.bg) c.backgroundColor = st.bg;
    if (st.dashed !== undefined) c.strokeStyle = st.dashed ? 'dashed' : 'solid';
    if (st.color && c.type === 'arrow') c.strokeColor = st.color;
    this.bump(c);
  }
  resize(c, { dw = 0, dh = 0, w, h } = {}) {
    if (w != null) c.width = w; else c.width += dw;
    if (h != null) c.height = h; else c.height += dh;
    this.bump(c);
    for (const be of c.boundElements || []) if (be.type === 'text') { const t = this.byId(be.id); this.place(t); this.bump(t); }
    this.reroute(c);
  }
  // Move a shape together with its bound text, and re-attach its arrows.
  moveShape(c, dx, dy) {
    this.move(c, dx, dy);
    for (const be of c.boundElements || []) if (be.type === 'text') { const t = this.byId(be.id); if (t) this.move(t, dx, dy); }
    this.reroute(c);
  }
  remove(e) {
    e.isDeleted = true; this.bump(e); this.deleted.add(e.id);
    // drop dangling references
    for (const o of this.live()) {
      if (o.boundElements && o.boundElements.some((b) => b.id === e.id)) { o.boundElements = o.boundElements.filter((b) => b.id !== e.id); this.bump(o); }
      if (o.type === 'arrow') {
        if (o.startBinding && o.startBinding.elementId === e.id) { o.startBinding = null; this.bump(o); this.warn(`Arrow ${o.id} lost its start binding (target deleted)`); }
        if (o.endBinding && o.endBinding.elementId === e.id) { o.endBinding = null; this.bump(o); this.warn(`Arrow ${o.id} lost its end binding (target deleted)`); }
      }
    }
  }
  move(e, dx, dy) { e.x += dx; e.y += dy; this.bump(e); }

  fitFrame(f, padding = 40) {
    const kids = this.live().filter((e) => e.frameId === f.id);
    if (!kids.length) return;
    const bs = kids.map(bbox);
    const x0 = Math.min(...bs.map((b) => b.x)) - padding, y0 = Math.min(...bs.map((b) => b.y)) - padding;
    const x1 = Math.max(...bs.map((b) => b.x + b.w)) + padding, y1 = Math.max(...bs.map((b) => b.y + b.h)) + padding;
    // grow only — never shrink a frame the user sized
    const nx = Math.min(f.x, x0), ny = Math.min(f.y, y0);
    const nr = Math.max(f.x + f.width, x1), nb = Math.max(f.y + f.height, y1);
    if (nx !== f.x || ny !== f.y || nr !== f.x + f.width || nb !== f.y + f.height) {
      f.x = nx; f.y = ny; f.width = nr - nx; f.height = nb - ny; this.bump(f);
    }
  }

  bounds(filter = () => true) {
    const bs = this.live().filter(filter).map(bbox);
    if (!bs.length) return null;
    const x = Math.min(...bs.map((b) => b.x)), y = Math.min(...bs.map((b) => b.y));
    return { x, y, w: Math.max(...bs.map((b) => b.x + b.w)) - x, h: Math.max(...bs.map((b) => b.y + b.h)) - y };
  }
}

// ---------------------------------------------------------------- semantic diff

function diffScenes(oldEls, newEls) {
  const A = new Map(oldEls.map((e) => [e.id, e]));
  const out = [];
  const label = (e) => e.type === 'frame' ? `frame ${JSON.stringify(e.name)}` : e.type === 'text' ? `text ${JSON.stringify(e.text.slice(0, 50))}` : `${e.type} ${e.id}`;
  for (const e of newEls) {
    const o = A.get(e.id);
    if (!o) { if (!e.isDeleted) out.push(`NEW      ${label(e)} @(${Math.round(e.x)},${Math.round(e.y)})`); continue; }
    if (!o.isDeleted && e.isDeleted) { out.push(`DELETED  ${label(o)}`); continue; }
    if (e.isDeleted) continue;
    if (o.text !== e.text) out.push(`TEXT     ${JSON.stringify((o.text || '').slice(0, 40))} → ${JSON.stringify((e.text || '').slice(0, 40))}`);
    if (o.name !== e.name) out.push(`RENAMED  frame ${JSON.stringify(o.name)} → ${JSON.stringify(e.name)}`);
    if (Math.abs(o.x - e.x) > 20 || Math.abs(o.y - e.y) > 20) out.push(`MOVED    ${label(e)} (${Math.round(o.x)},${Math.round(o.y)}) → (${Math.round(e.x)},${Math.round(e.y)})`);
    else if (Math.abs((o.width || 0) - (e.width || 0)) > 20 || Math.abs((o.height || 0) - (e.height || 0)) > 20) out.push(`RESIZED  ${label(e)}`);
    if (o.strokeColor !== e.strokeColor || o.backgroundColor !== e.backgroundColor || o.strokeStyle !== e.strokeStyle) out.push(`RESTYLED ${label(e)}`);
  }
  for (const o of oldEls) if (!o.isDeleted && !newEls.some((e) => e.id === o.id)) out.push(`REMOVED  ${label(o)}`);
  return out;
}

module.exports = {
  STATE_DIR, BACKUP_DIR, SNAPSHOT_DIR, sha256, hashFile, load, create, serialize, syncTextSection, snapshotPathFor,
  measure, bbox, intersects, contains, Scene, diffScenes,
};
