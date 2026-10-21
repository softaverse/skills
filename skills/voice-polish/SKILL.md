---
name: voice-polish
description: Polish a spoken-voice recording (YouTube voiceover, podcast, narration, talking head) with an ffmpeg vocal channel strip — audition presets on a short sample, compare them at matched loudness, tweak EQ / compression / warmth by parameter, then even out tone and level differences between sections, process the full file and master it to a platform loudness target. Needs only ffmpeg and Python. Use when the user wants to clean up, enhance, warm up, deepen, or loudness-normalize a voice or 口播 audio file, or when parts of it are louder, quieter or sound different from the rest. Not for music mixing/mastering, pitch correction, or noise removal from heavily degraded audio.
---

# Voice Polish

`scripts/matcheq.py` first matches the tone of sections that sound like another mic or take, and `scripts/level.py` evens out section-to-section level jumps (takes or clips recorded at different levels); `scripts/ffchain.py` then runs a spoken-voice chain built from stock ffmpeg filters: high-pass → low shelf → mud bell → presence bell → air shelf → compressor → split-band de-esser → tanh saturation (2× oversampled), with eleven built-in presets.

## Requirements

`ffmpeg` (with the `acompressor`, `acrossover`, `aeval` and `allpass` filters — any recent build) and `python3`. `uv` only for `matcheq.py`, `level.py` and `analyze.py`. No build step, no model download.

## Workflow

Write all intermediate files to the scratchpad or an `output/` folder next to the input, never next to the source recording. Quote paths: recordings often have spaces in their names.

1. **Inspect** — `ffprobe` the file (duration, rate, channels, bit depth) and measure it with `ffmpeg -af ebur128=peak=true`. Note the integrated loudness: a quiet source (below about −24 LUFS) makes the compressor work harder and raises room noise. Then check whether tone and level hold across the file:

   ```bash
   uv run scripts/matcheq.py --check in.wav   # tone outliers: presence-to-body tilt per 5 s vs the file median
   uv run scripts/level.py --check in.wav     # speech loudness per 15 s window + spread
   ```

   A tone outlier (tilt more than 8 dB off the median) is a stretch recorded on another mic, off-axis or far away: at equal loudness it still sounds like a different take, and usually quieter. A level spread above 3 dB means sections sit at different levels — typical for a timeline cut from several takes or clips. Tell the user which stretches stand out and how, and fix them before processing (step 6). Long digital silences (`silencedetect=n=-90dB`) in the middle of a timeline are gaps worth pointing out, not something to fix.

2. **Cut a sample** — the first 10 s of speech: `ffmpeg -i in.wav -t 10 -c copy sample.wav` (add `-ss` if it opens with silence).

3. **Render candidates** — pick 3–5 presets from `scripts/ffchain.py --list` (details in [references/recipes.md](./references/recipes.md)) and render the sample with each:

   ```bash
   python3 scripts/ffchain.py sample.wav out/podcast-host.wav --preset podcast-host
   ```

4. **Compare fairly** — louder always sounds better, so gain-match before the user listens, and report tone with numbers:

   ```bash
   scripts/gainmatch.sh out/matched -16 out/a.wav out/b.wav out/c.wav   # also writes AB_all.wav
   uv run scripts/analyze.py out/a.wav out/b.wav out/c.wav
   ```

   Present a table (loudness, crest, centroid, band shares) and translate it into plain listening terms: thicker / clearer / more even / more natural. Point the user at `AB_all.wav` for back-to-back listening.

5. **Tweak** — map feedback ("too thin", "harsh", "deeper") to `--set` overrides on top of a preset using [references/recipes.md](./references/recipes.md); parameter IDs, units and ranges are in [references/parameters.md](./references/parameters.md). Render, gain-match, compare again. Change a few parameters at a time so the user can hear what each move does.

6. **Match, level, process the full file and master** — tone first, then level (matching shifts loudness), then the exact same `ffchain.py` command line as the sample, then master. Skip a fix step that step 1 did not call for:

   ```bash
   uv run scripts/matcheq.py in.wav matched.wav 193.0 227.0   # START END pairs printed by --check
   uv run scripts/level.py matched.wav leveled.wav -28          # slow gain riding, ±5 s window
   python3 scripts/ffchain.py leveled.wav processed.wav --preset youtube-deep-warm
   scripts/master.sh processed.wav "final_-14LUFS.wav" -14 -1   # YouTube: -14 LUFS, -1 dBTP
   ```

   Level to −28 LUFS whatever the final target: it keeps the speech near the level the presets were voiced at, and mastering sets the final loudness. `level.py` lists every stretch it lifted by 8 dB or more.

   Use −16 LUFS for podcasts. Verify the result: duration equals the source (so it stays in sync with video), integrated loudness within ±0.5 LU of target, true peak at or below the ceiling, `matcheq.py --check` finds no outliers and `level.py --check` spread is at or below 3 dB. Stretches that leveling lifted a lot (+8 dB or more) or matching boosted a lot also lift their room noise; name them so the user listens there, and say that a matched section only comes close to the main mic — another take or mic track of that stretch beats EQ.

## Rules

- You cannot hear the audio. Report measurements and what they usually mean, say plainly that you have not listened, and let the user judge.
- There is no reverb stage, so the output never gains echo; echo the user still hears is room sound in the recording (see the recipes table).
- The compressor rides syllables and phrases, not sections: mastering normalises the whole file once, so a quiet clip stays quiet unless `level.py` runs first, and a dull clip stays dull unless `matcheq.py` runs first.
- When the user still hears a difference after the checks pass, ask for timestamps rather than guessing.
- The presets were voiced on speech recorded around −30 LUFS. On much hotter or quieter material, adjust `compThresh` by the level difference before judging the tone.
- In zsh, a variable holding several `--set` flags is not word-split; put the flags in an array (`args=(--set a=1 --set b=2)` then `"${args[@]}"`).
- Do not raise loudness above the platform target: YouTube turns louder uploads down, so the extra level only costs dynamics.
