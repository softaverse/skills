# Diagram types — when to use which, and how to draw it well

## Contents
1. Choosing (decision table)
2. flow — flowchart
3. swimlane — cross-functional process
4. layers — layered architecture
5. flow + groups — free-form architecture / context map
6. sequence — interactions over time
7. state — state machine
8. er — data model
9. tree / mindmap — hierarchy, breakdown
10. timeline — phases, roadmap
11. table — numbers, comparisons
12. Combining views

## 1. Choosing

Ask what question the reader has, then:

| Reader's question | Type | Spec |
|---|---|---|
| What are the steps, where does it branch or loop? | Flowchart | `diagram: flow` |
| Who does each step, where are the hand-offs? | Swimlane | `diagram: swimlane` |
| What are the parts of the system and how are they tiered? | Layered architecture | `diagram: layers` |
| Which services/contexts exist and who depends on whom? | Context map | `diagram: flow` + `groups`, `direction: LR` |
| In what order do parties call each other (and what comes back)? | Sequence | `diagram: sequence` |
| What statuses can X be in, and what moves it between them? | State machine | `diagram: state` |
| What data exists and how is it related? | ER / data model | `diagram: er` |
| How does it break down / what belongs under what? | Tree / mind map | `diagram: tree` / `mindmap` |
| When does what happen? | Timeline / roadmap | `diagram: timeline` |
| How do the numbers / options compare? | Table / matrix | `table` item |

Signals in the text: "如果…否則", "重試", "審核" → flow; several departments/roles → swimlane; "前端/後端/DB/第三方"
→ layers; "呼叫/回傳/callback/token" → sequence; "狀態/待付款/已出貨/取消" → state; "一對多/欄位/關聯" → er;
"Q1/里程碑/上線" → timeline; amounts, rates, plan A vs B → table.

## 2. flow — flowchart
- One `start` (ellipse) and one or more `end`; `decision` (diamond) for every question; `process` for actions.
- Decision text is a question ending in ？; every outgoing edge of a decision is labelled (是/否, 成功/失敗).
- `direction: "TB"` for ≤ ~8 steps in a line, `"LR"` when it's wide and shallow or has long text.
- Loops (retry, back to edit) are normal; label them ("否，重寄"). If a loop clutters, an `edgeRoute: "orthogonal"`
  or splitting the loop into a note can help.
- Highlight the happy path's last step with `success`, error/abort steps with `warning`.

## 3. swimlane — cross-functional process
- One lane per role/system (`lanes`), each node has `lane`. Columns follow the flow order automatically; force a
  column with `col` when two steps should line up.
- Hand-offs (edges that change lane) are the interesting part — label them if it's not obvious what is handed over.
- Keep lanes to ≤ 5; merge minor actors into one lane ("其他系統").

## 4. layers — layered architecture
- `layers` top→bottom = closest to the user → furthest (clients / edge / services / data / external).
- Node styles by kind: `ui` clients, `service` own services, `external` third-party (dashed), `datastore`, `queue`.
- Edges point in the direction of the call/dependency; label protocols only when they differ (REST, gRPC, webhook).
- Nodes are re-ordered inside a layer to reduce crossings (`keepOrder: true` to stop that). Same-layer edges
  that skip a neighbour are routed underneath automatically.

## 5. flow + groups — context map / free-form architecture
- `groups: [{id, label, nodes:[...]}]` draws a dashed box around members (bounded context, VPC, team, module).
- Use when tiers don't describe the system well (micro-services, integrations, event flows). `direction: "LR"`.
- Async edges (events, queues) `dashed: true`, sync calls solid.

## 6. sequence — interactions over time
- `participants` left→right in the order they first act (usually user → client → own services → external).
- Messages: `{from, to, text}`; responses `reply: true` (dashed); self-call `from === to`; `{note, over:[ids]}`
  for explanations; `{divider: "非同步"}` to separate phases. Optional `n` numbers the step.
- Keep message text short (verb + object); put payload detail in a note.

## 7. state — state machine
- Nodes are states (`state` style; `start` dot-like ellipse for the initial pseudo-state, `end` for terminal).
- Edges are transitions labelled with the trigger (and guard): "付款成功", "逾時 30 分 / 系統".
- `direction: "LR"` usually reads best. Terminal states (`已完成`, `已取消`) at the far right.

## 8. er — data model
- One node per entity, `style: "entity"` (left-aligned): first line the entity name, then key fields:
  `"Order\n─────\nid PK\nuser_id FK\nstatus\ntotal"`.
- Edge labels carry cardinality: "1 — N", "N — M"; `arrowhead: false` for plain relations.
- Show only the fields that matter for the question; link to the schema for the rest.

## 9. tree / mindmap
- `tree` = top→bottom hierarchy (org chart, feature breakdown); `mindmap` = left→right from a central topic.
- Root `highlight` or `system`; second level a category color; leaves `process`/`note`.
- More than ~3 levels or ~20 leaves → split into several trees.

## 10. timeline — phases, roadmap
- `items: [{date, text, style}]` in chronological order; they alternate above/below the axis.
- Mark the current/next milestone with `highlight`; done items can be `muted`.

## 11. table — numbers, comparisons
- Use a `table` item (see spec-format). Header row `header`, data rows a category color, totals `total`.
- Show the arithmetic in cells (`$1,000－28－263＝$709`), not just results — readers check numbers, and
  rounding (`12.5→13`) is often the point. Put assumptions in a `note` under the table.
- For option comparisons: options as columns, criteria as rows, verdict row last.

## 12. Combining views
A good diagram set for a feature is often: context/architecture (who's involved) → the main flow or sequence
(how it works) → a table of a concrete example (what the numbers are) → notes/open questions. Put each in its
own frame, stack them vertically with ~150px gaps, and keep colors consistent across frames (same color = same
kind of thing everywhere).
