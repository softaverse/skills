#!/usr/bin/env python3
"""Serve a scrollable page of live effect demos and open it.

    board.py splitreveal scramble
    board.py --title "首頁 Hero 的標題" \
        --group "A｜沉穩：一行一行浮上來" splitreveal \
        --group "B｜科技感：亂碼解出正確的字" scramble

The effects are stacked as sections of one page, like a real site: scroll down
to go through them. The demos load real libraries from a CDN, so the page is
served from a local port (not opened as a file) and runs until Ctrl+C.
Standard library only.
"""
import argparse
import html
import http.server
import json
import pathlib
import re
import sys
import threading
import urllib.parse
import webbrowser

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENTRY = re.compile(r"^- \*\*(.+?)\*\* `([a-z0-9]+)` — (.+)$")
FIELD = re.compile(r"^  - (感受|適合|搭配|注意|工具|成本|手機|減少動態|來源|Demo)：(.+)$")


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


SHELL = """<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{ --page:#e9e9e6; --bar:#ffffff; --ink:#18181b; --muted:#71717a; --line:#e4e4e1; --accent:#18181b;
  --on-accent:#ffffff; --frame:#fafaf9; --bezel:#d4d4d0; }}
body.dark {{ --page:#0b0b0c; --bar:#1a1a1d; --ink:#ededef; --muted:#8b8b93; --line:#2e2e33; --accent:#ededef;
  --on-accent:#0b0b0c; --frame:#111113; --bezel:#2a2a30; }}
* {{ box-sizing:border-box; }}
html, body {{ margin:0; height:100%; background:var(--page); color:var(--ink);
  font:14px/1.5 -apple-system,"PingFang TC","Noto Sans TC",system-ui,sans-serif; }}
body {{ display:flex; flex-direction:column; }}
header {{ display:flex; flex-wrap:wrap; gap:8px 16px; align-items:center; justify-content:space-between;
  padding:8px 16px; background:var(--bar); border-bottom:1px solid var(--line); }}
h1 {{ margin:0; font-size:15px; }}
.controls {{ display:flex; flex-wrap:wrap; gap:8px; }}
.seg {{ display:inline-flex; border:1px solid var(--line); border-radius:999px; overflow:hidden; }}
.seg button {{ font:inherit; font-size:13px; padding:4px 12px; border:0; background:transparent;
  color:var(--muted); cursor:pointer; }}
.seg button[aria-pressed="true"] {{ background:var(--accent); color:var(--on-accent); }}
.stage {{ flex:1; display:flex; justify-content:center; min-height:0; }}
iframe {{ border:0; width:100%; height:100%; display:block; background:var(--frame); }}
body.mobile .stage {{ padding:16px 0; }}
body.mobile iframe {{ width:375px; max-width:100%; border-radius:24px; outline:8px solid var(--bezel); }}
</style></head>
<body>
<header><h1>{title}</h1>
<div class="controls">
  <span class="seg" data-toggle="mobile"><button type="button" aria-pressed="true">桌機</button><button type="button" aria-pressed="false">手機寬度</button></span>
  <span class="seg" data-toggle="dark"><button type="button" aria-pressed="true">淺色</button><button type="button" aria-pressed="false">深色</button></span>
  <span class="seg" data-toggle="reduced"><button type="button" aria-pressed="true">正常</button><button type="button" aria-pressed="false">減少動態</button></span>
</div></header>
<div class="stage"><iframe src="{src}" title="{title}"></iframe></div>
<script>
const frame = document.querySelector("iframe");
const base = frame.getAttribute("src");
const state = {{ mobile: false, dark: false, reduced: false }};
document.querySelectorAll(".seg").forEach((seg) => {{
  const [off, on] = seg.querySelectorAll("button");
  seg.addEventListener("click", (ev) => {{
    if (ev.target.tagName !== "BUTTON") return;
    const key = seg.dataset.toggle, value = ev.target === on;
    if (state[key] === value) return;
    state[key] = value;
    off.setAttribute("aria-pressed", String(!value));
    on.setAttribute("aria-pressed", String(value));
    document.body.classList.toggle(key, value);
    // The phone frame is only a narrower view; theme and reduced motion reload the page.
    if (key !== "mobile")
      frame.src = base + (state.dark ? "&theme=dark" : "") + (state.reduced ? "&reduced=1" : "");
  }});
}});
</script></body></html>
"""


class Handler(http.server.SimpleHTTPRequestHandler):
    shell = b""
    vocab = b""

    def send_bytes(self, body, ctype):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            self.send_bytes(self.shell, "text/html; charset=utf-8")
        elif path == "/vocab.json":
            self.send_bytes(self.vocab, "application/json; charset=utf-8")
        elif path.startswith("/demos/"):
            super().do_GET()
        else:
            self.send_error(404)

    def end_headers(self):
        # Demos are edited while the board runs; never serve a stale copy.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def guess_type(self, path):
        return "text/javascript" if str(path).endswith(".js") else super().guess_type(path)

    def log_message(self, *args):
        pass


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="*", help="vocabulary ids for a single ungrouped page")
    ap.add_argument("--group", nargs="+", action="append", metavar=("LABEL", "ID"),
                    help="a labeled direction followed by its ids; repeat to compare")
    ap.add_argument("--title", default="動畫效果比較")
    ap.add_argument("--port", type=int, default=0, help="port to serve on (default: any free port)")
    ap.add_argument("--no-open", action="store_true", help="serve without opening a browser")
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

    query = [("title", args.title)]
    for label, ids in groups:
        if label:
            query.append(("group", label))
        query.append(("ids", ",".join(ids)))
    src = "/demos/_shared/page.html?" + urllib.parse.urlencode(query)

    Handler.shell = SHELL.format(title=html.escape(args.title), src=html.escape(src)).encode()
    Handler.vocab = json.dumps(vocab, ensure_ascii=False).encode()

    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", args.port), lambda *a: Handler(*a, directory=str(ROOT)))
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    print(url, flush=True)
    print(f"single effect: {url}demos/_shared/page.html?ids=<id>", flush=True)
    if not args.no_open:
        threading.Timer(0.3, webbrowser.open, (url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
