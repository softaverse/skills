# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy", "soundfile", "pyloudnorm"]
# ///
"""Loudness, dynamics and tonal balance of one or more voice files.

  uv run analyze.py a.wav b.wav ...

Band values are each band's share of total energy in dB, so they compare tone
independently of how loud each file is. Lower centroid = darker / deeper.
"""
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import welch

BANDS = [("sub <80", 20, 80), ("body 80-250", 80, 250), ("mud 250-500", 250, 500),
         ("mid 500-2k", 500, 2000), ("presence 2-5k", 2000, 5000),
         ("sibilance 5-9k", 5000, 9000), ("air 9-16k", 9000, 16000)]

for path in sys.argv[1:]:
    y, sr = sf.read(path, always_2d=True)
    lufs = pyln.Meter(sr).integrated_loudness(y)
    mono = y.mean(axis=1)
    peak = 20 * np.log10(np.max(np.abs(y)))
    rms = 20 * np.log10(np.sqrt(np.mean(mono ** 2)))
    f, p = welch(mono, sr, nperseg=8192)
    total = p[(f >= 20) & (f <= 16000)].sum()
    centroid = (f * p).sum() / p.sum()
    print(f"\n{path.split('/')[-1]}  ({y.shape[1]} ch, {sr} Hz, {len(y) / sr:.1f} s)")
    print(f"  LUFS {lufs:6.1f} | peak {peak:5.1f} dBFS | crest {peak - rms:4.1f} dB | centroid {centroid:5.0f} Hz")
    print("  " + " | ".join(
        f"{name} {10 * np.log10(p[(f >= lo) & (f < hi)].sum() / total):5.1f}" for name, lo, hi in BANDS))
