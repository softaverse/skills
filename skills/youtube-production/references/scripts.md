# Scripts

All Python 3, stdlib only (OpenCC — `pip install opencc-python-reimplemented` — is optional
and converts Whisper's Simplified output to Traditional before matching). Run with `python3 <skill>/scripts/<name>.py`. hf-studio is found
from `--studio`, then `HF_STUDIO`, then `~/Workspace/hyperframes/hf-studio`
(`storyboard.py` also walks up from the episode folder to the one holding `kinds.json`).

## Stage A

### `index_compositions.py` — search the animation library

```bash
index_compositions.py --layer cutaway --purpose flow            # by kind
index_compositions.py --layer overlay --purpose label --q 標註   # keywords rank, don't filter
index_compositions.py --source channel                          # only the channel's own
index_compositions.py --layer transition --q flash              # incl. Gallery "官方 Transitions"
index_compositions.py --untagged --q chart                      # also items with no kind
index_compositions.py ... --json                                # full records (thumb path, tags)
```

Ranking: kit (`compositions/kit/`) → channel compositions → library; within each, keyword hits → times reused in other episodes'
`storyboard.json` (`×2`) → path. `transition*` means the layer was inferred from the Gallery
tag, not declared in the manifest. Output per hit: path, kind, duration (root `data-duration`, or the `duration` variable's default for kit),
name, variable ids, description.

### `storyboard.py` — estimate, validate, derive

```bash
storyboard.py estimate <episode-dir>          # Markdown table: length per section + total
storyboard.py check <episode-dir> [--write]   # ✗ errors / ⚠ warnings; exit 1 on errors
storyboard.py lists <episode-dir>             # writes animations.md + assets.md
storyboard.py recipes [<episode-dir>]         # recipes per element type (target) — the menu for `motion`
```

- `estimate` counts a CJK character as 1, a Latin word as 1.2, a digit as 1, at 4.5 units/s,
  plus 0.3 s per line. Flags lines over 40 units.
- `check` rules are listed in `storyboard-schema.md`. It prints the picture-mix table
  (footage / template / custom share of running time, from `timing.dur` when measured, else
  `est`) before the warnings. `--write` stores `timing.est` per segment and reformats the JSON.
- `lists` writes `animations.md`: picture mix, the 分鏡總表 (every segment and overlay with its
  template, mode, recipes and param overrides, length), 配方說明 (the recipes used, with demo
  links once built), then the reuse / fork / new tables. `assets.md` adds a zoom list.
- Recipes are read from hf-studio `recipes/<id>/RECIPE.md` frontmatter (`name`, `status`,
  `role`, `targets`, `params`). The 配方說明 lists, for each recipe, the others that share a
  target (同類可替換). Repeated "not accepted yet" warnings collapse into one line.
- `lists` does not validate — run `check` first.

```bash
storyboard.py revisions <episode-dir> [--all]   # open change requests, resolved
```

- Per revision: the segment at `at` (from `timing`), every slot in it with its source and placement
  (overlays marked `← on screen` when they cover `at`), the script line (`voice/lines.json`) and the
  words said ±2 s (`voice/transcript.json`). `--all` includes `done` ones.

## Stage B

### `transcribe.py` — voice → transcript

```bash
transcribe.py <voice.wav> <out-dir> [--script script.md] [--model small] [--language zh] [--speed 1.0]
```

mlx_whisper (the engine behind obs-stt), `small` by default. With `--script`, Latin-script
terms and 「」 names go into `--initial-prompt`. `--speed` > 1 runs atempo first and scales
timestamps back. Writes `whisper.json` (raw), `transcript.json` (flat `[{text, start, end}]`,
the hf-studio transcript format) and `transcript.txt`. Converts to Traditional when OpenCC is installed.

### `align_voice.py` — place every script line on the voice

```bash
align_voice.py <script.md> <transcript.json> <out-dir> [--audio voice.wav] [--min-score 0.4]
```

Local alignment (Smith-Waterman) of each line against the transcript's characters, then a
monotonic choice over all candidates (lines in order, no overlap, a skipped line costs 0.35).
Writes `lines.json` (`start / end / score / cover / heard / flags` per line, plus unscripted
stretches) and `lines.md`. Flags: `missing`, `reworded` (score < 0.6), `partial` (cover < 0.8),
`duplicate` (a second good match — a retake left in), `no-spoken-text`. ~3 s for 110 lines / 15 min.

### `retime.py` — measured timing into the storyboard

```bash
retime.py <episode-dir> [--lines voice/lines.json] [--lead 0.2] [--dry-run]
```

Segments tile the voice (first starts at 0, last ends at the audio end, each cut `lead` s
before the next segment's first word). Unplaced lines are interpolated between neighbours:
scripted lines get their estimated length, an ad-lib placeholder line absorbs the rest.
Writes `timing.start / end / dur / source / flags` per segment, `timing` per overlay, `t / rel`
per zoom, and `timing.md` (est vs dur, flags, measured picture mix).

### `instances.py` — one composition per animation

```bash
instances.py <episode-dir> [--dry-run]
```

Copies each slot's source composition to `<episode>/<slot>` (`Seg_06.o1` → `seg_06-o1`) and bakes
the slot's content into the variable defaults (kit pieces also get `duration`, `theme`, `placement`,
`motion`). Relinks relative asset symlinks so copies one level deeper still find fonts. Custom builds
already at the slot path are updated in place; stale instances (manifest `instance`) are removed.
Prints one line per slot, noting values the component doesn't declare.

### `render_plan.py` — render commands, never run

```bash
render_plan.py <episode-dir> [--fps 60] [--resolution landscape-4k]
```

One command per cutaway / transition / overlay, rendering the slot's instance when it exists (no
variables needed); otherwise `reuse.from` / `reuse.as` / the custom build with the slot's vars (kit
pieces get `duration` + `theme`); overlays → MOV,
others → MP4, into `<episode>/renders/<slot>.<ext>`. Writes `renders.sh` and `renders.md`
(blocked: not built / no timing; notes: fixed-length compositions to trim or hold).

`--since <snapshot.json>` adds a 這輪要重匯 section to `renders.md` (and prints it): slots that
are new, whose render inputs changed (source, mode, vars, motion, placement, length, theme), or that
were removed. An overlay whose only change is its start (`rel`) is edit-only — move it in DaVinci.
Component changes (a kit fix) don't show in the storyboard; add those slots by hand.

### `ytlib.py`

Shared: script parsing (`L01` / `L01a` ids, `（）` directions dropped), normalisation
(NFKC, Traditional, letters and digits only), transcript loading, Smith-Waterman hits.
