#!/usr/bin/env python3
"""Search free, commercially usable stock media for one slot of a website and save
the results as a labeled group in a session file, for board.py to show and fetch.py
to download.

    search.py --slot hero --label "A｜高調明亮" --style highkey \
        --q "bright minimal workspace natural light" --color white
    search.py --slot hero --label "B｜暖色紀實" --style candid golden \
        --q "people working together warm light"
    search.py --slot herovideo --label "A｜慢速空拍" --q "aerial ocean slow"
    search.py --slot icons --label "A｜細線" --style iconline \
        --q "home, user, settings, chart, mail" --prefixes lucide tabler ph --variant base

Run it once per direction; the same --slot and --label replaces that group. Sources
without an API key are skipped and reported. Standard library only.
"""
import argparse
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sources  # noqa: E402

# kind, desktop ratio, phone ratio, orientation, minimum source width (px)
SLOTS = {
    "hero":         ("photo", "16:9", "4:5", "landscape", 1920, "首頁主視覺"),
    "herovideo":    ("video", "16:9", "9:16", "landscape", 1280, "首頁背景影片"),
    "banner":       ("photo", "21:9", "4:5", "landscape", 1920, "橫幅／區塊背景"),
    "feature":      ("photo", "4:3", "4:3", "landscape", 1200, "功能／區塊配圖"),
    "card":         ("photo", "4:3", "4:3", None, 800, "卡片縮圖"),
    "cover":        ("photo", "16:9", "16:9", "landscape", 1200, "文章封面"),
    "og":           ("photo", "1200:630", "1200:630", "landscape", 1200, "社群分享圖（OG）"),
    "avatar":       ("photo", "1:1", "1:1", "square", 400, "頭像／團隊"),
    "texture":      ("photo", "1:1", "1:1", None, 1600, "背景紋理"),
    "illustration": ("illustration", "4:3", "4:3", None, 800, "插畫"),
    "icons":        ("icon", "1:1", "1:1", None, 0, "圖示"),
}


def load(path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"version": 1, "slots": {}, "picks": {}}


def save(path, session):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(session, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--session", default=".web-media/session.json", help="session file (default: %(default)s)")
    ap.add_argument("--slot", required=True, help=f"a preset ({', '.join(SLOTS)}) or any new name with --kind and --ratio")
    ap.add_argument("--slot-label", help="display name for the slot, e.g. 「關於我們」大圖")
    ap.add_argument("--label", required=True, help="the direction, e.g. 「A｜高調明亮」")
    ap.add_argument("--style", nargs="*", default=[], help="vocabulary ids this direction stands for")
    ap.add_argument("--q", required=True, help="English search words; for icons, comma-separated concepts")
    ap.add_argument("--kind", choices=list(sources.KINDS), help="override the slot's media kind")
    ap.add_argument("--ratio", help="override the slot's desktop crop, e.g. 3:2")
    ap.add_argument("--orientation", choices=["landscape", "portrait", "square", "any"])
    ap.add_argument("--color", help="dominant color: a name (white, blue…), bw for black and white; Pexels also takes #hex")
    ap.add_argument("--min-width", type=int, help="drop results narrower than this many pixels")
    ap.add_argument("--sources", nargs="*", help="limit to these sources")
    ap.add_argument("--n", type=int, default=8, help="results per source, or icon sets for icons (default: %(default)s)")
    ap.add_argument("--prefixes", nargs="*", help="icons: Iconify set prefixes to search, e.g. lucide tabler")
    ap.add_argument("--variant", help="icons: keep only this variant (duotone, fill, bold…; base = no suffix)")
    args = ap.parse_args()

    kind, ratio, mratio, orient, minw, slot_label = SLOTS.get(args.slot, (None, "4:3", "4:3", None, 0, args.slot))
    kind = args.kind or kind
    if not kind:
        ap.error(f"--slot {args.slot} is not a preset; give --kind")
    ratio = args.ratio or ratio
    orient = None if args.orientation == "any" else args.orientation or orient
    minw = minw if args.min_width is None else args.min_width

    wanted = args.sources or sources.KINDS[kind]
    items, report = [], []
    if kind == "icon":
        terms = [t.strip() for t in args.q.split(",") if t.strip()]
        try:
            items = sources.iconify(terms, args.n, args.prefixes, args.variant)
            report.append(f"iconify {len(items)} sets")
        except sources.SourceError as e:
            report.append(f"iconify skipped: {e}")
    else:
        for name in wanted:
            if name not in sources.KINDS[kind]:
                report.append(f"{name} skipped: no {kind} search")
                continue
            if not sources.available(name):
                report.append(f"{name} skipped: set {sources.KEYS[name]}")
                continue
            try:
                found = sources.SEARCH[name](kind, args.q, args.n, orient, args.color, minw)
            except sources.SourceError as e:
                report.append(f"{name} skipped: {e}")
                continue
            found = [r for r in found if sources.allowed(r)][: args.n]
            items += found
            report.append(f"{name} {len(found)}")

    path = pathlib.Path(args.session)
    session = load(path)
    slot = session["slots"].setdefault(args.slot, {})
    slot.update(kind=kind, ratio=ratio, mobile_ratio=args.ratio or mratio,
                label=args.slot_label or slot.get("label") or slot_label)
    group = {"label": args.label, "styles": args.style, "query": args.q,
             "params": {"orientation": orient, "color": args.color, "min_width": minw,
                        "prefixes": args.prefixes, "variant": args.variant},
             "searched": time.strftime("%Y-%m-%d %H:%M"), "items": items}
    groups = slot.setdefault("groups", [])
    labels = [g["label"] for g in groups]
    if args.label in labels:
        groups[labels.index(args.label)] = group  # a re-run keeps its place on the board
    else:
        groups.append(group)
    save(path, session)

    flagged = sum(1 for r in items if r["flags"])
    print(f"[{args.slot}] {args.label}: {len(items)} results ({'; '.join(report)})"
          + (f", {flagged} flagged ⚠️" if flagged else ""))
    if not items:
        sys.exit(1)


if __name__ == "__main__":
    main()
