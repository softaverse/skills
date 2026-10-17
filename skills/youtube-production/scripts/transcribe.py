#!/usr/bin/env python3
"""Transcribe a recording with mlx_whisper, the engine behind obs-stt.

    transcribe.py <audio-or-video> <out-dir> [--script script.md] [--model small]
                  [--language zh] [--speed 1.0]

Writes into <out-dir>:
  whisper.json     raw mlx_whisper output (segments + word timestamps)
  transcript.json  flat [{text, start, end}] in seconds — the hf-studio transcript format
  transcript.txt   timestamped text for reading

With --script, proper nouns and Latin-script terms from the script go into
--initial-prompt, which helps Whisper spell them and keeps zh output Traditional.
--speed > 1 speeds the audio up with atempo first (obs-stt's trick); timestamps
are scaled back to the original timeline.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ytlib import dump_json, fmt_time, has_opencc, load_words, parse_script, to_traditional  # noqa: E402

MODELS = {
    "tiny": "mlx-community/whisper-tiny-mlx",
    "base": "mlx-community/whisper-base-mlx",
    "small": "mlx-community/whisper-small-mlx",
    "medium": "mlx-community/whisper-medium-mlx",
    "large-v3-turbo": "mlx-community/whisper-large-v3-turbo",
}
CANDIDATES = ["~/.pyenv/shims/mlx_whisper", "/opt/homebrew/bin/mlx_whisper", "/usr/local/bin/mlx_whisper"]


def find_whisper():
    found = shutil.which("mlx_whisper")
    if found:
        return found
    for c in CANDIDATES:
        p = os.path.expanduser(c)
        if os.access(p, os.X_OK):
            return p
    sys.exit("mlx_whisper not found — pip install mlx-whisper")


def prompt_from_script(path):
    """Terms Whisper tends to misspell: Latin-script words plus 「」-quoted names."""
    text = " ".join(l["spoken"] for l in parse_script(path))
    terms = re.findall(r"[A-Za-z][A-Za-z0-9.+#-]*(?:\s+[A-Z][A-Za-z0-9.+#-]*)*", text)
    terms += re.findall(r"「([^」]{1,12})」", text)
    seen, uniq = set(), []
    for t in terms:
        if t.lower() not in seen and len(t) > 1:
            seen.add(t.lower())
            uniq.append(t)
    # Whisper reads only the last ~224 tokens of the prompt.
    return "以下是繁體中文的影片口播，會提到：" + "、".join(uniq[:40]) + "。"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("media")
    ap.add_argument("out_dir")
    ap.add_argument("--script")
    ap.add_argument("--model", default="small")
    ap.add_argument("--language", default="zh")
    ap.add_argument("--speed", type=float, default=1.0)
    args = ap.parse_args()

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    model = MODELS.get(args.model, args.model)
    speed = min(2.0, max(0.5, args.speed))

    with tempfile.TemporaryDirectory() as work:
        wav = Path(work) / "audio.wav"
        filt = ["-filter:a", f"atempo={speed:.4f}"] if abs(speed - 1) > 1e-3 else []
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", args.media, "-vn", *filt,
                        "-ar", "16000", "-ac", "1", str(wav)], check=True)
        cmd = [find_whisper(), "--model", model, "--word-timestamps", "True",
               "--output-format", "json", "--output-dir", work, "--output-name", "whisper",
               "--verbose", "False", "--condition-on-previous-text", "False"]
        if args.language:
            cmd += ["--language", args.language]
        if args.script:
            prompt = prompt_from_script(args.script)
            cmd += ["--initial-prompt", prompt]
            print(f"initial prompt: {prompt}", file=sys.stderr)
        subprocess.run(cmd + [str(wav)], check=True)
        raw = json.loads((Path(work) / "whisper.json").read_text(encoding="utf-8"))

    if abs(speed - 1) > 1e-3:  # back to the original timeline
        for seg in raw.get("segments", []):
            seg["start"] *= speed
            seg["end"] *= speed
            for w in seg.get("words") or []:
                w["start"] *= speed
                w["end"] *= speed
    for seg in raw.get("segments", []):
        seg["text"] = to_traditional(seg["text"])
        for w in seg.get("words") or []:
            w["word"] = to_traditional(w["word"])

    dump_json(raw, out / "whisper.json")
    words = [{"text": w["text"], "start": round(w["start"], 3), "end": round(w["end"], 3)}
             for w in load_words(out / "whisper.json")]
    dump_json(words, out / "transcript.json")
    with open(out / "transcript.txt", "w", encoding="utf-8") as f:
        for seg in raw.get("segments", []):
            f.write(f"[{fmt_time(seg['start'])} → {fmt_time(seg['end'])}] {seg['text'].strip()}\n")
    note = "" if has_opencc() else " (OpenCC not installed: Simplified output stays Simplified)"
    print(f"wrote {out}/whisper.json, transcript.json, transcript.txt — {len(words)} words{note}")


if __name__ == "__main__":
    main()
