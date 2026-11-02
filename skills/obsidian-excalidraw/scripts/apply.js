#!/usr/bin/env node
// Apply a declarative drawing spec to an .excalidraw.md file and write a CANDIDATE copy.
// The original file is never touched here — use commit.js to write it back safely.
//
//   node apply.js <file.excalidraw.md> <spec.json> --out <candidate.excalidraw.md>
//
// Prints a summary + warnings, and writes <candidate>.changes.json (added/modified/deleted ids, warnings)
// which preview.js uses to render only the affected region.
'use strict';
const fs = require('fs');
const path = require('path');
const { load, create, serialize, bbox, intersects, contains, Scene } = require('./lib');
const layout = require('./layout');
const STYLES = require('./styles.json');

function args() {
  const a = process.argv.slice(2);
  const pos = a.filter((x, i) => !x.startsWith('--') && !(a[i - 1] || '').startsWith('--'));
  const flag = (n) => { const i = a.indexOf('--' + n); return i >= 0 ? a[i + 1] : undefined; };
  if (pos.length < 2 || !flag('out')) {
    console.error('usage: node apply.js <file.excalidraw.md> <spec.json> --out <candidate.excalidraw.md>');
    process.exit(2);
  }
  return { file: pos[0], spec: pos[1], out: flag('out') };
}

function styleOf(spec, name, extra = {}) {
  const custom = (spec.styles || {})[name];
  const st = custom || STYLES[name];
  if (name && (!st || name.startsWith('_'))) throw new Error(`Unknown style ${JSON.stringify(name)}. Known: ${Object.keys({ ...STYLES, ...(spec.styles || {}) }).filter((k) => !k.startsWith('_')).join(', ')}`);
  // only explicit (defined) overrides may replace style values
  const defined = Object.fromEntries(Object.entries(extra).filter(([, v]) => v !== undefined));
  return { ...(st || {}), ...defined };
}

function main() {
  const { file, spec: specPath, out } = args();
  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  let doc;
  if (fs.existsSync(file)) doc = load(file);
  else if (spec.create) { doc = create(file); console.log('new file: ' + file); }
  else throw new Error(`${file} does not exist. To start a new drawing set "create": true in the spec.`);
  if (spec.create && !doc.isNew) throw new Error(`"create": true but ${file} already exists — inspect it and edit instead of overwriting.`);
  if (!doc.isNew && spec.expectHash && spec.expectHash !== doc.hash) {
    throw new Error(`File changed since it was inspected (expectHash mismatch). Re-run inspect.js and rebuild the spec on the current content.\n  expected ${spec.expectHash}\n  actual   ${doc.hash}`);
  }
  const S = new Scene(doc);
  const ids = {}; // local spec ids → elements

  // 1) shift existing content to make room (before adding, so new content lands in the gap)
  for (const sh of spec.shift || []) {
    const movers = S.live().filter((e) => e.y >= sh.fromY && (!sh.x || (e.x >= sh.x[0] && e.x < sh.x[1])));
    for (const e of movers) S.move(e, sh.dx || 0, sh.dy || 0);
    for (const e of S.live().filter((e) => e.type === 'arrow' && e.y < sh.fromY)) {
      const b = bbox(e);
      if (b.y + b.h >= sh.fromY) S.warn(`Arrow ${e.id} crosses shift line y=${sh.fromY}; it was not moved — check it in the preview`);
    }
    console.log(`shift: moved ${movers.length} elements from y≥${sh.fromY} by (${sh.dx || 0},${sh.dy || 0})`);
  }

  // 2) origin for new elements
  let ox = 0, oy = 0;
  if (spec.origin === 'below' || (spec.origin && spec.origin.below)) {
    const gap = (spec.origin && spec.origin.gap) || 150;
    const b = S.bounds((e) => !S.added.has(e.id));
    ox = b ? b.x + ((spec.origin && spec.origin.dx) || 0) : 0;
    oy = b ? b.y + b.h + gap : 0;
  } else if (spec.origin) { ox = spec.origin.x || 0; oy = spec.origin.y || 0; }
  if (spec.origin) console.log(`origin: (${Math.round(ox)}, ${Math.round(oy)})`);

  // 3) frame (new or existing) that added elements belong to
  let frame = null, newFrame = false;
  if (spec.frame && spec.frame.into) frame = S.findFrame(spec.frame.into);
  else if (spec.frame && spec.frame.name) { frame = S.frame(spec.frame.name, ox, oy, 10, 10); newFrame = true; }
  const fid = frame ? frame.id : null;
  const P = (x, y) => [ox + (x || 0), oy + (y || 0)];

  // 4) add
  for (const it of spec.add || []) {
    const kind = it.type || (it.diagram ? 'diagram' : it.arrow ? 'arrow' : it.table ? 'table' : it.text != null && it.w == null && it.style == null && !it.box ? 'text' : 'box');
    if (kind === 'box') {
      const [x, y] = P(it.x, it.y);
      const st = styleOf(spec, it.style, { fontSize: it.fontSize, align: it.align, dashed: it.dashed, square: it.square, stroke: it.stroke, bg: it.bg, shape: it.shape });
      st.frameId = fid;
      const r = S.box(it.text ?? it.box ?? null, x, y, it.w, it.h, st);
      if (it.id) ids[it.id] = r;
    } else if (kind === 'text') {
      const [x, y] = P(it.x, it.y);
      const t = S.text(it.text, x, y, { fontSize: it.fontSize || 20, color: it.color || (it.style && styleOf(spec, it.style).stroke) || '#1e1e1e', frameId: fid });
      if (it.id) ids[it.id] = t;
    } else if (kind === 'arrow') {
      const [fromRef, toRef] = it.arrow || [it.from, it.to];
      const a = S.resolve(fromRef, ids), b = S.resolve(toRef, ids);
      const abs = (p) => p && P(p[0], p[1]);
      const ar = S.arrow(a, b, {
        label: it.label, fontSize: it.fontSize, dashed: it.dashed, color: it.color || (it.style && styleOf(spec, it.style).stroke),
        fromSide: it.fromSide, toSide: it.toSide, fromOffset: it.fromOffset, toOffset: it.toOffset,
        fromPoint: it.fromPointAbs || abs(it.fromPoint), toPoint: it.toPointAbs || abs(it.toPoint), endArrowhead: it.endArrowhead, startArrowhead: it.startArrowhead, frameId: fid,
      });
      if (it.id) ids[it.id] = ar;
    } else if (kind === 'table') {
      addTable(S, spec, it, P, fid, ids);
    } else if (kind === 'diagram') {
      layout.render({ S, P, fid, ids, style: (n, extra = {}) => styleOf(spec, n, extra) }, it);
    } else throw new Error('Unknown add item ' + JSON.stringify(it));
  }

  // 5) edits on existing (or just-added) text and their containers
  for (const ed of spec.edit || []) {
    const t = S.findText(ed.target || ed);
    const c = t.containerId ? S.byId(t.containerId) : null;
    if (ed.text != null || ed.fontSize || ed.color) S.setText(t, ed.text ?? t.text, { fontSize: ed.fontSize, color: ed.color });
    if (c && (ed.style || ed.stroke || ed.bg || ed.dashed !== undefined || (ed.color && c.type === 'arrow'))) {
      S.styleContainer(c, { ...(ed.style ? styleOf(spec, ed.style) : {}), stroke: ed.stroke, bg: ed.bg, dashed: ed.dashed, color: ed.color });
      if (ed.style && styleOf(spec, ed.style).stroke && c.type === 'arrow') c.strokeColor = styleOf(spec, ed.style).stroke;
    }
    if (c && (ed.resize || ed.dh || ed.dw)) S.resize(c, ed.resize || { dh: ed.dh || 0, dw: ed.dw || 0 });
    if (c && c.type !== 'arrow' && ed.moveTo) S.moveShape(c, ed.moveTo.x != null ? ed.moveTo.x - c.x : 0, ed.moveTo.y != null ? ed.moveTo.y - c.y : 0);
    else if (c && c.type !== 'arrow' && ed.moveBy) S.moveShape(c, ed.moveBy.dx || 0, ed.moveBy.dy || 0);
    else if (!c && (ed.moveTo || ed.moveBy)) S.move(t, ed.moveBy ? ed.moveBy.dx || 0 : ed.moveTo.x - t.x, ed.moveBy ? ed.moveBy.dy || 0 : ed.moveTo.y - t.y);
    else if (c) S.place(t);
  }
  for (const fr of spec.frameEdit || []) {
    const f = S.findFrame(fr.frame);
    if (fr.name) { f.name = fr.name; S.bump(f); }
    if (fr.dh || fr.dw) S.resize(f, { dh: fr.dh || 0, dw: fr.dw || 0 });
  }

  // 6) delete
  for (const dl of spec.delete || []) {
    const t = S.findText(dl.target || dl);
    const c = t.containerId ? S.byId(t.containerId) : null;
    S.remove(t);
    if (c && c.type !== 'arrow' && !dl.keepContainer) S.remove(c);
  }

  // 7) frames: fit new frame / grow existing frame to its children
  if (frame) S.fitFrame(frame, (spec.frame && spec.frame.padding) || 40);

  // 8) overlap check: new top-level shapes vs existing shapes (ignores frames and anything the new shape sits inside)
  const newTop = S.live().filter((e) => S.added.has(e.id) && !e.containerId && e.type !== 'frame' && e.type !== 'arrow');
  const oldTop = S.live().filter((e) => !S.added.has(e.id) && !e.containerId && e.type !== 'frame' && e.type !== 'arrow');
  for (const n of newTop) {
    const bn = bbox(n);
    for (const o of oldTop) {
      const bo = bbox(o);
      if (intersects(bn, bo) && !contains(bo, bn)) {
        const label = (e) => { const tx = e.type === 'text' ? e : (e.boundElements || []).map((b) => S.byId(b.id)).find((x) => x && x.type === 'text'); return tx ? JSON.stringify(tx.text.slice(0, 25)) : e.type + ' ' + e.id; };
        S.warn(`OVERLAP: new ${label(n)} intersects existing ${label(o)} @(${Math.round(bo.x)},${Math.round(bo.y)})`);
      }
    }
  }
  if (newFrame) {
    const fb = bbox(frame);
    for (const o of S.live().filter((e) => e.type === 'frame' && e.id !== frame.id)) if (intersects(fb, bbox(o))) S.warn(`OVERLAP: new frame intersects existing frame ${JSON.stringify(o.name)}`);
  }

  fs.writeFileSync(out, serialize(doc));
  const changes = {
    source: path.resolve(file), sourceHash: doc.hash, isNew: !!doc.isNew, candidate: path.resolve(out),
    added: [...S.added], modified: [...S.modified].filter((id) => !S.deleted.has(id)), deleted: [...S.deleted],
    localIds: Object.fromEntries(Object.entries(ids).map(([k, v]) => [k, v.id])), warnings: S.warnings,
  };
  fs.writeFileSync(out + '.changes.json', JSON.stringify(changes, null, 2));
  // sanity: candidate must load
  const check = load(out);
  console.log(`candidate: ${out}`);
  console.log(`elements: ${check.data.elements.filter((e) => !e.isDeleted).length} live (added ${changes.added.length}, modified ${changes.modified.length}, deleted ${changes.deleted.length})`);
  console.log(`source hash: ${doc.hash}`);
  if (S.warnings.length) { console.log(`\nWARNINGS (${S.warnings.length}):`); S.warnings.forEach((w) => console.log('  - ' + w)); }
  else console.log('no warnings');
}

function addTable(S, spec, it, P, fid, ids) {
  const fs_ = it.fontSize || 18;
  const cols = it.columns.map((c) => (typeof c === 'string' ? { title: c } : c));
  const lineH = fs_ * 1.25;
  const autoH = (texts) => Math.max(it.rowHeight || 50, ...texts.map((t) => Math.ceil(String(t ?? '').split('\n').length * lineH + 20)));
  // column widths: explicit, else fit content
  cols.forEach((c, i) => {
    if (c.w) return;
    const texts = [c.title, ...it.rows.map((r) => { const cell = (r.cells || r)[i]; return cell && typeof cell === 'object' ? cell.text : cell; })];
    c.w = Math.max(120, ...texts.map((t) => require('./lib').measure(String(t ?? ''), fs_).w + 32));
  });
  let [x0, y] = P(it.x, it.y);
  const head = styleOf(spec, it.headerStyle || 'header', { fontSize: fs_, square: true, frameId: fid });
  const hh = autoH(cols.map((c) => c.title));
  let x = x0;
  for (const c of cols) { S.box(c.title, x, y, c.w, hh, head); x += c.w; }
  y += hh;
  const spans = new Array(cols.length).fill(0); // remaining rows covered by a vertical span
  const rows = it.rows.map((r) => (Array.isArray(r) ? { cells: r } : r));
  const heights = rows.map((r) => r.h || autoH(r.cells.map((c) => (c && typeof c === 'object' ? (c.span > 1 ? '' : c.text) : c))));
  rows.forEach((r, ri) => {
    let x = x0;
    const rowSt = styleOf(spec, r.style || it.rowStyle || 'cell', { fontSize: fs_, square: true, frameId: fid });
    r.cells.forEach((cell, ci) => {
      const w = cols[ci].w;
      if (spans[ci] > 0) { spans[ci]--; x += w; return; }
      const obj = cell && typeof cell === 'object' ? cell : { text: cell };
      const span = obj.span || 1;
      const h = heights.slice(ri, ri + span).reduce((s, v) => s + v, 0);
      const st = obj.style ? styleOf(spec, obj.style, { fontSize: fs_, square: true, frameId: fid }) : rowSt;
      const b = S.box(obj.text == null || obj.text === '' ? null : String(obj.text), x, y, w, h, st);
      if (obj.id) ids[obj.id] = b;
      if (span > 1) spans[ci] = span - 1;
      x += w;
    });
    y += heights[ri];
  });
  console.log(`table: ${cols.length} cols × ${rows.length} rows, ${cols.reduce((s, c) => s + c.w, 0)}×${Math.round(y - P(it.x, it.y)[1])} at (${Math.round(x0)},${Math.round(P(it.x, it.y)[1])})`);
}

try { main(); } catch (e) { console.error('ERROR: ' + e.message); process.exit(1); }
