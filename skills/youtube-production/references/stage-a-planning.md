# Stage A — Plan

Goal: a script and storyboard the user can record from, with every animation either
traced to an existing composition or explicitly justified as new. **No animation is built
or rendered in this stage, and no composition folder is created.**

Stage A has three checkpoints. Stop at each; continue only on the user's ok.

```
A0 setup ─ A1 brief ─ A2 outline ──▶ ✋1 ─ A3 script ──▶ ✋2 ─ A4 storyboard ──▶ ✋3 (end of A)
```

---

## A0 — Setup

1. Locate hf-studio (see SKILL.md). Read its `kinds.json`.
2. Pick the episode folder: list `compositions/EP*` and take the next number, slug from
   the topic (`EP4-stitch-shop`). Create only the folder and planning files.
3. **Channel style.** If `compositions/DESIGN.md` does not exist, bootstrap it once, before
   the outline:
   - Run `index_compositions.py --source channel` and pick 6–8 recent channel compositions
     across different purposes.
   - Read their `index.html` styles: fonts, colour values, backgrounds, corner radius,
     how text enters, typical durations, recurring layout (eyebrow + headline, cards, nodes).
   - Write `compositions/DESIGN.md`: palette with roles, type scale, layout grid and safe
     areas, motion language (eases, durations, entrance patterns), dos and don'ts, and a
     *Reference compositions* list naming the ones that best embody the style.
   - Show it to the user and get an ok. This is a one-time extra checkpoint.
4. **Episode style.** If this episode deviates from the channel style, write only the
   differences in `EP<n>-<slug>/DESIGN.md`, set `"style": "DESIGN.md"` and a `"theme"` in
   storyboard.json. If hf-studio's `assets/kit/themes.css` has no `.kit-theme-<name>` for it yet,
   list that as an open item — adding the theme is Stage B work.

## A1 — Brief

Required from the user:

| Field | What it must settle |
|---|---|
| Topic | What the video is about, in one line |
| Audience | Who watches and what they already know — decides how much to explain |
| Core point | The one sentence a viewer should leave with |
| What is built | The hands-on part: tools used, steps, what is shown on screen |
| Result | What exists at the end, and how it is shown |

Optional: target length (default 8–12 min), call to action, related earlier episodes.

Ask only for what is missing, at most 3 questions per round (`AskUserQuestion` when the
answer is a choice). Write `brief.md` with these headings.

## A2 — Outline

A build/tutorial episode usually follows:

| Part | Job | Typical length |
|---|---|---|
| Hook | Show the result first, then the promise. Viewers decide in the first 30 s | 20–40 s |
| Why | The problem or pain that makes this worth watching | 30–90 s |
| Steps | One section per step of the build; each opens with a section card | most of the video |
| Payoff | The finished result, demonstrated | 30–60 s |
| Recap + CTA | The core point again, then subscribe / link | 20–40 s |

Adapt it to the brief; don't force sections that have nothing to say. For each section in
`outline.md`: its goal, key message, what is on screen (camera / screen / animation), and an
estimated length. Total it against the target.

**✋ Checkpoint 1** — show the outline as a table (section · goal · on screen · length).
Ask: is the core point right, is anything missing or too long?

## A3 — Script

Write `script.md`:

```markdown
# EP4 一個人 30 分鐘做出電商首頁

## S1 Hook
L01 你有沒有想過，一個人也能做出完整的網站？
L02 今天我用 Google Stitch 跟 Claude Code，三十分鐘做出一個電商首頁。（畫面：成品首頁捲動）

## S2 流程
L03 整個流程只有三步：先在 Stitch 畫設計稿，再交給 Claude Code 寫程式，最後部署成網站。
```

Format rules (the Stage B aligner depends on them):
- Sections are `## <id> <name>`. If the user records one file per block (`3-1.mp4`), use the
  block number as the section id (`## 3-1 初始提示詞`) so recordings map to sections; otherwise `S1`, `S2`…
- If the user arrives with a finished script, convert it without rewording: keep their lines,
  fix only obvious typos, and list every change you made.
- One spoken line per row: `L01 <text>`. Ids are sequential and permanent once recording starts.
- Stage directions go in `（）` — they are dropped when matching the recording.
- Write what will be **said**: `三十分鐘` if that is how it is spoken, `30 分鐘` only if read as "thirty".

Writing rules:
- One idea per line, roughly 10–35 characters — one breath, 2–8 s. Long lines are hard to
  record in one take and give overlays nothing precise to anchor to.
- Spoken Chinese, not written: `然後`, `所以`, `你會發現`; avoid `此外`, `綜上所述`.
- Name tools exactly as the screen shows them (`Claude Code`, not `claude code`); these become
  the transcription hints in Stage B.
- Say the key term out loud where a label or zoom should appear (`這個叫 enhance-prompt`), so the
  overlay's `at` has a phrase to anchor to.

Estimate the length with `storyboard.py estimate` (≈ 4.5 spoken characters per second) and
report it per section and in total, against the outline.

**✋ Checkpoint 2** — show the script section by section with lengths. Ask for wording changes
before storyboarding; changing lines later means re-storyboarding.

## A4 — Storyboard

### 1. Segment the script

Group consecutive lines into segments and choose each segment's `picture`:

| Picture | Use for |
|---|---|
| `screen` | The demo — anything the viewer must see happen in the tool |
| `camera` | Opinions, personal story, direct address (only if this episode shows a face) |
| `cutaway` | Ideas that have no footage: section cards, flows, comparisons, lists, numbers, key statements |
| `broll` | Footage or stills of things that exist outside the screen |

**Picture budget** — share of running time, checked by `storyboard.py check`:

| Tier | Counts | Target |
|---|---|---|
| Footage | `screen` / `broll` / `camera` segments, including the overlays and zooms on them | 60–70% |
| Template | cutaways that reuse a composition (`as-is` / `variables`) or build a kit piece (`as`) | 20–30% |
| Custom | cutaways that `fork` or build `new` without `as` — one-off work | 5–10% |

Start from footage: if the thing is on screen in the demo, show the demo and carry the point
with a label overlay or a zoom. Spend cutaways on ideas that have no footage (section cards,
comparisons, numbers, the core statement), and spend the custom budget on the one or two
moments that matter most (usually the promise and the payoff). An episode can override the
targets with `"mix"` in storyboard.json.

Rhythm: change the picture every ~5–15 s; never hold a static cutaway past ~20 s.
Add overlays where a term, number, or name must stick (`label`, `stat`, `lower-third`), and
`zooms` where a detail on screen is too small to read (a button, a URL, a setting).

### 2. Find the animation for every slot

For each cutaway, overlay, and transition, search the library before inventing anything:

```bash
python3 <skill>/scripts/index_compositions.py --layer cutaway --purpose flow
python3 <skill>/scripts/index_compositions.py --layer overlay --purpose label --q 標註
```

Results are ranked **kit** components first (`compositions/kit/`: generic, length set by the
storyboard, themeable — the preferred choice), then the channel's own compositions (most reused
first), then library ones (official catalog, Herk, Remocn, snapcn, Remotion-inspired). For the top candidates, read
`manifest.json` (its variables are what `vars` can set) and look at the thumbnail
`<hf-studio>/.thumbs/<path>.jpg` when one exists.

Choose the mode:

| Mode | When |
|---|---|
| `as-is` | Content is literally the same (subscribe CTA, recurring transition) |
| `variables` | Structure, item count, and text lengths all fit; only values change |
| `fork` | Structure fits but counts or layout differ — or it is a library item that must be restyled to the channel's DESIGN.md |
| `new` | No composition with a matching structure exists. Name the closest ones in `reuse.ref` and say what they lack |

Most channel compositions are multi-act scenes written for one transcript, not templates:
their variables are that episode's copy, and their act count is fixed. Use them as
`variables` only when the act structure matches the lines; otherwise `fork` and say which
acts you keep. When a simple piece recurs (step card, label chip, centered statement, CTA
chip), plan it as a kit component — `reuse.as: "kit/<name>"` — and reuse it with `variables`
everywhere else. Kit components follow hf-studio's *Kit compositions* contract (length from
`duration`, `--kit-*` theme tokens, every string a variable with a `max`); that is how the
channel kit grows. Set the episode's `theme` in storyboard.json so kit pieces pick up its style.

If the episode has its own `DESIGN.md`, a composition drawn in another style is a `fork`
(restyle) unless it is themeable.

A library item may be used as `variables` only if it already matches the channel style;
otherwise it is a `fork`. Consistency across episodes beats novelty — prefer the channel
composition that is slightly less ideal over a library one that is slightly better.

### 3. Fill in the details

- `vars` with the real copy, within each variable's `max` (kit components declare one) or
  close to its default length.
- `elements` for `fork` / `new`: every node, label, number, icon that is drawn.
- No inner cues: a cutaway plays its acts across whatever length the segment ends up being.
  If something must land on a word, make it an overlay with `at`, or split the segment.
- Prefer `screen` + a label overlay over a cutaway whenever the thing being described is on
  screen anyway — the viewer sees the real tool, and the label carries the point.
- `constraints` the build must respect. Common ones:
  - text length per element (CJK reads as 1 em per character at 1280×720)
  - items per screen (≤ 5 list items, ≤ 4 flow nodes reads comfortably)
  - overlays render with transparency (MOV) — keep them self-contained, no full-frame background
  - on `camera` segments, overlays stay off the face
- `assets` for every `screen` / `broll` segment: what exactly to record or collect.

### 4. Validate and derive

```bash
python3 <skill>/scripts/storyboard.py check <episode-dir> --write   # fills timing.est, reports errors
python3 <skill>/scripts/storyboard.py lists <episode-dir>           # writes animations.md, assets.md
```

Fix every error; judge every warning (explain the ones you keep).

**✋ Checkpoint 3 (end of Stage A)** — present, in chat:
1. The segment table: id · lines · picture · animation (source + mode) · overlays · est.
2. The picture mix table from `check`, and workload: counts of `as-is` / `variables` /
   `fork` / `new`, and why each `new` exists.
3. The asset list to record.
4. Open questions (a line that needs a clearer phrase for an overlay, a doubtful match, a
   missing kit theme).

Do not dump the JSON. On ok, Stage A is done: the user records and edits the voice, and
Stage B starts when they bring the edited voice track.
