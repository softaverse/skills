#!/usr/bin/env node
// Summarize an .excalidraw.md file before editing it.
//
//   node inspect.js <file.excalidraw.md> [--texts] [--grep <substring>] [--region y0,y1]
//
// Always prints: hash (pass it to the spec as expectHash), bounds, free space below, frames, counts.
// If this skill wrote the file before, also prints what changed since then (the user's own edits
// in Obsidian, or plugin re-saves) so they can be preserved.
'use strict';
const fs = require('fs');
const { load, bbox, snapshotPathFor, diffScenes } = require('./lib');

const a = process.argv.slice(2);
const file = a.find((x, i) => !x.startsWith('--') && !(a[i - 1] || '').startsWith('--grep') && !(a[i - 1] || '').startsWith('--region'));
if (!file) { console.error('usage: node inspect.js <file.excalidraw.md> [--texts] [--grep str] [--region y0,y1]'); process.exit(2); }
const flag = (n) => { const i = a.indexOf('--' + n); return i >= 0 ? a[i + 1] : undefined; };

const doc = load(file);
const live = doc.data.elements.filter((e) => !e.isDeleted);
const r = (n) => Math.round(n);
const bs = live.map(bbox);
const B = bs.length ? { x0: Math.min(...bs.map((b) => b.x)), y0: Math.min(...bs.map((b) => b.y)), x1: Math.max(...bs.map((b) => b.x + b.w)), y1: Math.max(...bs.map((b) => b.y + b.h)) } : null;

console.log(`file:    ${file}`);
console.log(`hash:    ${doc.hash}`);
console.log(`format:  ${doc.format}`);
const counts = {};
live.forEach((e) => (counts[e.type] = (counts[e.type] || 0) + 1));
console.log(`live:    ${live.length} elements ${JSON.stringify(counts)} (${doc.data.elements.length - live.length} deleted)`);
if (B) {
  console.log(`bounds:  x ${r(B.x0)}..${r(B.x1)}, y ${r(B.y0)}..${r(B.y1)}`);
  console.log(`free:    everything below y=${r(B.y1)} is empty → "origin": "below" starts at x=${r(B.x0)}, y=${r(B.y1 + 150)}`);
}
const frames = live.filter((e) => e.type === 'frame');
if (frames.length) {
  console.log('frames:');
  frames.sort((p, q) => p.y - q.y).forEach((f) => {
    const kids = live.filter((e) => e.frameId === f.id).length;
    console.log(`  ${JSON.stringify(f.name)}  x ${r(f.x)}..${r(f.x + f.width)}, y ${r(f.y)}..${r(f.y + f.height)}  (${kids} children)`);
  });
}

// Changes since this skill last wrote the file
const snap = snapshotPathFor(file);
if (fs.existsSync(snap)) {
  const prev = load(snap);
  if (prev.hash === doc.hash) console.log('\nsince last write: unchanged');
  else {
    const d = diffScenes(prev.data.elements, doc.data.elements);
    console.log(`\nsince last write by this skill: file changed (${d.length ? d.length + ' meaningful changes' : 'only re-measure / re-index by the plugin'})`);
    d.slice(0, 60).forEach((l) => console.log('  ' + l));
    if (d.length > 60) console.log(`  … ${d.length - 60} more`);
    if (d.length) console.log('  → these are the user\'s edits: keep them, and don\'t re-create anything they deleted.');
  }
} else console.log('\nsince last write: (no snapshot — this skill has not written this file before)');

// Text listing
if (a.includes('--texts') || flag('grep') || flag('region')) {
  let ts = live.filter((e) => e.type === 'text');
  if (flag('grep')) ts = ts.filter((t) => t.text.includes(flag('grep')));
  if (flag('region')) { const [y0, y1] = flag('region').split(',').map(Number); ts = ts.filter((t) => t.y >= y0 && t.y < y1); }
  console.log(`\ntexts (${ts.length}):`);
  ts.sort((p, q) => p.y - q.y || p.x - q.x).forEach((t) => {
    const c = t.containerId ? live.find((e) => e.id === t.containerId) : null;
    const where = c ? `in ${c.type} ${r(c.x)},${r(c.y)} ${r(c.width)}×${r(c.height)}` : `free ${r(t.x)},${r(t.y)}`;
    const fr = t.frameId ? frames.find((f) => f.id === t.frameId) : null;
    console.log(`  [${where}${fr ? ' | frame ' + JSON.stringify(fr.name.slice(0, 12)) : ''}] ${JSON.stringify(t.text)}`);
  });
}
