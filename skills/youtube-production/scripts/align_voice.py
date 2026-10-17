#!/usr/bin/env python3
"""Place every script line on the final (already edited) voice track.

    align_voice.py <script.md> <transcript.json> <out-dir> [--audio voice.wav] [--min-score 0.4]

The voice is expected to be clean: fillers, pauses and retakes already cut by the user.
Each line gets exactly one span, chosen by a monotonic alignment over all candidate
matches (lines stay in script order and never overlap). Leftovers are reported, not fixed:

  missing     a line with no acceptable match (cut in the edit, or said very differently)
  reworded    matched, but the wording drifted (score < 0.6)
  partial     only part of the line was found (cover < 0.8)
  duplicate   the line matches well twice — a retake the edit may have left in
  unscripted  transcript stretches no line covers (ad-libs)

Writes:
  lines.json  {audio, duration, lines: [{id, start, end, score, cover, heard, flags}], unscripted}
  lines.md    review table
"""

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ytlib import char_stream, dump_json, fmt_time, load_words, local_hits, normalize, parse_script  # noqa: E402

MISSING_PENALTY = 0.35  # what skipping a line costs vs. accepting a weak match


def audio_duration(path):
    if not path:
        return None
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True)
    try:
        return round(float(out.stdout.strip()), 3)
    except ValueError:
        return None


def best_path(cands):
    """Pick ≤1 hit per line, in order, non-overlapping, maximising total score.

    cands[i] = list of hits for line i (each with t0, t1, score). Returns a list of
    index-or-None per line. DP over (line, chosen hit) with "skip" allowed.
    """
    # state: dict end_pos -> (total, choices)  — keep the best total per reachable end
    states = {0: (0.0, [])}
    for hits in cands:
        nxt = {}
        for end, (total, choices) in states.items():
            # skip this line
            key = end
            val = (total - MISSING_PENALTY, choices + [None])
            if key not in nxt or val[0] > nxt[key][0]:
                nxt[key] = val
            for k, h in enumerate(hits):
                if h["t0"] < end:
                    continue
                key = h["t1"]
                val = (total + h["score"], choices + [k])
                if key not in nxt or val[0] > nxt[key][0]:
                    nxt[key] = val
        # prune dominated states: a later end with a lower total is never better
        best, pruned = float("-inf"), {}
        for end in sorted(nxt):
            if nxt[end][0] > best:
                best = nxt[end][0]
                pruned[end] = nxt[end]
        states = pruned
    return max(states.values(), key=lambda s: s[0])[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("transcript")
    ap.add_argument("out_dir")
    ap.add_argument("--audio", help="the edited voice file the transcript came from")
    ap.add_argument("--min-score", type=float, default=0.4)
    args = ap.parse_args()

    lines = parse_script(args.script)
    target, times = char_stream(load_words(args.transcript))
    spoken = [(l, normalize(l["spoken"])) for l in lines]
    cands = [local_hits(q, target, min_score=args.min_score) if q else [] for _, q in spoken]
    picks = best_path(cands)

    used = [False] * len(target)
    out = []
    for (line, q), hits, k in zip(spoken, cands, picks):
        rec = {"id": line["id"], "section": line["section"], "text": line["text"], "flags": []}
        if not q:
            rec["flags"].append("no-spoken-text")
        if k is None:
            if q:
                rec["flags"].append("missing")
            out.append(rec)
            continue
        h = hits[k]
        for p in range(h["t0"], h["t1"]):
            used[p] = True
        rec.update({"start": round(times[h["t0"]][0], 3), "end": round(times[h["t1"] - 1][1], 3),
                    "score": h["score"], "cover": h["cover"], "heard": target[h["t0"]:h["t1"]]})
        if h["score"] < 0.6:
            rec["flags"].append("reworded")
        if h["cover"] < 0.8:
            rec["flags"].append("partial")
        others = [o for i, o in enumerate(hits) if i != k and o["score"] >= 0.75 and o["cover"] >= 0.8]
        if others:
            rec["flags"].append("duplicate")
            rec["duplicates"] = [round(times[o["t0"]][0], 3) for o in others]
        out.append(rec)

    unscripted, p = [], 0
    while p < len(target):
        if used[p]:
            p += 1
            continue
        q = p
        while q < len(target) and not used[q]:
            q += 1
        if q - p >= 4:
            unscripted.append({"start": round(times[p][0], 3), "end": round(times[q - 1][1], 3),
                               "heard": target[p:q]})
        p = q

    od = Path(args.out_dir)
    od.mkdir(parents=True, exist_ok=True)
    dur = audio_duration(args.audio) or (round(times[-1][1], 3) if times else 0)
    dump_json({"audio": args.audio, "transcript": args.transcript, "duration": dur,
               "lines": out, "unscripted": unscripted}, od / "lines.json")

    flag_names = {"missing": "❌ 找不到", "reworded": "⚠ 說法不同", "partial": "⚠ 只找到一部分",
                  "duplicate": "⚠ 疑似重講殘留", "no-spoken-text": "— 沒有口播稿"}
    md = ["# Line alignment", "", f"Audio: `{args.audio or '?'}` · {fmt_time(dur)}", "",
          "| Line | Start | End | Score | Heard | Flags |", "|---|---|---|---|---|---|"]
    for r in out:
        if "start" not in r:
            md.append(f"| {r['id']} | — | — | — | {r['text'][:30]} | {' '.join(flag_names[f] for f in r['flags'])} |")
            continue
        fl = [flag_names[f] for f in r["flags"]]
        if "duplicates" in r:
            fl.append("also at " + ", ".join(fmt_time(t) for t in r["duplicates"]))
        md.append(f"| {r['id']} | {fmt_time(r['start'])} | {fmt_time(r['end'])} | {r['score']:.2f} | "
                  f"{r['heard'][:30]} | {' '.join(fl)} |")
    if unscripted:
        md += ["", "## 稿子裡沒有的口播", "", "| Time | Heard |", "|---|---|"]
        md += [f"| {fmt_time(u['start'])}–{fmt_time(u['end'])} | {u['heard'][:60]} |" for u in unscripted]
    (od / "lines.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    counts = {f: sum(f in r["flags"] for r in out) for f in flag_names}
    print(f"{len(out)} lines · placed {sum('start' in r for r in out)} · "
          + " · ".join(f"{k} {v}" for k, v in counts.items() if v)
          + f" · unscripted {len(unscripted)} → {od}/lines.json, lines.md")


if __name__ == "__main__":
    main()
