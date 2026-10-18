#!/usr/bin/env python3
"""Spoken-voice channel strip built from stock ffmpeg filters.

  ffchain.py --list
  ffchain.py <in.wav> <out.wav> [--preset NAME] [--set paramId=value ...] [--print]

Chain: high-pass -> low shelf / mud bell / presence bell / air shelf -> compressor
-> split-band de-esser -> tanh saturation (2x oversampled). There is no gate,
denoiser or reverb.

Writes 24-bit WAV with the input's sample rate, channel count and length.
"""
import argparse
import math
import subprocess
import sys

DEFAULTS = {
    "inputGain": 0.0, "outputGain": 0.0,
    "hpFreq": 80.0,
    "lowShelfFreq": 120.0, "lowShelfGain": 0.0,
    "lowMidFreq": 300.0, "lowMidGain": 0.0, "lowMidQ": 0.9,
    "presenceFreq": 4000.0, "presenceGain": 0.0, "presenceQ": 0.7,
    "airFreq": 10000.0, "airGain": 0.0,
    "compThresh": -18.0, "compRatio": 3.0, "compAttack": 10.0, "compRelease": 120.0,
    "compMakeup": 0.0,
    "deEssFreq": 6500.0, "deEssThresh": -24.0, "deEssAmount": 50.0,
    "satDrive": 20.0, "satMix": 30.0, "osQuality": 1.0,
}

RANGES = {
    "inputGain": (-24, 24), "outputGain": (-24, 24), "hpFreq": (20, 400),
    "lowShelfFreq": (40, 400), "lowShelfGain": (-12, 12),
    "lowMidFreq": (100, 1000), "lowMidGain": (-12, 12), "lowMidQ": (0.3, 4),
    "presenceFreq": (1000, 8000), "presenceGain": (-12, 12), "presenceQ": (0.3, 4),
    "airFreq": (6000, 16000), "airGain": (-6, 12),
    "compThresh": (-48, 0), "compRatio": (1, 20), "compAttack": (0.1, 100), "compRelease": (10, 1000),
    "compMakeup": (0, 24), "deEssFreq": (3000, 12000), "deEssThresh": (-48, 0), "deEssAmount": (0, 100),
    "satDrive": (0, 100), "satMix": (0, 100), "osQuality": (0, 2),
}

# Spoken-voice presets: (description, values that differ from DEFAULTS).
PRESETS = {
    "podcast-host": ("Clear, consistent podcast voice", dict(
        hpFreq=90, lowMidFreq=250, lowMidGain=-3, presenceFreq=3000, presenceGain=3,
        compThresh=-26, compRatio=5, compAttack=5, compMakeup=6, deEssAmount=60)),
    "audiobook-neutral": ("Lightest touch, keeps natural dynamics, brightest", dict(
        hpFreq=85, lowMidGain=-2, presenceGain=2, compThresh=-24, compRatio=4, compMakeup=5,
        deEssAmount=55)),
    "narration-warm": ("Warm documentary read", dict(
        hpFreq=75, lowShelfGain=2, presenceGain=2, compThresh=-22, compRatio=4, compMakeup=5,
        satDrive=25)),
    "radio-voice": ("Big, warm broadcast voice", dict(
        hpFreq=70, lowShelfGain=3, presenceGain=3, compThresh=-28, compRatio=6, compMakeup=8,
        satDrive=35, satMix=40)),
    "commercial-vo": ("Punchy, bright ad read", dict(
        hpFreq=90, presenceGain=4, airGain=2, compThresh=-28, compRatio=6, compMakeup=8, satDrive=25)),
    "gaming-streamer": ("Bright, energetic streamer mic", dict(
        hpFreq=95, presenceGain=4, airGain=3, compThresh=-28, compRatio=6, compMakeup=7,
        deEssAmount=55)),
    "zoom-calls": ("Intelligibility first; thin", dict(
        hpFreq=120, lowMidGain=-3, presenceGain=4, compThresh=-26, compRatio=6, compMakeup=6,
        deEssAmount=60)),
    "clarity-boost": ("Cuts mud, adds presence, little else", dict(
        hpFreq=90, lowMidFreq=280, lowMidGain=-3, presenceFreq=3200, presenceGain=3,
        compThresh=-18, compRatio=3, compMakeup=3)),
    "gentle-polish": ("Light glue and air for a take that is already good", dict(
        hpFreq=70, presenceGain=1.5, airGain=2, compThresh=-16, compRatio=2, compMakeup=2,
        deEssAmount=35)),
    "youtube-deep-warm": ("YouTube voiceover: deeper and warmer, still clear", dict(
        hpFreq=85, lowShelfFreq=150, lowShelfGain=3, lowMidFreq=300, lowMidGain=-2,
        presenceFreq=3500, presenceGain=2.5, compThresh=-26, compRatio=4, compMakeup=7,
        deEssAmount=55, satDrive=25)),
    "youtube-thick": ("Most body, heavier compression; can boom on phone speakers", dict(
        hpFreq=60, lowShelfFreq=150, lowShelfGain=5, presenceGain=3, compThresh=-28, compRatio=6,
        compMakeup=8, satDrive=35, satMix=40)),
}

# ffmpeg's compressor envelope coefficient is 1 / (ms * sr / 4000), i.e. a time
# constant of ms / 4, so the de-esser scales its times by 4 to get true time
# constants. The main compressor is voiced slower with a wide knee so it rides
# speech smoothly instead of grabbing individual peaks; the presets assume these.
DEESS_TIME_SCALE = 4.0
COMP_ATTACK_SCALE = 5.0
COMP_RELEASE_SCALE = 10.0
COMP_KNEE_DB = 14.0

# Phase-only voicing after 2x oversampling: an allpass that lags the highs like an
# IIR half-band oversampler (-11 deg at 6.5 kHz, -100 deg at 16 kHz at 48 kHz).
# Flat magnitude, so it does not change tone. Scales with the sample rate.
OVERSAMPLER_ALLPASS_HZ_AT_48K = 19500.0
OVERSAMPLER_ALLPASS_Q = 1.7


def db_to_lin(db):
    return 10.0 ** (db / 20.0)


def build_graph(p, sample_rate):
    """Return an ffmpeg -filter_complex graph from [0:a] to [out]."""
    chain = ["aformat=sample_fmts=dblp"]
    if p["inputGain"]:
        chain.append(f"volume={p['inputGain']}dB")

    # RBJ cookbook biquads.
    chain.append(f"highpass=f={p['hpFreq']}:poles=2:width_type=q:width={1 / math.sqrt(2):.8f}")
    if p["lowShelfGain"]:
        chain.append(f"lowshelf=f={p['lowShelfFreq']}:g={p['lowShelfGain']}:width_type=q:width=0.707")
    if p["lowMidGain"]:
        chain.append(f"equalizer=f={p['lowMidFreq']}:width_type=q:width={p['lowMidQ']}:g={p['lowMidGain']}")
    if p["presenceGain"]:
        chain.append(f"equalizer=f={p['presenceFreq']}:width_type=q:width={p['presenceQ']}:g={p['presenceGain']}")
    if p["airGain"]:
        chain.append(f"highshelf=f={p['airFreq']}:g={p['airGain']}:width_type=q:width=0.707")

    # Peak-detecting feed-forward compressor; ffmpeg's knee is a linear width.
    if p["compRatio"] > 1:
        chain.append(
            "acompressor="
            f"threshold={max(db_to_lin(p['compThresh']), 0.000976563):.6f}:ratio={p['compRatio']}"
            f":attack={p['compAttack'] * COMP_ATTACK_SCALE}:release={p['compRelease'] * COMP_RELEASE_SCALE}"
            f":knee={db_to_lin(COMP_KNEE_DB):.4f}:detection=peak:link=maximum")
    if p["compMakeup"]:
        chain.append(f"volume={p['compMakeup']}dB")

    graph = "[0:a]" + ",".join(chain)

    # Split-band de-esser: LR4 crossover, compress only the high band, sum back.
    # Reduces by (over * amount) above threshold, i.e. ratio 1 / (1 - amount), hard knee,
    # with a 1 ms / 60 ms envelope follower. The crossover always runs, so the phase
    # response does not jump when the de-esser is switched off.
    amount = min(p["deEssAmount"] / 100.0, 0.95)
    high = "[hi]anull[hic];"
    if amount > 0:
        high = (
            f"[hi]acompressor=threshold={db_to_lin(p['deEssThresh']):.6f}:ratio={1 / (1 - amount):.4f}"
            f":attack={1 * DEESS_TIME_SCALE}:release={60 * DEESS_TIME_SCALE}"
            ":knee=1:detection=peak:link=maximum[hic];"
        )
    graph += f",acrossover=split={p['deEssFreq']}:order=4th[lo][hi];{high}[lo][hic]amix=inputs=2:normalize=0"

    # tanh saturation, peak-compensated, parallel mix, inside the oversampler. The
    # oversampler runs whenever osQuality is on, even with no saturation.
    factor = {0: 1, 1: 2, 2: 4}[int(p["osQuality"])]
    if factor > 1:
        graph += f",aresample={sample_rate * factor}"
    mix = p["satMix"] / 100.0
    if mix > 0:
        pre = 1.0 + p["satDrive"] / 100.0 * 15.0
        wet = "val({ch})+{mix}*(tanh(val({ch})*{pre})/{norm}-val({ch}))"
        expr = "|".join(wet.format(ch=ch, mix=mix, pre=pre, norm=math.tanh(pre)) for ch in range(2))
        graph += f",aformat=channel_layouts=stereo,aeval='{expr}':c=same"
    if factor > 1:
        graph += f",aresample={sample_rate}"
    if factor == 2:
        hz = OVERSAMPLER_ALLPASS_HZ_AT_48K * sample_rate / 48000
        graph += f",allpass=f={hz:.0f}:width_type=q:width={OVERSAMPLER_ALLPASS_Q}:order=2"

    if p["outputGain"]:
        graph += f",volume={p['outputGain']}dB"
    return graph + "[out]"


def main():
    if sys.argv[1:] == ["--list"]:
        for name, (description, _) in PRESETS.items():
            print(f"{name:20} {description}")
        return

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--preset", choices=sorted(PRESETS), help="start from a preset (see --list)")
    ap.add_argument("--set", action="append", default=[], metavar="paramId=value",
                    help="override one parameter; repeatable")
    ap.add_argument("--print", action="store_true", help="print the filter graph")
    args = ap.parse_args()

    params = dict(DEFAULTS)
    if args.preset:
        params.update(PRESETS[args.preset][1])
    for item in args.set:
        key, _, value = item.partition("=")
        if key not in params or not value:
            sys.exit(f"ffchain: unsupported override {item!r} (parameters: {', '.join(DEFAULTS)})")
        lo, hi = RANGES[key]
        params[key] = min(max(float(value), lo), hi)

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=sample_rate,channels",
         "-of", "csv=p=0", args.input], capture_output=True, text=True, check=True)
    sample_rate, channels = (int(x) for x in probe.stdout.strip().split(","))

    graph = build_graph(params, sample_rate)
    if args.print:
        print(graph)
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", args.input, "-filter_complex", graph, "-map", "[out]",
         "-ac", str(channels), "-c:a", "pcm_s24le", args.output], check=True)
    print(f"ffchain: {args.preset or 'defaults'}"
          + "".join(f" {item}" for item in args.set) + f" -> {args.output}")


if __name__ == "__main__":
    main()
