#!/usr/bin/env node
// Semantic diff of two .excalidraw.md files (ignores version bumps / re-measuring noise).
//   node diff.js <old.excalidraw.md> <new.excalidraw.md>
'use strict';
const { load, diffScenes } = require('./lib');
const [o, n] = process.argv.slice(2);
if (!o || !n) { console.error('usage: node diff.js <old> <new>'); process.exit(2); }
const d = diffScenes(load(o).data.elements, load(n).data.elements);
console.log(d.length ? d.join('\n') : 'no meaningful changes');
