# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy", "soundfile"]
# ///
"""Find sections whose tone differs from the rest of the file, and match them to it.

  uv run matcheq.py --check in.wav                         # list tone outliers
  uv run matcheq.py in.wav out.wav START END [START END ...]

A section recorded on another mic, off-axis or far away can sit at the same loudness
as the rest and still sound like a different take; level.py cannot fix that.
--check compares the presence-to-body tilt (2-5 kHz vs 100-500 Hz) of each 5 s
window with the file's median and reports stretches that deviate by more than 8 dB.
Matching takes the long-term speech spectrum of each section vs everything outside
the sections, smooths the difference to 1/3 octave, clamps it, and applies it as a
linear-phase FIR to that section only; edges snap to the quietest 50 ms within
+-1.5 s and crossfade over 50 ms. Run it before level.py.
"""
import sys

import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve, firwin2, welch

FRAME_S = 0.05
GATE_DB = 30.0                       # speech frames: within 30 dB of the loud frames
CHECK_WIN_S, CHECK_HOP_S = 5, 1
TILT_DEV_DB = 8.0
MERGE_GAP_S, MIN_RUN_S = 3, 5
BOOST_MAX, CUT_MAX = 15.0, -8.0
F_LO, F_HI = 70.0, 11000.0           # outside this, hold the edge value (no hiss / rumble lift)
TAPS = 4095
XFADE_S = 0.05
SNAP_S = 1.5


def fmt(sec):
    return f"{int(sec) // 60}:{int(sec) % 60:02d}"


def read_mono(path):
    y, sr = sf.read(path, always_2d=True)
    return y, y.mean(axis=1), sr


def speech_frames(x, hop, ref_db):
    fr = x[: len(x) // hop * hop].reshape(-1, hop)
    db = 10 * np.log10((fr ** 2).mean(axis=1) + 1e-12)
    return fr[db > ref_db - GATE_DB]


def loud_ref(mono, hop):
    fr = mono[: len(mono) // hop * hop].reshape(-1, hop)
    return np.percentile(10 * np.log10((fr ** 2).mean(axis=1) + 1e-12), 95)


def spectrum(frames, sr):
    f, p = welch(frames.ravel(), sr, nperseg=min(8192, frames.size))
    return f, p / p.sum()


def check(path):
    _, mono, sr = read_mono(path)
    hop = int(FRAME_S * sr)
    ref = loud_ref(mono, hop)
    tilt = []
    for a in range(0, int(len(mono) / sr) - CHECK_WIN_S + 1, CHECK_HOP_S):
        fr = speech_frames(mono[a * sr:(a + CHECK_WIN_S) * sr], hop, ref)
        if len(fr) < 20:                                       # under 1 s of speech
            tilt.append(np.nan); continue
        f, p = spectrum(fr, sr)
        tilt.append(10 * np.log10(p[(f >= 2000) & (f < 5000)].sum() / p[(f >= 100) & (f < 500)].sum()))
    tilt = np.array(tilt)
    dev = tilt - np.nanmedian(tilt)
    centre = np.arange(len(tilt)) * CHECK_HOP_S + CHECK_WIN_S / 2
    bad = np.flatnonzero(np.abs(np.nan_to_num(dev)) > TILT_DEV_DB)
    runs = np.split(bad, np.flatnonzero(np.diff(bad) > MERGE_GAP_S / CHECK_HOP_S) + 1) if len(bad) else []
    found = []
    for r in runs:
        # A window flags its centre; widen by half a window so the run covers the whole stretch.
        s, e = centre[r[0]] - CHECK_WIN_S / 2 + 1, centre[r[-1]] + CHECK_WIN_S / 2 - 1
        if e - s < MIN_RUN_S:
            continue
        d = np.nanmean(dev[r])
        found.append((s, e))
        print(f"  {fmt(s)}-{fmt(e)}  tilt {d:+.1f} dB vs file median: {'duller / more muffled' if d < 0 else 'brighter / thinner'}")
    print(f"check: {len(found)} tone outlier(s) (median tilt {np.nanmedian(tilt):.1f} dB, threshold ±{TILT_DEV_DB:.0f} dB)")
    if found:
        print("match: uv run matcheq.py in.wav matched.wav " + " ".join(f"{s:.1f} {e:.1f}" for s, e in found))


def match(src, dst, bounds):
    y, mono, sr = read_mono(src)
    hop = int(FRAME_S * sr)

    def quietest(t):
        a = max(0, int((t - SNAP_S) * sr) // hop)
        r = [np.mean(mono[(a + i) * hop:(a + i + 1) * hop] ** 2) for i in range(int(2 * SNAP_S / FRAME_S))]
        return (a + int(np.argmin(r))) * hop + hop // 2

    sections = [(quietest(s), quietest(e)) for s, e in zip(bounds[::2], bounds[1::2])]
    outside = np.ones(len(mono), bool)
    for s0, s1 in sections:
        outside[s0:s1] = False
    ref_db = loud_ref(mono, hop)
    f, p_ref = spectrum(speech_frames(mono[outside], hop, ref_db), sr)

    out = y.copy()
    n = int(XFADE_S * sr)
    for s0, s1 in sections:
        _, p_sec = spectrum(speech_frames(mono[s0:s1], hop, ref_db), sr)
        diff = np.zeros_like(f)
        for i, fc in enumerate(f[1:], 1):                       # 1/3-octave smoothing
            band = (f >= fc / 2 ** (1 / 6)) & (f <= fc * 2 ** (1 / 6))
            diff[i] = 10 * np.log10(p_ref[band].sum() / p_sec[band].sum())
        inside = (f >= F_LO) & (f <= F_HI)
        diff = np.interp(f, f[inside], diff[inside])
        diff -= np.average(diff[inside], weights=p_ref[inside])  # tone only; level.py handles loudness
        diff = np.clip(diff, CUT_MAX, BOOST_MAX)

        fir = firwin2(TAPS, f / (sr / 2), 10 ** (diff / 20))
        d, pad = TAPS // 2, int(0.5 * sr)
        a, b = max(0, s0 - pad), min(len(y), s1 + pad)
        seg = np.stack([fftconvolve(y[a:b, c], fir)[d:d + b - a] for c in range(y.shape[1])], axis=1)
        w = np.zeros(b - a)
        w[s0 - a:s1 - a] = 1
        w[s0 - a - n // 2:s0 - a + n // 2] = np.linspace(0, 1, n)
        w[s1 - a - n // 2:s1 - a + n // 2] = np.linspace(1, 0, n)
        out[a:b] = y[a:b] * (1 - w[:, None]) + seg * w[:, None]
        print(f"matcheq: {fmt(s0 / sr)}-{fmt(s1 / sr)} ({s0 / sr:.2f}-{s1 / sr:.2f} s): "
              + ", ".join(f"{fc if fc < 1000 else f'{fc / 1000:g}k'} {diff[np.argmin(abs(f - fc))]:+.1f}"
                          for fc in (100, 200, 400, 800, 1600, 3150, 5000, 8000, 10000)) + " dB")
        if diff.max() >= BOOST_MAX - 0.1:
            print("  boost hit the +15 dB clamp: the section is badly dull; another take or mic track will sound better",
                  file=sys.stderr)
    sf.write(dst, out, sr, subtype="PCM_24")
    print(f"matcheq: -> {dst}")


if __name__ == "__main__":
    if sys.argv[1] == "--check":
        check(sys.argv[2])
    else:
        bounds = [float(v) for v in sys.argv[3:]]
        if not bounds or len(bounds) % 2:
            sys.exit("matcheq: give START END pairs in seconds")
        match(sys.argv[1], sys.argv[2], bounds)
