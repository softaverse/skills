#!/usr/bin/env python3
"""Build a style comparison board (HTML) from vocabulary ids and open it.

    board.py glass clay aurora
    board.py --title "首頁方向" \
        --group "A｜Editorial：有觀點的品牌感" editorial serif bigtype \
        --group "B｜Swiss：理性清楚" swiss minimal gray1

Images are inlined, so the board is a single self-contained file.
Standard library only.
"""
import argparse
import base64
import datetime
import html
import pathlib
import re
import sys
import tempfile
import webbrowser

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENTRY = re.compile(r"^- \*\*(.+?)\*\* `([a-z0-9]+)` — (.+)$")
FIELD = re.compile(r"^  - (感受|適合|搭配|注意)：(.+)$")


def load_vocabulary():
    vocab = {}
    for md in sorted((ROOT / "references").glob("*.md")):
        current = None
        for line in md.read_text(encoding="utf-8").splitlines():
            m = ENTRY.match(line)
            if m:
                name, id_, definition = m.groups()
                current = vocab[id_] = {"id": id_, "name": name, "def": definition, "fields": {}}
                continue
            m = FIELD.match(line)
            if m and current:
                current["fields"][m[1]] = m[2]
    return vocab


def image_uri(id_):
    for ext, mime in (("webp", "image/webp"), ("png", "image/png")):
        path = ROOT / "assets" / f"{id_}.{ext}"
        if path.exists():
            return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()
    return None


def card(entry):
    e = html.escape
    uri = image_uri(entry["id"])
    img = f'<img src="{uri}" alt="{e(entry["name"])}">' if uri else '<div class="noimg">無樣張</div>'
    fields = "".join(
        f"<dt>{k}</dt><dd>{e(v)}</dd>" for k, v in entry["fields"].items() if k != "搭配"
    )
    return (
        f'<article class="card">{img}<div class="body">'
        f'<h3>{e(entry["name"])}</h3><p>{e(entry["def"])}</p>'
        f'{f"<dl>{fields}</dl>" if fields else ""}</div></article>'
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
  grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr)); }}
section h2 {{ font-size:17px; margin:0 0 12px; padding-bottom:8px; border-bottom:2px solid var(--accent); }}
.card {{ display:grid; grid-template-columns:150px 1fr; gap:14px; align-items:start; padding:12px;
  background:var(--panel); border:1px solid var(--line); border-radius:12px; margin-bottom:12px; }}
.card img, .noimg {{ display:block; width:150px; aspect-ratio:1; object-fit:cover; border-radius:8px; background:var(--line); }}
.noimg {{ display:grid; place-items:center; color:var(--muted); font-size:13px; }}
@media (max-width:420px) {{ .card {{ grid-template-columns:96px 1fr; }} .card img, .noimg {{ width:96px; }} }}
.body {{ min-width:0; }}
h3 {{ margin:0 0 4px; font-size:15px; }}
.body p {{ margin:0; color:var(--muted); font-size:13px; }}
dl {{ margin:10px 0 0; display:grid; grid-template-columns:auto 1fr; gap:4px 8px; font-size:13px; }}
dt {{ color:var(--accent); font-weight:600; }}
dd {{ margin:0; }}
</style></head>
<body><header><h1>{title}</h1><p>{stamp}</p></header>
<main>{sections}</main></body></html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="*", help="vocabulary ids for a single ungrouped board")
    ap.add_argument("--group", nargs="+", action="append", metavar=("LABEL", "ID"),
                    help="a labeled direction followed by its ids; repeat to compare")
    ap.add_argument("--title", default="風格比較")
    ap.add_argument("--out", help="output .html path (default: system temp dir)")
    ap.add_argument("--no-open", action="store_true", help="write the file without opening a browser")
    args = ap.parse_args()

    groups = [(g[0], g[1:]) for g in args.group or []]
    if args.ids:
        groups.insert(0, ("", args.ids))
    if not groups or not any(ids for _, ids in groups):
        ap.error("give at least one id")

    vocab = load_vocabulary()
    unknown = [i for _, ids in groups for i in ids if i not in vocab]
    if unknown:
        sys.exit(f"unknown id(s): {', '.join(unknown)} — ids are the `code` after each name in references/*.md")

    sections = "".join(
        f'<section>{f"<h2>{html.escape(label)}</h2>" if label else ""}'
        + "".join(card(vocab[i]) for i in ids) + "</section>"
        for label, ids in groups
    )
    now = datetime.datetime.now()
    page = PAGE.format(title=html.escape(args.title), stamp=now.strftime("%Y-%m-%d %H:%M"), sections=sections)

    out = pathlib.Path(args.out) if args.out else (
        pathlib.Path(tempfile.gettempdir()) / "web-design-vocabulary" / f"board-{now:%Y%m%d-%H%M%S}.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(out)
    if not args.no_open:
        webbrowser.open(out.resolve().as_uri())


if __name__ == "__main__":
    main()
