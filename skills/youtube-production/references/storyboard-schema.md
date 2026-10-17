# storyboard.json

One file per episode. It records every visual decision; `animations.md` and `assets.md`
are generated from it (`scripts/storyboard.py lists`).

## Model

The storyboard mirrors the editing timeline:

- **Segments partition the script.** Every script line belongs to exactly one segment, in
  script order. A segment decides what fills the main picture while those lines are spoken.
- **Overlays sit on top of a segment.** Labels, lower-thirds, callouts — each anchored to a
  phrase inside the segment's lines.
- **Transitions sit between segments**, on the incoming one.

```
V3  overlays     ·········[label]··········[stat]·····
V2  cutaways     [section]        [flow diagram]
V1  picture      camera ── screen ─────────── camera ─
A1  voice        L01 L02 L03 L04 L05 L06 L07 L08 ...
```

## File

```json
{
  "episode": "EP4-stitch-shop",
  "title": "一個人 30 分鐘做出電商首頁",
  "style": "../DESIGN.md",
  "theme": "channel",
  "segments": [
    {
      "id": "Seg_01",
      "script": ["L01", "L02"],
      "picture": "cutaway",
      "visual": "步驟字卡：STEP 1 + 標題，右下英文浮水印",
      "animation": {
        "kind": { "layer": "cutaway", "purpose": ["section"] },
        "reuse": { "mode": "variables", "from": "kit/step-card", "why": "頻道的步驟字卡" },
        "vars": { "step": "STEP 1", "title": "做出第一版設計", "ghost": "STITCH" }
      },
      "timing": { "est": 9.1 }
    },
    {
      "id": "Seg_02",
      "script": ["L03"],
      "picture": "cutaway",
      "visual": "三個節點由左到右依序出現，虛線連接，最後一個節點亮起",
      "transition_in": { "mode": "as-is", "from": "flash-through-white", "dur": 0.5 },
      "animation": {
        "kind": { "layer": "cutaway", "purpose": ["flow"] },
        "reuse": { "mode": "fork", "from": "design-flow-overview", "why": "虛線流程合用，但只要第 ③④ 幕、四個節點改三個" },
        "elements": [
          { "type": "node", "label": "Google Stitch" },
          { "type": "node", "label": "Claude Code" },
          { "type": "node", "label": "Website" }
        ],
        "constraints": ["節點文字 ≤ 14 字元"]
      },
      "timing": { "est": 8.9 }
    },
    {
      "id": "Seg_03",
      "script": ["L04"],
      "picture": "screen",
      "visual": "Stitch 產出首頁的錄影，最後停在完成畫面",
      "assets": [{ "type": "screen", "what": "Stitch 從提示詞產出首頁，含捲動" }],
      "zooms": [{ "type": "zoom", "at": "按鈕", "target": "改成圓角的主要按鈕" }],
      "overlays": [
        {
          "id": "Seg_03.o1",
          "at": "CSS",
          "dur": 3,
          "placement": "bottom-left",
          "kind": { "layer": "overlay", "purpose": ["label"] },
          "reuse": { "mode": "variables", "from": "kit/label-chip", "why": "頻道的標註 chip" },
          "vars": { "text": "0 行 CSS", "sub": "全部交給 AI" }
        }
      ],
      "timing": { "est": 3.8 }
    }
  ]
}
```

## Fields

### Episode

| Field | Required | Notes |
|---|---|---|
| `episode` | yes | Folder name, `EP<n>-<slug>` |
| `title` | yes | Working title |
| `style` | no | Path to the style doc, relative to the episode folder. Default `../DESIGN.md`; point at `DESIGN.md` when the episode has its own |
| `theme` | no | Kit theme for every `kit/…` animation in the episode (`.kit-theme-<name>` in hf-studio `assets/kit/themes.css`). Default `channel` |
| `mix` | no | Override the picture budget: `{ "footage": [0.6, 0.7], "template": [0.2, 0.3], "custom": [0.05, 0.1] }` (the defaults) |
| `segments` | yes | In script order |

### Segment

| Field | Required | Notes |
|---|---|---|
| `id` | yes | `Seg_01`, `Seg_02`… Permanent once Stage B starts; insert as `Seg_02b`, never renumber |
| `script` | yes | Consecutive line ids from `script.md` (`L01`…; lines inserted later are `L78a`, `L78b`) |
| `picture` | yes | `camera` (speaker's face) · `screen` (screen recording) · `broll` (footage / stills) · `cutaway` (a full-frame animation replaces the picture) |
| `visual` | yes | One sentence on composition: what is where, what moves. Enough to judge without the animation |
| `animation` | if `picture` = `cutaway` | See *Animation* below; `kind.layer` must be `cutaway` |
| `overlays` | no | Animations on top of the picture; see *Overlay* |
| `transition_in` | no | An animation reference (`mode`, `from`, `dur`) with a `transition` layer. Omit for a hard cut — the default |
| `zooms` | no | Footage only. Done in the edit, not animated: `{ "type": "zoom" \| "highlight", "at": "<phrase>", "target": "<what to enlarge>" }`. Stage B adds `t` / `rel` |
| `assets` | no | What must be recorded or collected: `{ "type": "screen" \| "broll" \| "image" \| "logo" \| "audio", "what": "…" }` |
| `timing` | yes | Stage A: `{ "est": <s> }`, filled in by `storyboard.py check --write`. Stage B (`retime.py`) adds `start` / `end` / `dur` / `source` measured from the user's edited voice track, plus `flags` (`interpolated`, `not-heard`) — that `dur` is what the animation is rendered at |
| `notes` | no | Anything an editor needs that has no field |

`picture: camera` or `screen` segments without overlays are still listed — they are what
drives the asset list and tells the editor where no graphics go.

### Animation (cutaway, overlay, transition)

| Field | Required | Notes |
|---|---|---|
| `kind` | yes | `{ "layer": …, "purpose": [ … ] }` using the ids in hf-studio `kinds.json` |
| `reuse.mode` | yes | `as-is` — use unchanged · `variables` — same composition, new variable values · `fork` — copy and modify (structure fits, details don't) · `new` — build from scratch |
| `reuse.from` | unless `new` | Composition path relative to `compositions/`, e.g. `design-flow-overview`, `catalog/orbit-card` |
| `reuse.why` | yes | Why this one — or, for `new`, why nothing in the library fits |
| `reuse.ref` | no | For `new` / `fork`: other compositions to borrow motion or layout from |
| `reuse.as` | no | For `new` / `fork`: the composition path the build will create. Other slots may then use it as `from` with mode `variables` — build once, reuse. Generic pieces go in the kit (`kit/step-card`) and follow hf-studio's kit contract; episode-only pieces go in the episode folder (`EP4-x/hero`) |
| `vars` | `as-is` / `variables` | Keys must be variable ids in the source `manifest.json`. Only list values that change. For `kit/…` never set `duration` (Stage B fills it from the segment length) or `theme` (comes from the episode) |
| `motion` | `fork` / `new`; optional elsewhere | Recipes from hf-studio `recipes/` that move the elements, in order — one per element, chosen by the element's type (each recipe's `targets`: `eyebrow`, `title`, `sentence`, `keyword`, `cards`, `number`, `line`, `ghost`). Each item is a recipe id, or `{ "recipe": "card-stagger", "params": { "direction": "x", "speed": 1.2, "color": "danger" } }` to tune this use. Params are the recipe's own (its `params` frontmatter, with ranges) plus two every recipe has: `speed` (multiplier on the theme tempo, 0.5–2) and `color` (a theme token name or `#hex`; default is the theme's). On a kit slot, `motion` only overrides params of the recipes the kit already uses. The build uses these recipes and nothing else; a motion no recipe covers means a new recipe first |
| `elements` | `fork` / `new` | What is drawn: `{ "type": "node" \| "text" \| "icon" \| "image" \| "number" \| …, "label": "…" }`. Free-form but concrete |
| `cues` | no | Avoid. Cutaways are **duration-driven**: their inner timing scales with the segment length, so speech never has to land on a scene change. Word-timed emphasis goes in an overlay (`at`) or a cut. Kept only for overlays that must change mid-way: `{ "at": "<phrase>", "do": "…" }` |
| `constraints` | no | Limits the build must respect: text length, items per screen, transparency |

### Overlay

An animation plus where and when it sits:

| Field | Required | Notes |
|---|---|---|
| `id` | yes | `<segment id>.o1`, `.o2`… |
| `at` | yes | Phrase in the segment's lines where it enters |
| `dur` | yes | Seconds on screen (planned). Stage B writes `timing: { start, rel, dur }` — `rel` is seconds after the segment start, `dur` is capped at the segment end |
| `placement` | yes | `top-left` · `top-right` · `bottom-left` · `bottom-right` · `left-third` · `right-third` · `lower-third` · `center`. On `picture: camera`, keep it off the face |
| + Animation fields | yes | `kind.layer` must be `overlay` |

## Validation (`storyboard.py check`)

Errors (must fix):
- duplicate or malformed ids; unknown line ids; a line in no segment or in two; lines out of order
- `picture` not in the enum; `cutaway` without `animation`; `kind.layer` not matching its slot
- `zooms` on a cutaway, without a `target`, or with an `at` phrase not in the segment's lines
- purpose not in `kinds.json`; `reuse.mode` not in the enum; `from` missing for a non-`new` mode
- `from` that has no `manifest.json` (unless another slot builds it `as` that path); a `vars` key the manifest does not declare
- a string longer than the variable's `max` (kit components declare one); `duration` / `theme` in a kit's `vars`; a kit without the episode's `theme`
- two slots building the same `as`; an `as` that already exists; `as` on `as-is` / `variables`; a `fork` of a path this episode builds
- an overlay or cue `at` phrase that does not occur in its segment's lines
- a `motion` id with no `recipes/<id>/RECIPE.md`; a param the recipe doesn't declare; a value outside its range or options; a `color` that is neither a token name nor `#hex`

Warnings (judge):
- a `vars` text value much wider than the manifest default (width in em: CJK 1, Latin 0.55) — likely overflows
- the picture mix outside its targets (footage / template / custom share of running time)
- `new` animations (each one is real build time)
- the episode has its own `DESIGN.md` but reuses (`as-is` / `variables`) a composition drawn in another style
- `cues` on a cutaway or transition
- a custom `fork` / `new` (no `as`) without `motion`; a `motion` recipe that is not `accepted` yet
- a cutaway whose estimate is under 2 s or over 20 s
- overlays on `camera` segments placed `center`
