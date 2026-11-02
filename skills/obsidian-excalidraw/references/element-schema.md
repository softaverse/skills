# Excalidraw element schema (for things the spec can't express)

Read this only when you need to create/modify elements directly with `scripts/lib.js`.

## File anatomy (.excalidraw.md, Obsidian Excalidraw plugin)

```
---
excalidraw-plugin: parsed
---
# Excalidraw Data
## Text Elements
<text> ^<textElementId>        ← one per text element, blank line between; the plugin reads this too
%%
## Drawing
```compressed-json             ← LZ-String compressToBase64 of the scene JSON, wrapped at 256 chars
...                              (some vaults use ```json uncompressed — lib.js handles both)
```
%%
```
Scene JSON: `{ type, version, source, elements: [...], appState: {...}, files: {...} }`.
`lib.serialize()` rebuilds the Text Elements section from the live text elements, so you never edit it by hand.

## Common fields (every element) — `Scene.base()` fills these
`id` (21 chars; text elements use 8 chars so the `^id` block ref is short), `type`, `x`, `y`, `width`,
`height`, `angle` 0, `strokeColor`, `backgroundColor`, `fillStyle` "solid", `strokeWidth` 2, `strokeStyle`
"solid"|"dashed"|"dotted", `roughness` 1, `opacity` 100, `groupIds` [], `frameId` null|frame id,
`index` (fractional order key), `roundness` null | {type:3} (rect) | {type:2} (arrow), `seed`, `version`,
`versionNonce`, `isDeleted`, `boundElements` [] , `updated` (ms), `link` null, `locked` false.

On every modification: `version++`, new `versionNonce`, `updated = now` (`Scene.bump`). Deletion is
`isDeleted: true` (keep the element; Obsidian syncs on versions).

## text
`text`, `rawText`, `originalText` (keep all three equal unless there are links), `fontSize`, `fontFamily` 5
(Excalifont; CJK falls back to Xiaolai), `textAlign` left|center|right, `verticalAlign` top|middle,
`containerId` (box or arrow id, or null), `autoResize` true, `lineHeight` 1.25.

## Binding rules (both directions, always)
- Text in a box: `text.containerId = box.id` **and** `box.boundElements` contains `{type:"text", id}`.
- Arrow between shapes: `arrow.startBinding = {elementId, focus: 0, gap: 5}`, same for `endBinding`, **and**
  each shape's `boundElements` contains `{type:"arrow", id: arrow.id}`.
- Arrow label: `label.containerId = arrow.id` and `arrow.boundElements` contains `{type:"text", id}`.
- When deleting a shape, remove it from others' `boundElements` and null arrow bindings to it (`Scene.remove`).

## arrow / line
`points` are **relative** to (x, y): `[[0,0],[dx,dy]]`; width/height = |dx|,|dy|. `startArrowhead` null,
`endArrowhead` "arrow"|"triangle"|"bar"|null, `elbowed` false, `lastCommittedPoint` null.

## frame
`type: "frame"`, `name` (rendered as the title above the frame), roundness null. Children set
`frameId`. Excalidraw clips children to the frame, so grow the frame when adding content (`Scene.fitFrame`).

## Fractional index
Order key strings, compared lexicographically (ASCII). New elements must sort after the current max:
`Scene.nextIndex()` appends `V` + two base62 chars to the current max (never ending in "0"). The plugin
re-normalizes indexes on its next save — that shows up as harmless noise in `inspect.js`.

## Using lib.js directly
Useful Scene methods: `box(text,x,y,w,h,style)` (style may set `shape: 'diamond'|'ellipse'`), `text()`,
`arrow(a,b,{label, via:[[x,y]…], route:'orthogonal', fromPoint, toPoint})` (a/b may be null for free arrows),
`line(points)`, `frame()`, `setText()`, `moveShape(el,dx,dy)` and `resize()` (both re-attach bound arrows via
`reroute(el)`), `remove()`, `fitFrame()`, `findText(query)`, `findFrame(prefix)`.
Layouts can be called directly too: `require('./layout').render({S, P:(x,y)=>[x,y], fid:null, ids:{}, style}, diagramSpec)`.

```js
const L = require('<skill-dir>/scripts/lib.js');
const doc = L.load(file);                // { data, hash, format, src }   — or L.create(file) for a new drawing
const S = new L.Scene(doc);
const e = S.push(S.base({ id: 'x'.repeat(21), type: 'ellipse', x: 0, y: 0, width: 120, height: 80, roundness: { type: 2 } }));
require('fs').writeFileSync(candidate, L.serialize(doc));
// then write <candidate>.changes.json like apply.js does ({source, sourceHash: doc.hash, added:[...], modified:[], deleted:[]})
// so preview.js --changes and commit.js work.
```
