# Recipes

## Presets

`python3 scripts/ffchain.py --list` prints these. All have no reverb.

| Preset | Character |
|---|---|
| `podcast-host` | clear, consistent; 250 Hz −3, 3 kHz +3, comp 5:1 |
| `audiobook-neutral` | lightest touch, keeps natural dynamics, brightest of the set, least body |
| `narration-warm` | warm documentary read; low shelf +2, saturation |
| `radio-voice` | big and warm; low shelf +3, comp 6:1, most saturation |
| `commercial-vo` | punchy and bright; presence +4, air +2, comp 6:1 |
| `gaming-streamer` | bright, energetic; presence +4, air +3 |
| `zoom-calls` | intelligibility first; HPF 120 Hz, thin |
| `clarity-boost` | cuts mud, adds presence, light compression |
| `gentle-polish` | light glue and air for a take that is already good |
| `youtube-deep-warm` | YouTube voiceover: deeper and warmer than `narration-warm`, still clear (see below) |
| `youtube-thick` | most body; heavier compression, can boom on phone speakers |

## YouTube voiceover (deep and warm)

`youtube-deep-warm` is built from published voiceover guidance (HPF 80–100 Hz, 1–2 dB cut at 200–300 Hz, 2–3 dB lift at 3–5 kHz, 3:1–4:1 compression, light de-essing) with extra low shelf for warmth: HPF 85, low shelf +3 dB at 150 Hz, −2 dB at 300 Hz, +2.5 dB at 3.5 kHz, compressor −26 dB 4:1 +7 dB, de-esser 55, saturation 25 / 30.

```bash
python3 scripts/ffchain.py in.wav out.wav --preset youtube-deep-warm
scripts/master.sh out.wav final.wav -14 -1
```

## Loudness targets

| Destination | Integrated | True peak |
|---|---|---|
| YouTube | −14 LUFS | ≤ −1 dBTP |
| Podcast apps | −16 LUFS | ≤ −1 dBTP |
| Fair A/B listening | any common value, e.g. −16 LUFS, plain gain only | — |

## Feedback → parameter moves

| The user says | Try |
|---|---|
| echo, roomy, distant | the chain adds no reverb, so it is room sound in the recording: lower `compRatio` / `compMakeup` (compression lifts the room tail) |
| thin, want deeper / thicker / warmer | `lowShelfFreq=150 lowShelfGain=3..6`, `hpFreq=60..80`; more density with `satDrive=35..45 satMix=40..50` |
| boomy, muddy, boxy | `lowMidFreq=250..350 lowMidGain=-2..-4`, raise `hpFreq` to 90–100, or lower `lowShelfGain` |
| dull, muffled, unclear | `presenceFreq=3000..4000 presenceGain=2..4`, `airGain=1..3` |
| harsh, piercing | lower `presenceGain` or `airGain` |
| sibilant "s" sounds | `deEssAmount=60..75`, `deEssThresh` lower (more negative), `deEssFreq` 5500–7500 |
| one section sounds different, muffled, far away, like another mic | tone, not level: `matcheq.py --check`, then match that section (see SKILL.md step 6) |
| one section louder / quieter than the rest | section-level difference, not dynamics: `level.py` before the chain (see SKILL.md step 6); the compressor cannot fix it |
| levels jump around | lower `compThresh` (more negative) or raise `compRatio` toward 5–6, then rebalance `compMakeup` |
| over-processed, squashed | `compRatio=3`, `compThresh` closer to −20, less `satDrive` |
| background noise, hiss | out of scope: no gate or denoiser here; denoise first (e.g. DeepFilterNet), then run the chain |

A genuinely lower voice (pitch or formant shift) is outside this chain; EQ and saturation only make the same voice sound fuller.
