#!/usr/bin/env python3
"""Write measured timing into storyboard.json from the aligned voice track.

    retime.py <episode-dir> [--lines <dir>/lines.json] [--lead 0.2] [--dry-run]

Reads script.md, storyboard.json and lines.json (from align_voice.py; default
<episode-dir>/voice/lines.json). Segments tile the voice track with no gaps:

  - the first segment starts at 0, the last ends at the end of the audio;
  - a boundary sits `lead` seconds before the next segment's first word (never
    before the previous segment's last word), so the picture changes just ahead
    of the speech.

Lines align_voice.py could not place are interpolated between their neighbours,
weighted by spoken length, and the segment is flagged. Overlays and zooms get the
time their `at` phrase is spoken.

Writes into storyboard.json:
  segment.timing   {est, start, end, dur, source, flags?}
  overlay.timing   {start, rel, dur}      rel = seconds after the segment start
  zoom.t / zoom.rel
and <episode-dir>/timing.md — the review report (per-segment est vs dur, flags, picture mix).
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from storyboard import CHARS_PER_SEC, fmt_dur, mix_report, spoken_units  # noqa: E402
from ytlib import best_hit, char_stream, dump_json, fmt_time, load_json, load_words, normalize, parse_script  # noqa: E402


def line_times(lines, placed, total):
    """{line id: (start, end, interpolated?)} for every line, filling gaps."""
    ids = [l["id"] for l in lines]
    units = {l["id"]: max(spoken_units(l["spoken"]), 1) for l in lines}
    spoken = {l["id"]: bool(l["spoken"].strip()) for l in lines}
    out = {i: (placed[i]["start"], placed[i]["end"], False) for i in ids if i in placed}
    k = 0
    while k < len(ids):
        if ids[k] in out:
            k += 1
            continue
        j = k
        while j < len(ids) and ids[j] not in out:
            j += 1
        lo = out[ids[k - 1]][1] if k > 0 else 0.0
        hi = out[ids[j]][0] if j < len(ids) else total
        span = max(hi - lo, 0.0)
        run = ids[k:j]
        # Scripted lines get their estimated length; an ad-lib line (no spoken text, e.g.
        # 「（即興：…）」) absorbs whatever is left. Without one, scale everything to fit.
        est = {i: units[i] / CHARS_PER_SEC for i in run}
        adlib = [i for i in run if not spoken[i]]
        scripted = sum(est[i] for i in run if spoken[i])
        if adlib and scripted < span:
            share = {i: est[i] if spoken[i] else (span - scripted) / len(adlib) for i in run}
        else:
            weight = sum(est.values())
            share = {i: span * est[i] / weight for i in run}
        t = lo
        for i in run:
            out[i] = (round(t, 3), round(t + share[i], 3), True)
            t += share[i]
        k = j
    return out


def phrase_time(phrase, window, target, times):
    """Absolute time `phrase` starts inside the time window (start, end), or None."""
    lo, hi = window
    idx = [k for k, (s, _) in enumerate(times) if lo - 0.05 <= s <= hi + 0.05]
    if not idx:
        return None
    a, b = idx[0], idx[-1] + 1
    q = normalize(phrase)
    pos = target.find(q, a, b)
    if pos < 0:
        hit = best_hit(q, target[a:b])
        if not hit or hit["score"] < 0.5:
            return None
        pos = a + hit["t0"]
    return round(times[pos][0], 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--lines")
    ap.add_argument("--lead", type=float, default=0.2)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ep = Path(args.episode)
    lines_path = Path(args.lines) if args.lines else ep / "voice" / "lines.json"
    aligned = load_json(lines_path)
    script = parse_script(ep / "script.md")
    sb = load_json(ep / "storyboard.json")
    total = aligned["duration"]
    placed = {l["id"]: l for l in aligned["lines"] if "start" in l}
    lt = line_times(script, placed, total)
    target, times = char_stream(load_words(aligned["transcript"]))
    source = Path(aligned.get("audio") or lines_path).name

    segs = sb["segments"]
    firsts = [lt[s["script"][0]][0] for s in segs]
    lasts = [lt[s["script"][-1]][1] for s in segs]
    bounds = [0.0]
    for k in range(1, len(segs)):
        bounds.append(round(max(lasts[k - 1], firsts[k] - args.lead), 3))
    bounds.append(round(max(total, lasts[-1]), 3))

    problems = []
    for k, seg in enumerate(segs):
        start, end = bounds[k], bounds[k + 1]
        t = seg.setdefault("timing", {})
        t.update({"start": start, "end": end, "dur": round(end - start, 3), "source": source})
        flags = []
        if any(lt[i][2] for i in seg["script"]):
            flags.append("interpolated")
        missing = [i for i in seg["script"] if i not in placed]
        if missing and len(missing) == len(seg["script"]):
            flags.append("not-heard")
        if flags:
            t["flags"] = flags
        else:
            t.pop("flags", None)

        window = (lt[seg["script"][0]][0], lt[seg["script"][-1]][1])
        for ov in seg.get("overlays", []):
            at = phrase_time(ov["at"], window, target, times)
            if at is None:
                at = window[0]
                problems.append(f"{ov['id']}: '{ov['at']}' not heard — placed at the segment's first word")
            dur = round(min(ov.get("dur", 3), end - at), 3)
            ov["timing"] = {"start": at, "rel": round(at - start, 3), "dur": dur}
        for z in seg.get("zooms", []):
            at = phrase_time(z["at"], window, target, times)
            if at is None:
                at = window[0]
                problems.append(f"{seg['id']} zoom: '{z['at']}' not heard — placed at the segment's first word")
            z["t"], z["rel"] = at, round(at - start, 3)

    if not args.dry_run:
        dump_json(sb, ep / "storyboard.json")

    md = [f"# Timing — {sb.get('episode', ep.name)}", "",
          f"Voice: `{source}` · {fmt_time(total)} · {len(placed)}/{len(script)} lines heard", "",
          "| Seg | Lines | Picture | Start | Est | Dur | Δ | Flags |", "|---|---|---|---|---|---|---|---|"]
    flag_names = {"interpolated": "⚠ 有句子沒對到，時間是推估", "not-heard": "❌ 整段都沒聽到"}
    for seg in segs:
        t = seg["timing"]
        est, dur = t.get("est", 0), t["dur"]
        delta = dur - est
        notes = [flag_names[f] for f in t.get("flags", [])]
        if est and abs(delta) > max(2.0, 0.4 * est):
            notes.append("長度差很多")
        if seg["picture"] == "cutaway" and not 2 <= dur <= 20:
            notes.append("cutaway 太短" if dur < 2 else "cutaway 太長")
        ids = seg["script"]
        span = ids[0] if len(ids) == 1 else f"{ids[0]}–{ids[-1]}"
        md.append(f"| {seg['id']} | {span} | {seg['picture']} | {fmt_time(t['start'])} | {est:.1f} | "
                  f"{dur:.1f} | {delta:+.1f} | {' '.join(notes)} |")
    table, off = mix_report(sb)
    md += ["", "## Picture mix（實測）", "", *table]
    if problems:
        md += ["", "## Overlay / zoom", ""] + [f"- {p}" for p in problems]
    (ep / "timing.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    est_total = sum(s["timing"].get("est", 0) for s in segs)
    print(f"{len(segs)} segments · voice {fmt_dur(total)} (est {fmt_dur(est_total)}) · "
          f"{sum(1 for s in segs if s['timing'].get('flags'))} flagged · {len(problems)} overlay/zoom problems"
          f"{' · dry run' if args.dry_run else ' → storyboard.json'}, timing.md")
    for o in off:
        print(f"⚠ picture mix: {o}")


if __name__ == "__main__":
    main()
