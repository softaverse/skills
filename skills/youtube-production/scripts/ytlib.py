"""Shared helpers for the youtube-production scripts (stdlib only).

Script format, text normalisation, transcript loading, and the local
alignment used to find every take of a script line in a raw recording.
"""

import json
import re
import unicodedata
from pathlib import Path

try:  # Whisper's zh output is often Simplified; convert when OpenCC is available.
    import opencc  # pip install opencc-python-reimplemented

    _S2T = opencc.OpenCC("s2twp")
except Exception:  # noqa: BLE001 - any import/config failure means "no conversion"
    _S2T = None

LINE_RE = re.compile(r"^\s*(?:[-*]\s*)?\**\[?(L\d{2,4})\]?\**\s*[|:：.\s]\s*(.+?)\s*$")
SECTION_RE = re.compile(r"^\s*#{2,3}\s+(.+?)\s*$")
DIRECTION_RE = re.compile(r"（[^）]*）|\([^)]*\)|\[[^\]]*\]|【[^】]*】")


def to_traditional(text):
    return _S2T.convert(text) if _S2T else text


def has_opencc():
    return _S2T is not None


# ── script ──────────────────────────────────────────────────────────────────


def parse_script(path):
    """Return [{id, section, text, spoken}] from script.md.

    A spoken line is `L01 句子` (also `- L01 | 句子`, `**L01** 句子`).
    Stage directions in （）/ () / [] / 【】 are kept in `text`, dropped from `spoken`.
    """
    lines, section = [], None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        m = SECTION_RE.match(raw)
        if m and not LINE_RE.match(raw):
            section = m.group(1)
            continue
        m = LINE_RE.match(raw)
        if m:
            text = m.group(2)
            spoken = DIRECTION_RE.sub("", text).strip()
            lines.append({"id": m.group(1), "section": section, "text": text, "spoken": spoken})
    ids = [l["id"] for l in lines]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise SystemExit(f"duplicate line ids in {path}: {sorted(dupes)}")
    return lines


def normalize(text):
    """Lowercase, Traditional, no punctuation/space: the string alignment compares."""
    text = unicodedata.normalize("NFKC", to_traditional(text)).lower()
    return "".join(ch for ch in text if unicodedata.category(ch)[0] in "LN")


# ── transcript ──────────────────────────────────────────────────────────────


def load_words(path):
    """Flat [{text, start, end}] from a flat word list or mlx_whisper/openai JSON."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [w for w in data if w.get("text", "").strip()]
    words = []
    for seg in data.get("segments", []):
        seg_words = seg.get("words") or []
        if seg_words:
            for w in seg_words:
                words.append({"text": w["word"].strip(), "start": w["start"], "end": w["end"]})
        else:  # no word timestamps: treat the segment as one word
            words.append({"text": seg["text"].strip(), "start": seg["start"], "end": seg["end"]})
    return [w for w in words if w["text"]]


def char_stream(words):
    """Explode words into normalised characters, each with an interpolated time.

    Returns (chars, times) where times[i] = (start, end) of chars[i].
    """
    chars, times = [], []
    for w in words:
        norm = normalize(w["text"])
        if not norm:
            continue
        step = (w["end"] - w["start"]) / len(norm)
        for k, ch in enumerate(norm):
            chars.append(ch)
            times.append((w["start"] + k * step, w["start"] + (k + 1) * step))
    return "".join(chars), times


# ── alignment ───────────────────────────────────────────────────────────────

MATCH, MISMATCH, GAP = 2, -1, -1


def local_hits(query, target, min_score=0.45, min_cover=0.3):
    """Every non-overlapping local alignment of `query` inside `target`.

    Smith-Waterman with start tracking. Returns hits sorted by position:
    [{t0, t1, q0, q1, score, cover}] where t0..t1 is the matched target span
    (end exclusive), score is normalised to 0..1 against a perfect match of the
    whole query, and cover is the fraction of the query the hit spans.
    """
    n, m = len(query), len(target)
    if not n or not m:
        return []
    prev = [0] * (n + 1)
    prev_start = [(0, 0)] * (n + 1)  # (t0, q0) where the path ending here began
    col_best = []  # per target position: (score, q_end, t0, q0)
    for j in range(1, m + 1):
        cur = [0] * (n + 1)
        cur_start = [(j, 0)] * (n + 1)
        tj = target[j - 1]
        best = (0, 0, j, 0)
        for i in range(1, n + 1):
            diag = prev[i - 1] + (MATCH if query[i - 1] == tj else MISMATCH)
            up = prev[i] + GAP
            left = cur[i - 1] + GAP
            s, start = 0, (j, i)
            if diag > s:
                s, start = diag, (prev_start[i - 1] if prev[i - 1] else (j - 1, i - 1))
            if up > s:
                s, start = up, prev_start[i]
            if left > s:
                s, start = left, cur_start[i - 1]
            cur[i], cur_start[i] = s, start
            if s > best[0]:
                best = (s, i, start[0], start[1])
        col_best.append(best)
        prev, prev_start = cur, cur_start

    perfect = MATCH * n
    radius = max(3, n // 2)
    cands = []
    for j, (s, q1, t0, q0) in enumerate(col_best):
        if s / perfect < min_score or (q1 - q0) / n < min_cover:
            continue
        lo, hi = max(0, j - radius), min(m, j + radius + 1)
        if s >= max(c[0] for c in col_best[lo:hi]):
            cands.append({"t0": t0, "t1": j + 1, "q0": q0, "q1": q1,
                          "score": round(s / perfect, 3), "cover": round((q1 - q0) / n, 3)})
    cands.sort(key=lambda h: -h["score"])
    hits = []
    for h in cands:
        if all(h["t1"] <= o["t0"] or h["t0"] >= o["t1"] for o in hits):
            hits.append(h)
    return sorted(hits, key=lambda h: h["t0"])


def best_hit(query, target):
    hits = local_hits(query, target, min_score=0.3, min_cover=0.2)
    return max(hits, key=lambda h: h["score"]) if hits else None


def fmt_time(t):
    m, s = divmod(max(0.0, t), 60)
    return f"{int(m):02d}:{s:05.2f}"


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump_json(obj, path):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
