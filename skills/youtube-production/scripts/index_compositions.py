#!/usr/bin/env python3
"""Search hf-studio's compositions by kind, keyword, and source.

    index_compositions.py [--layer cutaway] [--purpose flow ...] [--q 關鍵字 ...]
                          [--source channel|library|all] [--untagged] [--limit 15] [--json]
                          [--studio <hf-studio>]

One line per composition, ranked: kit, then channel, then library compositions, then by
how many episode storyboards already reuse it, then by keyword hits.

  [channel ×2] design-flow-overview  cutaway/flow  12s  沒有設計師，怎麼產出網站風格
      vars: eyebrow headline n1 n2 n3 n4 …
      ↳ description (first 120 chars)

"kit" = generic duration-driven, themeable components (compositions/kit/), ranked first;
"channel" = authored for this channel (top level of compositions/ and EP*/ folders);
"library" = imported (catalog, catalog-components, herk-*, remocn, snapcn, remotion-inspired).
Untagged compositions (no manifest "kind") are skipped unless --untagged — except those
in the Gallery's 官方 Transitions tag, which count as layer "transition" (shown as transition*).
--q keywords rank matches higher; they don't filter.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

TRANSITION_TAG = "官方 Transitions"
LIBRARY_ROOTS = ("catalog", "catalog-components", "remocn", "snapcn", "remotion-inspired")
ROOT_TAG_RE = re.compile(r"<[a-z]+\b[^>]*\bdata-composition-id=[^>]*>", re.S)
DURATION_RE = re.compile(r'data-duration="([\d.]+)"')


def studio_path(arg):
    p = Path(os.path.expanduser(arg or os.environ.get("HF_STUDIO") or "~/Workspace/hyperframes/hf-studio"))
    if not (p / "compositions").is_dir():
        sys.exit(f"hf-studio not found at {p} — pass --studio or set HF_STUDIO")
    return p


def source_of(rel):
    top = rel.split("/")[0]
    if top == "kit":
        return "kit"
    return "library" if top in LIBRARY_ROOTS or top.startswith("herk-") else "channel"


def duration_of(index_html):
    try:
        html = index_html.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    root = ROOT_TAG_RE.search(html)
    m = DURATION_RE.search(root.group(0)) if root else None
    return float(m.group(1)) if m else None


def usage_counts(comps):
    """How many episode storyboards reference each composition path."""
    counts = {}
    for sb in comps.glob("EP*/storyboard.json"):
        try:
            data = json.loads(sb.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        used = set()
        for seg in data.get("segments", []):
            for anim in [seg.get("animation"), seg.get("transition_in"), *seg.get("overlays", [])]:
                if not anim:
                    continue
                src = (anim.get("reuse") or {}).get("from") or anim.get("from")
                if src:
                    used.add(src)
        for src in used:
            counts[src] = counts.get(src, 0) + 1
    return counts


def gallery_tags(studio):
    """{composition path: [tag name, …]} from hf-studio's gallery.json."""
    try:
        g = json.loads((studio / "gallery.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    names = {t["id"]: t["name"] for t in g.get("tags", [])}
    return {path: [names.get(t, t) for t in ids] for path, ids in g.get("assign", {}).items()}


def load_index(studio):
    comps = studio / "compositions"
    usage = usage_counts(comps)
    tags = gallery_tags(studio)
    items = []
    for mf in comps.glob("**/manifest.json"):
        rel = mf.parent.relative_to(comps).as_posix()
        if "/storyboard" in f"/{rel}" or "/." in f"/{rel}":
            continue
        try:
            m = json.loads(mf.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        kind = m.get("kind") or {}
        purpose = kind.get("purpose") or []
        if isinstance(purpose, str):
            purpose = [purpose]
        layer, inferred = kind.get("layer"), False
        if layer is None and TRANSITION_TAG in tags.get(rel, []):
            layer, inferred = "transition", True
        items.append({
            "path": rel,
            "source": source_of(rel),
            "layer": layer,
            "inferred": inferred,
            "tags": tags.get(rel, []),
            "purpose": purpose,
            "name": m.get("name") or rel,
            "description": m.get("description") or "",
            "duration": duration_of(mf.parent / "index.html") or next(
                (v.get("default") for v in m.get("variables", []) if v.get("id") == "duration"), None),
            "vars": [v.get("id") for v in m.get("variables", []) if v.get("id")],
            "used": usage.get(rel, 0),
            "thumb": str(studio / ".thumbs" / f"{rel}.jpg"),
        })
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layer", choices=["cutaway", "overlay", "transition"])
    ap.add_argument("--purpose", nargs="*", default=[])
    ap.add_argument("--q", nargs="*", default=[], help="keywords matched against path/name/description")
    ap.add_argument("--source", choices=["kit", "channel", "library", "all"], default="all")
    ap.add_argument("--untagged", action="store_true", help="include compositions without a kind")
    ap.add_argument("--limit", type=int, default=15)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--studio")
    args = ap.parse_args()

    items = load_index(studio_path(args.studio))
    hits = []
    for it in items:
        if args.source != "all" and it["source"] != args.source:
            continue
        if it["layer"] is None and not args.untagged:
            continue
        if args.layer and it["layer"] not in (args.layer, None):
            continue
        if args.purpose and it["layer"] is not None and not set(args.purpose) & set(it["purpose"]):
            continue
        hay = f"{it['path']} {it['name']} {it['description']}".lower()
        hay += " " + " ".join(it["tags"]).lower()
        kw = sum(1 for q in args.q if q.lower() in hay)
        rank = {"kit": 0, "channel": 1, "library": 2}[it["source"]]
        hits.append((rank, -kw, -it["used"], it["path"], it))
    hits.sort(key=lambda h: h[:4])
    shown = [h[-1] for h in hits[: args.limit]]

    if args.json:
        print(json.dumps(shown, ensure_ascii=False, indent=2))
        return
    for it in shown:
        tag = it["source"] + (f" ×{it['used']}" if it["used"] else "")
        kind = f"{it['layer'] or '?'}{'*' if it['inferred'] else ''}/{','.join(it['purpose']) or '?'}"
        dur = f"{it['duration']:g}s" if it["duration"] else "?s"
        print(f"[{tag}] {it['path']}  {kind}  {dur}  {it['name']}")
        if it["vars"]:
            more = " …" if len(it["vars"]) > 12 else ""
            print(f"    vars: {' '.join(it['vars'][:12])}{more}")
        if it["description"]:
            print(f"    ↳ {it['description'][:120]}")
    print(f"— {len(shown)} of {len(hits)} matches")


if __name__ == "__main__":
    main()
