# Parameters

IDs for `--set id=value`, in plain units (dB, Hz, ms, 0–100 for percentages). A preset sets only some of these; the rest keep the default below. Out-of-range values are clamped. `python3 scripts/ffchain.py ... --print` shows the ffmpeg filter graph they produce.

Chain order: input gain → high-pass → low shelf → mud bell → presence bell → air shelf → compressor → makeup → de-esser → saturation → output gain.

| Stage | ID | Range | Default | ffmpeg filter |
|---|---|---|---|---|
| Gain | `inputGain`, `outputGain` | −24 … 24 dB | 0 | `volume` |
| High-pass | `hpFreq` | 20 … 400 Hz | 80 | `highpass`, 2-pole Butterworth |
| Low shelf | `lowShelfFreq` | 40 … 400 Hz | 120 | `lowshelf`, Q 0.707 |
| | `lowShelfGain` | −12 … 12 dB | 0 | |
| Mud bell | `lowMidFreq` | 100 … 1000 Hz | 300 | `equalizer` |
| | `lowMidGain` | −12 … 12 dB | 0 | |
| | `lowMidQ` | 0.3 … 4 | 0.9 | |
| Presence bell | `presenceFreq` | 1000 … 8000 Hz | 4000 | `equalizer` |
| | `presenceGain` | −12 … 12 dB | 0 | |
| | `presenceQ` | 0.3 … 4 | 0.7 | |
| Air shelf | `airFreq` | 6000 … 16000 Hz | 10000 | `highshelf`, Q 0.707 |
| | `airGain` | −6 … 12 dB | 0 | |
| Compressor | `compThresh` | −48 … 0 dB | −18 | `acompressor`, peak detection |
| | `compRatio` | 1 … 20 (1 = off) | 3 | |
| | `compAttack` | 0.1 … 100 ms | 10 | |
| | `compRelease` | 10 … 1000 ms | 120 | |
| | `compMakeup` | 0 … 24 dB | 0 | `volume` |
| De-esser | `deEssFreq` | 3000 … 12000 Hz | 6500 | `acrossover` LR4 split, `acompressor` on the high band |
| | `deEssThresh` | −48 … 0 dB | −24 | |
| | `deEssAmount` | 0 … 100 (0 = off) | 50 | ratio 1 / (1 − amount) |
| Saturation | `satDrive` | 0 … 100 | 20 | `aeval` tanh, drive maps to ×1 … ×16 pre-gain |
| | `satMix` | 0 … 100 (0 = off) | 30 | parallel blend |
| | `osQuality` | 0 off, 1 2×, 2 4× | 1 | `aresample` up/down + `allpass` |

Saturation is on by default (20 % drive, 30 % mix); set `satMix=0` for a fully clean chain.

## Fixed voicing

Constants in `ffchain.py` that the presets depend on; change them only deliberately.

- **EQ and high-pass** are RBJ cookbook biquads (`highpass`, `lowshelf`, `equalizer`, `highshelf` with `width_type=q`).
- **Compressor**: ffmpeg's envelope time constant is `ms / 4`. The main compressor runs attack ×5, release ×10 and a 14 dB knee, so it rides speech smoothly instead of grabbing single peaks.
- **De-esser**: 1 ms / 60 ms detector (ffmpeg attack 4 / release 240), hard knee. The crossover always runs, even at amount 0, so switching the de-esser off does not change the phase response.
- **Oversampling**: 2× via `aresample`, followed by a phase-only `allpass` (19.5 kHz at 48 kHz, scaled with sample rate, Q 1.7). The 4× setting has no allpass.
