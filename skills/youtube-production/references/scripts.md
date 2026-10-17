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
```

- `estimate` counts a CJK character as 1, a Latin word as 1.2, a digit as 1, at 4.5 units/s,
  plus 0.3 s per line. Flags lines over 40 units.
- `check` rules are listed in `storyboard-schema.md`. It prints the picture-mix table
  (footage / template / custom share of running time, from `timing.dur` when measured, else
  `est`) before the warnings. `--write` stores `timing.est` per segment and reformats the JSON.
- `lists` puts the mix table at the top of `animations.md` and a zoom list in `assets.md`.
- `lists` does not validate — run `check` first.

## Stage B (prototypes, not wired into the workflow yet)

- `transcribe.py` — mlx_whisper (`small` by default) with script-derived prompt → `transcript.json`
- `align_voice.py` — places every script line on the user's edited voice track → `lines.json`, `lines.md`
  (flags missing / reworded / partial lines, leftover retakes, unscripted stretches)
- `ytlib.py` — shared script parsing, normalisation, alignment
