# Spec format (apply.js)

One JSON object. Order of operations: `shift` → `origin` → `frame` → `add` (in order) → `edit` / `frameEdit`
→ `delete` → fit frame → overlap check.

## Contents
1. Top-level keys
2. `diagram` items (auto layout): flow / tree / mindmap / state / er · layers · swimlane · sequence · timeline
3. Manual items: box, text, arrow, table
4. Referring to existing elements (text queries)
5. edit, frameEdit, delete, shift
6. Examples

## 1. Top-level keys

| key | meaning |
|---|---|
| `create` | `true` → the file must not exist yet; a new drawing is created. |
| `expectHash` | (existing file) hash from `inspect.js`; apply refuses if the file changed since. |
| `origin` | `"below"` → under all current content (left-aligned, 150px gap; `{"below":true,"gap":200,"dx":0}` to tune). `{"x","y"}` absolute. Omitted → (0,0). All `add` coordinates are relative to it. |
| `frame` | `{"name": "…", "padding": 40}` new frame fitted around everything added (its name is the title). `{"into": "<name prefix>"}` add into an existing frame and grow it. |
| `styles` | extra named styles, e.g. `{"partner": {"stroke":"#087f5b","bg":"#e6fcf5"}}` |
| `add`, `edit`, `frameEdit`, `delete`, `shift` | below |

Several views in one spec: give each `diagram` its own `x`/`y` (they are relative to `origin`), or run one spec
per view with its own `frame` (simplest: each spec with `"origin": "below"`).

## 2. diagram items (auto layout)

Common fields: `diagram` (type), `x`, `y` (top-left, relative to origin), `title` (optional heading text above;
skip it when the frame name already says it), `fontSize` (default 20; sequence/timeline 18).

Node fields (everywhere): `id` (unique in the spec; usable by later manual arrows), `text`, `style` (default
`process`), optional `shape` (`rectangle|diamond|ellipse`), `w`, `h`, `minW`, `fontSize`, `dashed`, `align`.
Edge fields: `from`, `to`, `label`, `dashed`, `style` (uses its stroke color), `color`, `both: true` (double
arrowhead), `arrowhead: false` (plain line), `route: "orthogonal"`.

### flow (also `tree` = TB, `mindmap` = LR, `state`, `er` = LR + straight edges)
```json
{ "diagram": "flow", "direction": "TB", "nodesep": 60, "ranksep": 90, "edgeRoute": "curved",
  "nodes": [ {"id":"a","text":"填寫資料"}, {"id":"q","text":"資料正確？","style":"decision"}, {"id":"b","text":"送出","group":"be"} ],
  "edges": [ {"from":"a","to":"q"}, {"from":"q","to":"b","label":"是"}, {"from":"q","to":"a","label":"否"} ],
  "groups": [ {"id":"be","label":"後端處理","style":"group"} ] }
```
- `direction`: `TB | LR | BT | RL`. `edgeRoute`: `curved` (follows the layout engine's path, default),
  `straight` (side to side), `orthogonal` (right angles).
- `groups`: nodes join via `node.group` or `group.nodes: [...]`; drawn as dashed boxes with a label.
- `minlen` on an edge stretches it over more ranks.

### layers
```json
{ "diagram": "layers", "labelWidth": 180, "nodesep": 50, "layerGap": 50,
  "layers": [ {"id":"client","label":"Client"}, {"id":"svc","label":"Services"}, {"id":"data","label":"Data"} ],
  "nodes": [ {"id":"web","text":"Web","style":"ui","layer":"client"}, {"id":"api","text":"API","style":"service","layer":"svc"},
             {"id":"db","text":"PostgreSQL","style":"datastore","layer":"data"} ],
  "edges": [ {"from":"web","to":"api","label":"HTTPS"}, {"from":"api","to":"db"} ] }
```
Nodes join a layer via `node.layer` or `layer.nodes: [...]`. Order inside a layer is optimised to reduce
crossings (`"keepOrder": true` keeps yours). Several edges on one side of a box are spread apart.

### swimlane
```json
{ "diagram": "swimlane", "labelWidth": 170, "nodesep": 70, "edgeRoute": "orthogonal",
  "lanes": [ {"id":"c","label":"顧客"}, {"id":"s","label":"客服"} ],
  "nodes": [ {"id":"1","text":"提出申請","lane":"c"}, {"id":"2","text":"審核","lane":"s"}, {"id":"3","text":"通過？","lane":"s","style":"decision"} ],
  "edges": [ {"from":"1","to":"2"}, {"from":"2","to":"3"} ] }
```
Columns follow the flow automatically; `col: n` on a node forces its column.

### sequence
```json
{ "diagram": "sequence", "colWidth": 260, "step": 64,
  "participants": [ {"id":"u","text":"使用者","style":"actor"}, {"id":"api","text":"API","style":"service"} ],
  "messages": [ {"from":"u","to":"api","text":"POST /login"}, {"from":"api","to":"api","text":"驗證密碼"},
                {"note":"失敗 5 次鎖定","over":["u","api"]}, {"divider":"登入後"},
                {"from":"api","to":"u","text":"200 + token","reply":true} ] }
```
`reply: true` (or `dashed`) for responses; `from === to` self-call; `n` adds a step number; `color` per message.

### timeline
```json
{ "diagram": "timeline", "spacing": 260, "alternate": true,
  "items": [ {"date":"2026 Q1","text":"MVP"}, {"date":"2026 Q2","text":"金流","style":"highlight"} ] }
```

## 3. Manual items

### box
```json
{ "id": "legend", "text": "圖例\n藍：自有服務\n灰虛線：第三方", "x": 0, "y": 0, "w": 260, "h": 110, "style": "note",
  "shape": "rectangle", "fontSize": 18, "align": "left", "dashed": false, "square": false, "stroke": "#…", "bg": "#…" }
```
`w`/`h` omitted → sized from the text. No text → empty box (e.g. to frame other content; add a free text as its label).

### text
```json
{ "type": "text", "text": "⋮ 其餘同上", "x": 100, "y": 760, "fontSize": 20, "color": "#495057" }
```

### arrow
```json
{ "arrow": ["legend", {"find": "API"}], "label": "呼叫", "dashed": true, "color": "#0c8599",
  "fromSide": "right", "toSide": "left", "fromOffset": -20, "route": "orthogonal" }
```
Ends: a local `id` (including diagram node ids), a text query (→ the box containing that text), or `{"frame": "<prefix>"}`.
Sides are chosen automatically; `fromPoint`/`toPoint` (relative) or `fromPointAbs`/`toPointAbs` override.
`endArrowhead: null` plain line; `startArrowhead: "arrow"` double-headed.

### table
```json
{ "table": true, "x": 0, "y": 900, "fontSize": 18, "headerStyle": "header", "rowStyle": "cell",
  "columns": [ {"title": "方案", "w": 200}, "成本", "優點" ],
  "rows": [ { "cells": ["A", "$100", "便宜"], "style": "blue" },
            { "cells": ["B", {"text": "$300", "style": "highlight"}, "快"] },
            { "cells": ["結論", {"text": "選 A", "span": 1}, null], "style": "total", "h": 60 } ] }
```
Each cell is its own square box (stays editable). Column `w` omitted → fits content; rows auto-height.
`span: n` merges a cell down n rows (put `null` in the covered cells).

## 4. Text queries (existing elements)
Must match **exactly one** text element (else apply stops and lists candidates):
`{"find": "exact text"}`, `{"startsWith": "…"}`, `{"contains": "…"}`, plus `"within": {"x":[a,b], "y":[a,b]}`.
Multi-line text uses `\n`; copy exact strings from `inspect.js --texts` / `--grep`.

## 5. Changing existing content

**edit** — query + changes:
```json
{ "find": "待確認", "text": "已確認", "fontSize": 16, "color": "#0c8599",
  "style": "success", "stroke": "#…", "bg": "#…", "dashed": false,
  "dh": 30, "dw": 0, "resize": {"w": 400, "h": 120}, "moveBy": {"dx": 0, "dy": 170}, "moveTo": {"x": 0, "y": 0} }
```
`text`/`fontSize`/`color` change the text; `style`/`stroke`/`bg`/`dashed` restyle its container (box or arrow);
`dh`/`dw`/`resize` resize the container; `moveBy`/`moveTo` move box + text. Arrows attached to a moved or
resized box are re-attached automatically.

**frameEdit** — `{ "frame": "<prefix>", "name": "new name", "dh": 30 }`

**delete** — `{ "find": "…" }` removes the text and its box (an arrow label removes only the label);
`"keepContainer": true` keeps the box. Arrows bound to a deleted box lose that binding (reported).

**shift** — `{ "fromY": 5400, "dy": 320 }` (optional `"dx"`, `"x": [a,b]` range) moves everything whose top is
below `fromY`; runs before `add`. Use it to open space before growing a section that has others below it.

## 6. Examples

New file, two views:
```json
{ "create": true,
  "add": [
    { "diagram": "layers", "x": 0, "y": 0, "title": "系統架構", "layers": [...], "nodes": [...], "edges": [...] },
    { "diagram": "sequence", "x": 0, "y": 700, "title": "下單流程", "participants": [...], "messages": [...] } ] }
```

Append a framed view to an existing drawing:
```json
{ "expectHash": "…", "origin": "below", "frame": { "name": "訂單狀態" },
  "add": [ { "diagram": "state", "direction": "LR", "nodes": [...], "edges": [...] },
           { "text": "說明\n• 逾時 30 分自動取消", "x": 0, "y": 320, "w": 700, "h": 80, "style": "note" } ] }
```
(When a frame is used, read the diagram's printed size from apply's output to place notes below it, or
place them first and adjust after the preview.)
