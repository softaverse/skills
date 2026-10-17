# Stage B — Retime & animate

Goal: replace every estimated length in the storyboard with the length measured from the
voice the user actually recorded, then build and hand over every animation at exactly that
length. **The voice is now the source of truth for time; the storyboard follows it, and the
animations follow the storyboard.**

Input: the voice track the user already edited in DaVinci — fillers, pauses and retakes cut,
nothing left to choose. Stage B never picks takes or edits audio.

```
B0 input ─ B1 transcribe ─ B2 align ─ B3 retime ─▶ ✋1 ─ B4 build (hf-studio gates ✋✋✋) ─ B5 instances + render plan ─▶ ✋ end of B
```

All scripts: `python3 <skill>/scripts/<name>.py` (usage in `scripts.md`).

---

## B0 — Input

- Ask for the voice track exported from DaVinci: **voice track only** (screen-recording audio
  muted), Deliver → Audio Only → WAV, whole timeline. Its timeline is the final edit's timeline.
- Keep the file where the user put it; write derived files to `<episode>/voice/`.
- Ask where the screen recordings are (needed for real frames in hf-studio's static storyboard).
- Confirm Stage A is done: `storyboard.json` exists and `storyboard.py check` has no errors.

## B1 — Transcribe

```bash
transcribe.py <voice.wav> <episode>/voice --script <episode>/script.md
```

- Model `small` by default (larger models are too heavy on this machine).
- Script terms go into Whisper's prompt. OpenCC converts Simplified output to Traditional —
  if `transcribe.py` says OpenCC is missing, alignment will miss lines; install it first.

## B2 — Align

```bash
align_voice.py <episode>/script.md <episode>/voice/transcript.json <episode>/voice --audio <voice.wav>
```

Read `voice/lines.md`. Every flag needs a decision — the voice is final, so the **script
follows the voice**, not the other way round:

| Flag | Usually means | Do |
|---|---|---|
| ❌ 找不到 | Line was cut in the edit, or said completely differently | Ask: cut → remove the line from its segment (or the segment); reworded → rewrite the line to what was said |
| ⚠ 說法不同 | Wording drifted | Rewrite the line to what was said (captions in Stage C use script text) |
| ⚠ 只找到一部分 | Part of the line was cut or merged | Trim the line to what was said |
| ⚠ 疑似重講殘留 | The edit left a retake in | Tell the user the time; they fix it in DaVinci and re-export, or confirm it is intentional |
| 稿子裡沒有的口播 | Ad-lib | Add it as a new line with an inserted id (`L78a`) in the right segment, or fold it into the ad-lib placeholder line |
| — 沒有口播稿 | A placeholder line such as「（即興：…）」 | Fine — `retime.py` gives it the unscripted time around it |

Never renumber existing line ids — insert (`L78a`, `L78b`). After editing `script.md`, re-run
B2 until only flags the user has accepted remain.

## B3 — Retime

```bash
retime.py <episode>                     # writes timing into storyboard.json, writes timing.md
storyboard.py check <episode>           # the picture mix is now measured from timing.dur
```

`retime.py` tiles the voice with segments (no gaps; each cut lands 0.2 s before the next
segment's first word), stores `timing.start / end / dur`, and times every overlay and zoom
from its `at` phrase. Read `timing.md`, then fix the storyboard where the real lengths broke
the plan:

| Report says | Fix |
|---|---|
| cutaway 太長 (> 20 s) | Split it (insert `Seg_19b`, move lines), or turn part of it into footage + overlays |
| cutaway 太短 (< 2 s) | Merge it with a neighbour, or make it an overlay on the footage |
| 長度差很多 on footage | Usually fine — check the asset list still covers the time (a 50 s screen segment needs 50 s of recording) |
| ❌ 整段都沒聽到 | The lines were cut: drop the segment, or move its picture to a neighbour |
| picture mix ✗ | Rebalance as in Stage A (footage first) |
| overlay / zoom not heard | Re-anchor `at` to a phrase that was said |

Segment ids are permanent from here on (renders are named after them): insert, don't renumber.
After any storyboard edit, re-run `retime.py` and `check`.

**✋ Checkpoint 1** — present: the `timing.md` table (est vs dur, flags), the script and
storyboard changes you made and why, and the measured picture mix. On ok, timing is frozen.

## B4 — Build the animations (hf-studio)

Read hf-studio's `CLAUDE.md` first — its three gates and rules govern every composition built
here, and the kit contract governs every `kit/…` piece. Run `render_plan.py <episode>` to list
what is not built yet. What needs building:

| Slot | Built at | Notes |
|---|---|---|
| `new` / `fork` with `reuse.as: "kit/<name>"` | `compositions/kit/<name>/` | Follow the kit contract; it must work in every theme, at `minDuration` and with every string at `max` |
| `new` / `fork` without `as` (custom) | `compositions/<episode>/<slot>` — `Seg_03` → `seg_03`, `Seg_06.o1` → `seg_06-o1` | Build it to the measured `timing.dur` (root `data-duration`), no word cues |
| episode `theme` missing from `assets/kit/themes.css` | a `.kit-theme-<name>` block | From the episode `DESIGN.md`; add the option to every kit manifest |
| `as-is` / `variables` | nothing to build | Kit pieces get `duration` + `theme` at render time; a fixed-length composition is trimmed / held in DaVinci (`render_plan` notes it) |

Batch the gates across all builds — one text storyboard for everything, then one round of
static storyboards, then the compositions:

1. **✋ Gate 1 — text storyboard**: per build, what is on screen, every variable with its `max`,
   and **which recipe moves each element** (from the slot's `motion`; hf-studio `recipes/`).
   No motion outside the recipes. A motion no recipe covers → stop and add a recipe first
   (define → build + demo → accept, per `recipes/README.md`), then continue.
2. **✋ Gate 2 — static storyboards**: `compositions/<path>/storyboard/index.html` per build.
   For overlays and footage-based pieces, use a real frame from the screen recording at that
   moment as the backdrop. For kit pieces, show each theme side by side.
3. **✋ Gate 3 — compositions**: build with the recipe implementations in `assets/kit/recipes.js`
   (timing and easing from the theme's motion tokens, never hard-coded), `npx hyperframes inspect`,
   `npm run check-seek -- <path>`, give the player URLs. Do not render.

When a slot's build is done, give that slot `vars` with its own content (a builder slot's copy
lives in its `elements` until then) so the render uses it.

## B5 — Instances and render plan

```bash
instances.py <episode>          # one composition per animation, this episode's content baked in
render_plan.py <episode>        # writes renders.sh + renders.md from those instances; runs nothing
```

`instances.py` writes `<episode>/<slot>` for every cutaway, transition and overlay (`Seg_06.o1` →
`seg_06-o1`): a copy of the component with the slot's vars — and, for kit pieces, the measured
`duration`, the episode `theme`, the overlay `placement` and `motion` overrides — set as the variable
defaults. Layout and motion are untouched, so an instance is as correct as the verified component,
with data `check` already validated; no AI work is needed. Custom builds already at the slot path
are updated in place; instances whose slot disappeared are removed. Instances are generated — edit
the storyboard or the component and re-run, never edit them. Re-run both scripts after any B3 re-run.

The user previews every animation in the Gallery (the episode folder) with its real copy, length and
theme, before anything is rendered. Final files render at 60 fps, 4K (exact 3× of 1280×720) into
`<episode>/renders/`: overlays as MOV (ProRes 4444 with alpha), cutaways and transitions as MP4 —
either all at once with `renders.sh`, or one by one from the player's Export (format / fps / 4K
selectors). Fixed-length legacy compositions are flagged in `renders.md` to trim or hold in DaVinci.

**✋ End of Stage B** — point the user at the Gallery to review the instances, then hand over
`renders.md` and `renders.sh`. Never render yourself. Stage C starts when the renders exist.
