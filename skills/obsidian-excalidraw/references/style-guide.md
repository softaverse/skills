# Style guide

If the drawing already has its own conventions (colors per concept, fonts, lanes), follow the drawing —
consistency inside one file beats these defaults. Otherwise use the semantic styles, so the same kind of
thing looks the same everywhere.

## Semantic styles (scripts/styles.json)

| style | look | use for |
|---|---|---|
| `process` | blue box | a step / action (default node) |
| `decision` | yellow diamond | a question with labelled outgoing branches |
| `start` / `end` | green / red ellipse | start and terminal points |
| `actor` | white/gray box | a person or role, the user |
| `ui` | cyan box | front-ends: web, app, admin |
| `service` | blue box | your own services / modules |
| `system` | purple box | a whole system, or the central topic |
| `external` | gray dashed box | third-party / outside your control |
| `datastore` | green box | database, storage, cache |
| `queue` | orange box | queue, topic, event bus, scheduler |
| `entity` | white, left-aligned, 16px | ER entities with field lists |
| `state` | blue box | a state in a state machine |
| `milestone` | purple box | timeline items |
| `highlight` | pink box | the thing to look at (current milestone, changed part) |
| `success` | green box | happy-path result node, conclusions (add `"align": "left"` for multi-line callouts) |
| `warning` | red dashed box | error/abort nodes, risks, open questions ⚠ (add `"align": "left"` for multi-line callouts) |
| `note` | yellow, left-aligned | explanations, assumptions |
| `muted` | light gray | out of scope, done, "no data" |
| `group` | gray dashed outline | grouping around other boxes |
| `lane` / `layer` | light gray band | swimlanes / architecture tiers (used by the layouts) |
| `header` / `cell` / `total` | square cells | tables |

Plain colors for categories you define yourself: `gray blue cyan teal green yellow orange red pink purple violet`.
Pick one color per category and say what it means (a small legend box, or in the note) when it's not obvious.

Custom styles per spec: `"styles": {"partner": {"stroke": "#087f5b", "bg": "#e6fcf5"}}`.
Fields: `stroke`, `bg`, `dashed`, `square`, `shape` (`rectangle|diamond|ellipse`), `align`, `fontSize`, `textColor`, `strokeWidth`.

## Text
- Node text: short noun/verb phrase, ≤ ~3 lines; break lines yourself with `\n` at meaningful points.
- Sizes: 20 nodes, 18 dense nodes/tables/notes, 14 edge labels, frame names or 28 titles.
- Labels on edges only when they add information (conditions, protocol, amount, cardinality).
- Write in the user's language; keep technical names (API, Redis, merchant_id) as they are.

## Layout
- One idea per frame; frames stacked vertically ~150px apart, same left edge.
- Main reading direction: top→bottom for processes, left→right for pipelines/sequences/timelines.
- ≥ 40px between boxes; give labelled edges ≥ 100px of length.
- Notes and open questions go below or to the right of the diagram they explain, never on top of it.
