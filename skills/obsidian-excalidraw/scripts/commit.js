#!/usr/bin/env node
// Write a candidate produced by apply.js back over the real file — safely.
//
//   node commit.js <candidate.excalidraw.md>
//
// Reads <candidate>.changes.json for the target path and the hash the candidate was built from.
// Refuses if the target changed since then (the user edited it in Obsidian meanwhile).
// Backs up the current target, writes, re-loads to verify, and stores a snapshot so the next
// inspect.js can show what the user changed afterwards.
'use strict';
const fs = require('fs');
const path = require('path');
const { load, hashFile, BACKUP_DIR, SNAPSHOT_DIR, snapshotPathFor } = require('./lib');

const cand = process.argv[2];
if (!cand) { console.error('usage: node commit.js <candidate.excalidraw.md>'); process.exit(2); }
const meta = JSON.parse(fs.readFileSync(cand + '.changes.json', 'utf8'));
const target = meta.source;

if (meta.isNew) {
  if (fs.existsSync(target)) { console.error(`REFUSED: ${target} was created by someone else meanwhile. Inspect it and edit instead.`); process.exit(1); }
  fs.mkdirSync(path.dirname(target), { recursive: true });
  load(cand);
  fs.copyFileSync(cand, target);
  fs.mkdirSync(SNAPSHOT_DIR, { recursive: true });
  fs.copyFileSync(target, snapshotPathFor(target));
  console.log(`created:  ${target}\nelements: ${load(target).data.elements.filter((e) => !e.isDeleted).length} live`);
  process.exit(0);
}
const current = hashFile(target);
if (current !== meta.sourceHash) {
  console.error(`REFUSED: ${target} changed after the candidate was built (someone edited it).\n  built from ${meta.sourceHash}\n  now       ${current}\nRe-run inspect.js, rebuild the spec on the current content, apply again.`);
  process.exit(1);
}
const newDoc = load(cand); // must parse
fs.mkdirSync(BACKUP_DIR, { recursive: true });
fs.mkdirSync(SNAPSHOT_DIR, { recursive: true });
const stamp = new Date().toISOString().replace(/[:.]/g, '-');
const backup = path.join(BACKUP_DIR, `${path.basename(target)}.${stamp}.bak`);
fs.copyFileSync(target, backup);
fs.copyFileSync(cand, target);
const verify = load(target);
if (verify.hash !== newDoc.hash) { fs.copyFileSync(backup, target); console.error('REVERTED: written file did not verify; original restored from backup'); process.exit(1); }
fs.copyFileSync(target, snapshotPathFor(target));
console.log(`written:  ${target}`);
console.log(`elements: ${verify.data.elements.filter((e) => !e.isDeleted).length} live`);
console.log(`backup:   ${backup}`);
console.log(`restore:  cp "${backup}" "${target}"`);
