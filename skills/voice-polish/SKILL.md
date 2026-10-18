---
name: voice-polish
description: Polish a spoken-voice recording (YouTube voiceover, podcast, narration, talking head) with an ffmpeg vocal channel strip — audition presets on a short sample, compare them at matched loudness, tweak EQ / compression / warmth by parameter, then process the full file and master it to a platform loudness target. Needs only ffmpeg and Python. Use when the user wants to clean up, enhance, warm up, deepen, or loudness-normalize a voice or 口播 audio file. Not for music mixing/mastering, pitch correction, or noise removal from heavily degraded audio.
---

# Voice Polish

`scripts/ffchain.py` runs a spoken-voice chain built from stock ffmpeg filters: high-pass → low shelf → mud bell → presence bell → air shelf → compressor → split-band de-esser → tanh saturation (2× oversampled), with eleven built-in presets.

## Requirements

`ffmpeg` (with the `acompressor`, `acrossover`, `aeval` and `allpass` filters — any recent build) and `python3`. `uv` only for `analyze.py`. No build step, no model download.

## Workflow

Write all intermediate files to the scratchpad or an `output/` folder next to the input, never next to the source recording. Quote paths: recordings often have spaces in their names.

1. **Inspect** — `ffprobe` the file (duration, rate, channels, bit depth) and measure it with `ffmpeg -af ebur128=peak=true`. Note the integrated loudness: a quiet source (below about −24 LUFS) makes the compressor work harder and raises room noise.

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

6. **Process the full file and master** — run the exact same command line on the full recording, then:

   ```bash
   scripts/master.sh processed.wav "final_-14LUFS.wav" -14 -1   # YouTube: -14 LUFS, -1 dBTP
   ```

   Use −16 LUFS for podcasts. Verify the result: duration equals the source (so it stays in sync with video), integrated loudness within ±0.5 LU of target, true peak at or below the ceiling.

## Rules

- You cannot hear the audio. Report measurements and what they usually mean, say plainly that you have not listened, and let the user judge.
- There is no reverb stage, so the output never gains echo; echo the user still hears is room sound in the recording (see the recipes table).
- The presets were voiced on speech recorded around −30 LUFS. On much hotter or quieter material, adjust `compThresh` by the level difference before judging the tone.
- In zsh, a variable holding several `--set` flags is not word-split; put the flags in an array (`args=(--set a=1 --set b=2)` then `"${args[@]}"`).
- Do not raise loudness above the platform target: YouTube turns louder uploads down, so the extra level only costs dynamics.
