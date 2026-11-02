#!/usr/bin/env node
// Render (part of) an .excalidraw.md file to PNG with Excalidraw's own renderer (@excalidraw/utils)
// in headless Chrome via Playwright — the same look as in Obsidian.
//
//   node preview.js <file.excalidraw.md> --out <png> [--changes <candidate>.changes.json] [--margin 250]
//                   [--frame <name prefix>] [--region x,y,w,h] [--all] [--max 3000]
//
// Default with --changes: the bounding box of everything added/modified, plus a margin of context.
'use strict';
const fs = require('fs');
const path = require('path');
const http = require('http');
const { load, bbox, intersects } = require('./lib');

const SKILL_DIR = path.resolve(__dirname, '..');
const a = process.argv.slice(2);
const flag = (n) => { const i = a.indexOf('--' + n); return i >= 0 ? a[i + 1] : undefined; };
const file = a[0];
const out = flag('out');
if (!file || !out) { console.error('usage: node preview.js <file> --out <png> [--changes c.json | --frame prefix | --region x,y,w,h | --all]'); process.exit(2); }

const doc = load(file);
const live = doc.data.elements.filter((e) => !e.isDeleted);
const byId = new Map(live.map((e) => [e.id, e]));

let region = null;
if (flag('region')) { const [x, y, w, h] = flag('region').split(',').map(Number); region = { x, y, w, h }; }
else if (flag('frame')) {
  const f = live.filter((e) => e.type === 'frame' && (e.name || '').startsWith(flag('frame')));
  if (f.length !== 1) { console.error(`frame prefix matched ${f.length} frames`); process.exit(1); }
  region = { ...bbox(f[0]) }; region.y -= 40; region.h += 40;
} else if (flag('changes')) {
  const ch = JSON.parse(fs.readFileSync(flag('changes'), 'utf8'));
  const ids = new Set([...ch.added, ...ch.modified]);
  const bs = live.filter((e) => ids.has(e.id) && e.type !== 'frame').map(bbox);
  if (!bs.length) { console.error('no added/modified elements to preview'); process.exit(1); }
  const m = Number(flag('margin') || 250);
  const x0 = Math.min(...bs.map((b) => b.x)) - m, y0 = Math.min(...bs.map((b) => b.y)) - m;
  region = { x: x0, y: y0, w: Math.max(...bs.map((b) => b.x + b.w)) + m - x0, h: Math.max(...bs.map((b) => b.y + b.h)) + m - y0 };
}

let els = live;
if (region && !a.includes('--all')) {
  const pick = new Set(live.filter((e) => e.type !== 'frame' && intersects(bbox(e), region)).map((e) => e.id));
  // keep containers/labels together
  for (const id of [...pick]) {
    const e = byId.get(id);
    if (e.containerId && byId.has(e.containerId)) pick.add(e.containerId);
    for (const b of e.boundElements || []) if (b.type === 'text' && byId.has(b.id)) pick.add(b.id);
  }
  // frames whose children are shown (renders frame outline + name)
  for (const e of live) if (e.type === 'frame' && intersects(bbox(e), region) && [...pick].some((id) => byId.get(id).frameId === e.id)) pick.add(e.id);
  els = live.filter((e) => pick.has(e.id));
}
if (!els.length) { console.error('nothing to render in that region'); process.exit(1); }

const MIME = { '.js': 'text/javascript', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.json': 'application/json', '.html': 'text/html' };
const server = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split('?')[0]);
  if (u === '/') { res.setHeader('content-type', 'text/html'); return res.end('<!doctype html><meta charset="utf-8"><body></body>'); }
  const p = path.join(SKILL_DIR, u);
  if (!p.startsWith(SKILL_DIR)) { res.statusCode = 403; return res.end(); }
  fs.readFile(p, (err, buf) => { if (err) { res.statusCode = 404; return res.end(); } res.setHeader('content-type', MIME[path.extname(p)] || 'application/octet-stream'); res.end(buf); });
});

server.listen(0, '127.0.0.1', async () => {
  const { chromium } = require(path.join(SKILL_DIR, 'node_modules', 'playwright'));
  let browser;
  try { browser = await chromium.launch({ channel: 'chrome', headless: true }); }
  catch (e1) {
    try { browser = await chromium.launch({ headless: true }); }
    catch (e2) { console.error('Could not start Chrome. Install Google Chrome, or run: npx playwright install chromium (in ' + SKILL_DIR + ')'); server.close(); process.exit(1); }
  }
  const timer = setTimeout(() => { console.error('preview timed out after 60s'); process.exit(1); }, 60000);
  try {
    const page = await browser.newPage();
    const base = `http://127.0.0.1:${server.address().port}`;
    await page.goto(base + '/');
    const max = Number(flag('max') || 3000);
    const b64 = await page.evaluate(async ({ els, files, max }) => {
      window.EXCALIDRAW_ASSET_PATH = location.origin + '/node_modules/@excalidraw/utils/dist/prod/';
      const m = await import('/node_modules/@excalidraw/utils/dist/prod/index.js');
      const blob = await m.exportScene({
        data: { elements: els, appState: { viewBackgroundColor: '#ffffff' }, files: files || {} },
        type: 'png',
        config: { padding: 24, canvasBackgroundColor: '#ffffff', scale: (w, h) => Math.min(1.5, max / Math.max(w, h)) },
      });
      const buf = new Uint8Array(await blob.arrayBuffer());
      let s = ''; for (let i = 0; i < buf.length; i += 0x8000) s += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000));
      return btoa(s);
    }, { els, files: doc.data.files, max });
    fs.writeFileSync(out, Buffer.from(b64, 'base64'));
    console.log(`preview: ${out} (${els.length} elements${region ? `, region x ${Math.round(region.x)} y ${Math.round(region.y)} ${Math.round(region.w)}×${Math.round(region.h)}` : ', whole drawing'})`);
  } catch (e) { console.error('preview failed: ' + e.message); process.exitCode = 1; }
  finally { clearTimeout(timer); await browser.close(); server.close(); }
});
