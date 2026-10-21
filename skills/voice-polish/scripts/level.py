# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "soundfile"]
# ///
"""Slow speech leveler: ride gain so every stretch of speech sits at the same loudness.

  uv run level.py --check in.wav                       # loudness per 15 s window, spread
  uv run level.py in.wav out.wav [target_lufs=-28] [window_s=5]

Momentary loudness (ffmpeg ebur128, 400 ms, every 100 ms) -> speech frames only
(gated) -> local loudness over +-window_s -> gain to target, clamped, smoothed.
Pauses hold the gain of the neighbouring speech, so room noise is not pumped up.
Run it before ffchain.py: the compressor only rides peaks, not section-to-section
level jumps between takes or clips.
"""
import re
import subprocess
import sys

import numpy as np

GATE_ABS, GATE_REL = -50.0, -12.0      # speech = above -50 LUFS and within 12 LU of the local peak level
GAIN_MIN, GAIN_MAX = -10.0, 14.0
HOP = 0.1                              # ebur128 logs every 100 ms
SMOOTH_S = 1.5                         # moving average on the gain curve: no audible gain steps
CHECK_WINDOW_S = 15
BIG_LIFT_DB = 8.0
MERGE_S = 5.0


def fmt(sec):
    return f"{int(sec) // 60}:{int(sec) % 60:02d}"


def momentary(path):
    log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    M = np.array([float(m) for m in re.findall(r"\bM:\s*(-?[\d.]+)", log)])
    return M, HOP * (1 + np.arange(len(M)))


def speech_loudness(seg):
    """Energy mean of the gated speech frames in seg, or nan when there is no speech."""
    seg = seg[seg > GATE_ABS]
    if len(seg) < 5:
        return np.nan
    seg = seg[seg > seg.max() + GATE_REL]
    return 10 * np.log10(np.mean(10 ** (seg / 10)))


def check(path):
    M, t = momentary(path)
    levels = []
    for a in range(0, int(t[-1]), CHECK_WINDOW_S):
        L = speech_loudness(M[(t >= a) & (t < a + CHECK_WINDOW_S)])
        levels.append(L)
        print(f"  {fmt(a)}  " + ("   no speech" if np.isnan(L) else f"{L:6.1f} LUFS"))
    levels = np.array(levels)
    levels = levels[~np.isnan(levels)]
    spread = np.percentile(levels, 95) - np.percentile(levels, 5)
    print(f"check: speech level spread {spread:.1f} dB (5th-95th percentile of {CHECK_WINDOW_S} s windows)"
          + ("; level it first" if spread > 3 else ""))


def level(src, dst, target, win):
    import soundfile as sf

    M, t = momentary(src)
    half = int(win / HOP)
    local = np.array([speech_loudness(M[max(0, i - half):i + half + 1]) for i in range(len(M))])
    # Hold through gaps with no speech: carry the nearest known level.
    idx = np.arange(len(M)); ok = ~np.isnan(local)
    local = np.interp(idx, idx[ok], local[ok])
    gain = np.clip(target - local, GAIN_MIN, GAIN_MAX)
    k = int(SMOOTH_S / HOP)
    gain = np.convolve(np.pad(gain, k, mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), mode="valid")

    y, sr = sf.read(src, always_2d=True)
    ts = np.arange(len(y)) / sr
    g = 10 ** (np.interp(ts, t - 0.2, gain) / 20)   # an M frame covers the previous 400 ms
    sf.write(dst, y * g[:, None], sr, subtype="PCM_24")
    print(f"level: gain {gain.min():+.1f} .. {gain.max():+.1f} dB (median {np.median(gain):+.1f}) -> {dst}")
    # Big lifts raise room noise too: list them so the user listens there.
    # Stretches less than MERGE_S apart are reported as one.
    big = np.flatnonzero(gain >= BIG_LIFT_DB)
    runs = np.split(big, np.flatnonzero(np.diff(big) > MERGE_S / HOP) + 1) if len(big) else []
    for a, b in ((r[0], r[-1] + 1) for r in runs):
        print(f"  lifted {gain[a:b].max():+.1f} dB at {fmt(t[a])}-{fmt(t[b - 1])}: room noise rises with it")


if __name__ == "__main__":
    if sys.argv[1] == "--check":
        check(sys.argv[2])
    else:
        level(sys.argv[1], sys.argv[2],
              float(sys.argv[3]) if len(sys.argv) > 3 else -28.0,
              float(sys.argv[4]) if len(sys.argv) > 4 else 5.0)
