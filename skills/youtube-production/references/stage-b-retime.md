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

---

## Revision round

Once the instances exist, the user reviews the episode and collects changes. They don't come one by
one: the user writes them into `storyboard.json` → `revisions` (`at` or `slot` + `ask`, schema in
`storyboard-schema.md`) — or says them in chat, and you write them there — then says 「處理修改」.
Until then only record: add the revision, run `storyboard.py revisions` to show where it lands,
discuss options if asked (e.g. which library piece fits), and write each answer into its `ask`.
Never touch `segments` or compositions before the round.

```
queue R01…Rn ─ 「處理修改」─ 1 snapshot ─ 2 resolve ─ ✋3 batch plan ─ 4 storyboard ─ 5 build C (✋✋) ─ 6 hand over
                                                                                      └─ follow-up tweaks (below)
```

1. **Snapshot**: `cp <episode>/storyboard.json <episode>/voice/storyboard.before.json`.
2. **Resolve**: `storyboard.py revisions <episode>` — segment, slots on screen, script line and the
   words said ±2 s for each `at`. Fill `target` and `type` (A data · B new slot, existing component ·
   C new/changed component · D voice/script).
   - When the timecode and the content disagree (the phrase the request is about is said elsewhere),
     say so **once**, with both times. The user's answer wins; don't ask again.
   - **Clips-only mode**: the user may say placement is theirs (「我會手動處理放置位置」). Then stop
     asking about position, length fit or what the clip covers; anchor each slot where the timecode
     or the content puts it (that only names the instance and its render) and note in `constraints`
     that the edit places it.
3. **✋ One plan for the batch**: per revision, the target, the type and the exact storyboard change.
   For C, this plan *is* hf-studio gate 1 for every build in the round: what is on screen, every
   variable with its `max`, which recipe moves each element. Prefer one kit component serving several
   revisions (R01 + R03 → `kit/terminal-type` with a `mode`) and extending an existing kit (a new
   variable) over a new one. A motion no recipe covers → extend or add the recipe first (define →
   implement + demo → accept, `recipes/README.md`); its demo is reviewed with gate 2. On ok, mark them
   `planned`.
4. **Apply A / B / C to the storyboard**: edit `segments` (new overlays get the next free `.o<n>`;
   C slots get `mode: new|fork` + `as`; a slot that uses a variable the kit doesn't declare yet fails
   `check` until gate 3 adds it — expected). D goes through *Re-recording a segment* below. Then
   `storyboard.py check` → `retime.py` (re-times overlays) → `storyboard.py lists`.
5. **Build C**: gate 2 ✋ (static storyboards, plus the recipe demo), gate 3 ✋ (compositions) —
   batched, one gate at a time. A changed kit keeps its old storyboard; write the new one next to it
   (`storyboard/<change>.html`). Verify as in *Checks* below.
6. **Hand over**: `instances.py <episode>`, then
   `render_plan.py <episode> --since <episode>/voice/storyboard.before.json`. Add slots whose
   component changed in step 5 (they aren't in the storyboard diff) — unless check-seek shows they're
   unchanged. Mark each revision `done` with its `result`; give the user the player URL of every
   changed instance and the 這輪要重匯 list. Never render.

### Follow-up tweaks

After a hand-over the user often reacts to one clip (「拉寬」「放更多字」「要滿版不透明」「不要分兩排」).
Each reaction is a new revision (`R04`, `R05`…, `slot` = that clip), handled right away, one at a time:

1. Snapshot, add the revision with `target` / `type`, `status: planned`.
2. A **new design** (another layout, a new component) still starts at gate 1 — propose it with
   concrete numbers and wait. A **tweak of what was just approved** (size, amount of text, timing,
   opaque vs transparent) is built directly: when the request is open-ended (「縮小但看得清楚」),
   pick the value yourself, try it, and look at the snapshot before reporting — don't ask.
3. Change the kit through new variables whose defaults keep the old behaviour, so every other
   instance stays identical; then edit the slot's `vars`, `instances.py`, verify, `done` +
   `render_plan --since`.
4. Report what changed, what you chose and why (with the fallback if it's not right, e.g. "drop the
   last section to get 19 px back"), and the one render to re-export.

Things these tweaks taught:
- **Full-frame opaque in an overlay slot**: fine for a short insert the edit puts on the top track.
  It must be opaque from frame 0 (only the content enters, no fade-in of the frame), has no fade-out
  (cutaway rule), and `render_plan` still says MOV — tell the user to pick MP4 in the player.
- **Long text at a fixed length**: show most of it with the frame and type only the tail
  (`typeLast`), instead of speeding type-on past readability.
- **Readable size**: the 1280×720 canvas renders at 4K and lands at 1080p ×1.5. Keep body text ≥ 15 px
  on the canvas (≈ 22 px at 1080p); when it won't fit, cut content rather than go smaller.

### Checks

For every changed kit and every instance in the round:
- `npx hyperframes check` (kit components and instances), `npm run check-seek -- <path>`.
- Snapshots of the cases the round actually uses, plus `minDuration`, every string at `max` and both
  themes. `snapshot` can't take variables: copy the composition to a sibling temp folder at the same
  depth (`compositions/kit/_tmp-x/`, so relative asset symlinks still resolve), change the declared
  defaults in `data-composition-variables`, snapshot, delete the copy.
- Regression: check-seek the other instances of every kit you changed (e.g. `seg_15` after a
  `grid-list` change) and the other slots of the same kit in this round.
- Small text on a new background clears 4.5:1 in both themes (`check` reports it); theme tokens meant
  for light backgrounds (`--kit-highlight`, `--kit-accent`, the caret) may fail on a dark one.

## Re-recording a segment

During the edit the user may re-record one segment's voice. There is no per-segment sync:
every script reads the whole voice track, so the new take goes through the DaVinci timeline and
B1–B3 run again on the whole file.

1. **The user swaps the take in DaVinci.** The new recording replaces the old one on the
   timeline, with fillers and pauses already cut. The rest of the timeline must stay untouched;
   any other trim changes that segment's length too, and it will show up in the comparison below.
2. **The user re-exports the whole voice track** (as in B0: voice only, WAV, whole timeline) and
   says which segment was re-recorded.
3. **Snapshot the current timing** before anything rewrites it:
   ```bash
   cp <episode>/storyboard.json <episode>/voice/storyboard.before.json
   ```
4. **Re-run B1 → B2 → B3** on the new file. In B2 the script still follows the voice: if the new
   take is worded differently, rewrite those lines in `script.md` under the same ids, and insert
   new ids (`L78a`) for added sentences. Never renumber.
5. **Compare the lengths.** Renders depend on each slot's `dur` (and an overlay's `rel` / `dur`),
   not on `start`, so only the slots whose values changed need a new render:
   ```bash
   python3 - <episode> <<'EOF'
   import json, sys
   ep = sys.argv[1]
   old = {s["id"]: s for s in json.load(open(f"{ep}/voice/storyboard.before.json"))["segments"]}
   for s in json.load(open(f"{ep}/storyboard.json"))["segments"]:
       o = old.get(s["id"], {})
       a, b = o.get("timing", {}).get("dur"), s["timing"].get("dur")
       if a is None or abs(a - b) > 0.01:
           print(f'{s["id"]}: {a} → {b}')
       oo = {x["id"]: x for x in o.get("overlays", [])}
       for x in s.get("overlays", []):
           t0, t1 = oo.get(x["id"], {}).get("timing", {}), x.get("timing", {})
           if any(abs((t0.get(k) or 0) - (t1.get(k) or 0)) > 0.01 for k in ("rel", "dur")):
               print(f'  {x["id"]}: rel {t0.get("rel")} → {t1.get("rel")}, dur {t0.get("dur")} → {t1.get("dur")}')
   EOF
   ```
   Expect the re-recorded segment and often **the segment before it**: each cut lands `lead`
   (0.2 s) before the next segment's first word, so a new take with a different lead-in moves the
   previous segment's end. Later segments only shift; their renders stay valid.
6. **Re-run B5** (`instances.py`, `render_plan.py`) and hand over the list from step 5: the user
   reviews those instances in the Gallery and re-exports only them from the player, not the whole
   `renders.sh`. If a changed length breaks a kit piece's `minDuration` or a custom build's fixed
   `data-duration`, fix the storyboard (B3) or rebuild that slot (B4) first.
