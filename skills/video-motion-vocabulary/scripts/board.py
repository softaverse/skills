#!/usr/bin/env python3
"""Build a motion comparison board (HTML) from vocabulary ids and open it.

    board.py rise blurin slam
    board.py --title "Seg_05 進場方向" \
        --group "A｜俐落" rise blurin easeout \
        --group "B｜衝擊" slam impact shake
    board.py --check        # verify every 範例 path still exists in hf-studio

Thumbnails come from hf-studio's .thumbs/ and are inlined, so the board is one
self-contained file; each thumbnail links to the hf-studio player for the motion.
hf-studio is --studio, then $HF_STUDIO, then ~/Workspace/hyperframes/hf-studio.
Standard library only.
"""
import argparse
import base64
import collections
import datetime
import html
import json
import os
import pathlib
import re
import sys
import tempfile
import urllib.parse
import webbrowser

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENTRY = re.compile(r"^- \*\*(.+?)\*\* `([a-z0-9-]+)` — (.+)$")
FIELD = re.compile(r"^  - (感受|適合|搭配|注意|範例)：(.+)$")
CODE = re.compile(r"`([^`]+)`")
MAX_EXAMPLES = 3


def load_vocabulary():
    vocab = {}
    for md in sorted((ROOT / "references").glob("*.md")):
        current = None
        for line in md.read_text(encoding="utf-8").splitlines():
            m = ENTRY.match(line)
            if m:
                name, id_, definition = m.groups()
                if id_ in vocab:
                    sys.exit(f"duplicate id `{id_}` in {md.name} and {vocab[id_]['file']}")
                current = vocab[id_] = {"id": id_, "name": name, "def": definition,
                                        "fields": {}, "examples": [], "file": md.name}
                continue
            m = FIELD.match(line)
            if m and current:
                if m[1] == "範例":
                    current["examples"] = CODE.findall(m[2])
                else:
                    current["fields"][m[1]] = m[2]
    return vocab


def find_studio(arg):
    path = pathlib.Path(arg or os.environ.get("HF_STUDIO") or "~/Workspace/hyperframes/hf-studio").expanduser()
    if not (path / "compositions").is_dir():
        sys.exit(f"hf-studio not found at {path} — pass --studio or set HF_STUDIO")
    return path


def manifest(studio, comp):
    path = studio / "compositions" / comp / "manifest.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def thumb_uri(studio, comp):
    path = studio / ".thumbs" / f"{comp}.jpg"
    if path.exists():
        return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()
    return None


def player_url(port, comp):
    return f"http://localhost:{port}/app/player.html?c={urllib.parse.quote(comp, safe='/')}"


def card(entry, studio, port):
    e = html.escape
    shots = []
    for comp in entry["examples"][:MAX_EXAMPLES]:
        meta = manifest(studio, comp) or {}
        uri = thumb_uri(studio, comp)
        img = f'<img src="{uri}" alt="">' if uri else '<div class="noimg">無縮圖</div>'
        label = meta.get("name") or comp
        shots.append(f'<a class="shot" href="{e(player_url(port, comp))}" target="_blank">'
                     f'{img}<span>▶ {e(label)}</span><code>{e(comp)}</code></a>')
    if not shots:
        shots.append('<div class="noimg">hf-studio 尚無範例</div>')
    fields = "".join(
        f"<dt>{k}</dt><dd>{e(v)}</dd>" for k, v in entry["fields"].items() if k != "搭配"
    )
    return (
        f'<article class="card"><h3>{e(entry["name"])} <code>{e(entry["id"])}</code></h3>'
        f'<p>{e(entry["def"])}</p>'
        f'{f"<dl>{fields}</dl>" if fields else ""}'
        f'<div class="shots">{"".join(shots)}</div></article>'
    )


PAGE = """<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{ --bg:#f6f5f2; --panel:#fff; --ink:#1b1b1b; --muted:#6b6b6b; --line:#e3e1dc; --accent:#2f5bea; }}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg:#141414; --panel:#1e1e1e; --ink:#ecebe8; --muted:#a3a19c; --line:#2e2e2e; --accent:#8aa4ff; }}
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink);
  font:15px/1.6 -apple-system,"PingFang TC","Noto Sans TC",system-ui,sans-serif; }}
header {{ padding:32px 16px 8px; max-width:1400px; margin:auto; }}
h1 {{ margin:0; font-size:26px; }}
header p {{ margin:4px 0 0; color:var(--muted); font-size:13px; }}
main {{ display:grid; gap:24px; padding:16px; max-width:1400px; margin:auto;
  grid-template-columns:repeat(auto-fit,minmax(min(100%,460px),1fr)); }}
section h2 {{ font-size:17px; margin:0 0 12px; padding-bottom:8px; border-bottom:2px solid var(--accent); }}
.card {{ padding:14px; background:var(--panel); border:1px solid var(--line); border-radius:12px; margin-bottom:12px; }}
h3 {{ margin:0 0 4px; font-size:15px; }}
h3 code {{ font-size:12px; color:var(--muted); font-weight:400; }}
.card > p {{ margin:0; color:var(--muted); font-size:13px; }}
dl {{ margin:10px 0 0; display:grid; grid-template-columns:auto 1fr; gap:4px 8px; font-size:13px; }}
dt {{ color:var(--accent); font-weight:600; }}
dd {{ margin:0; }}
.shots {{ display:grid; gap:10px; margin-top:12px; grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); }}
.shot {{ display:block; color:inherit; text-decoration:none; font-size:12px; min-width:0; }}
.shot img, .noimg {{ display:block; width:100%; aspect-ratio:16/9; object-fit:cover; border-radius:6px;
  background:var(--line); border:1px solid var(--line); }}
.shot:hover img {{ outline:2px solid var(--accent); }}
.shot span {{ display:block; margin-top:4px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.shot code {{ display:block; color:var(--muted); font-size:11px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.noimg {{ display:grid; place-items:center; color:var(--muted); font-size:12px; }}
</style></head>
<body><header><h1>{title}</h1><p>{stamp}　縮圖是靜止畫面——點開在 hf-studio player 看動態（需先在 hf-studio 執行 npm start）</p></header>
<main>{sections}</main></body></html>
"""


def check(vocab, studio):
    missing = [(e["file"], e["id"], c) for e in vocab.values() for c in e["examples"]
               if manifest(studio, c) is None]
    empty = [e["id"] for e in vocab.values() if not e["examples"]]
    used = {c for e in vocab.values() for c in e["examples"]}
    comps = sorted(str(p.parent.relative_to(studio / "compositions"))
                   for p in (studio / "compositions").glob("**/manifest.json"))
    unused = collections.Counter(c.split("/")[0] if "/" in c else "(channel)" for c in comps if c not in used)

    print(f"{len(vocab)} entries, {len(used)} of {len(comps)} compositions referenced")
    for file, id_, comp in missing:
        print(f"MISSING  {file}  `{id_}`  {comp}")
    for id_ in empty:
        print(f"NO 範例  `{id_}`")
    print("unreferenced by collection: " + ", ".join(f"{k} {v}" for k, v in unused.most_common()))
    return 1 if missing else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="*", help="vocabulary ids for a single ungrouped board")
    ap.add_argument("--group", nargs="+", action="append", metavar=("LABEL", "ID"),
                    help="a labeled direction followed by its ids; repeat to compare")
    ap.add_argument("--title", default="動態比較")
    ap.add_argument("--studio", help="hf-studio path")
    ap.add_argument("--port", type=int, default=3025, help="hf-studio dev server port")
    ap.add_argument("--out", help="output .html path (default: system temp dir)")
    ap.add_argument("--no-open", action="store_true", help="write the file without opening a browser")
    ap.add_argument("--check", action="store_true", help="verify 範例 paths and report coverage, then exit")
    args = ap.parse_args()

    vocab = load_vocabulary()
    studio = find_studio(args.studio)
    if args.check:
        sys.exit(check(vocab, studio))

    groups = [(g[0], g[1:]) for g in args.group or []]
    if args.ids:
        groups.insert(0, ("", args.ids))
    if not groups or not any(ids for _, ids in groups):
        ap.error("give at least one id")

    unknown = [i for _, ids in groups for i in ids if i not in vocab]
    if unknown:
        sys.exit(f"unknown id(s): {', '.join(unknown)} — ids are the `code` after each name in references/*.md")

    sections = "".join(
        f'<section>{f"<h2>{html.escape(label)}</h2>" if label else ""}'
        + "".join(card(vocab[i], studio, args.port) for i in ids) + "</section>"
        for label, ids in groups
    )
    now = datetime.datetime.now()
    page = PAGE.format(title=html.escape(args.title), stamp=now.strftime("%Y-%m-%d %H:%M"), sections=sections)

    out = pathlib.Path(args.out) if args.out else (
        pathlib.Path(tempfile.gettempdir()) / "video-motion-vocabulary" / f"board-{now:%Y%m%d-%H%M%S}.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(out)
    if not args.no_open:
        webbrowser.open(out.resolve().as_uri())


if __name__ == "__main__":
    main()
