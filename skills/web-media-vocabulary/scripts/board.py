#!/usr/bin/env python3
"""Serve a comparison page of the search results in a session file and open it.

    board.py                       # every slot in .web-media/session.json
    board.py --slot hero           # one slot
    board.py --title "首頁 Hero 配圖" --headline "讓團隊專注在重要的事"

Each slot is a section; each direction searched for it is a row of results,
cropped to the slot's ratio. Clicking ☆ on a result picks it, and the pick is
written back to the session file for fetch.py. Previews load from the libraries'
CDNs, so the page needs a network connection. Runs until Ctrl+C. Standard library only.
"""
import argparse
import html
import http.server
import json
import pathlib
import re
import sys
import threading
import webbrowser

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from search import SLOTS  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENTRY = re.compile(r"^- \*\*(.+?)\*\* `([a-z0-9]+)` — (.+)$")


def load_vocabulary():
    vocab = {}
    for md in sorted((ROOT / "references").glob("*.md")):
        for line in md.read_text(encoding="utf-8").splitlines():
            m = ENTRY.match(line)
            if m:
                name, id_, definition = m.groups()
                vocab[id_] = {"name": name, "def": definition}
    return vocab


class Handler(http.server.BaseHTTPRequestHandler):
    page = b""
    vocab = b""
    session = None
    lock = threading.Lock()

    def send_bytes(self, body, ctype, code=200):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            self.send_bytes(self.page, "text/html; charset=utf-8")
        elif path == "/vocab.json":
            self.send_bytes(self.vocab, "application/json; charset=utf-8")
        elif path == "/session.json":
            with self.lock:
                body = self.session.read_bytes()
            self.send_bytes(body, "application/json; charset=utf-8")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/pick":
            return self.send_error(404)
        try:
            msg = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            slot, uid, on = msg["slot"], msg["uid"], bool(msg["on"])
        except (ValueError, KeyError, TypeError):
            return self.send_error(400)
        with self.lock:
            # Re-read so searches run while the board is open are kept.
            data = json.loads(self.session.read_text(encoding="utf-8"))
            picks = data.setdefault("picks", {}).setdefault(slot, [])
            if on and uid not in picks:
                picks.append(uid)
            if not on and uid in picks:
                picks.remove(uid)
            tmp = self.session.with_suffix(".tmp")
            tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            tmp.replace(self.session)
        self.send_bytes(json.dumps(data["picks"], ensure_ascii=False).encode(), "application/json; charset=utf-8")

    def log_message(self, *args):
        pass


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--session", default=".web-media/session.json", help="session file (default: %(default)s)")
    ap.add_argument("--slot", nargs="*", help="show only these slots")
    ap.add_argument("--title", default="網站素材比較")
    ap.add_argument("--headline", default="把標題放在這張圖上", help="text for the 疊上標題 preview")
    ap.add_argument("--port", type=int, default=0, help="port to serve on (default: any free port)")
    ap.add_argument("--no-open", action="store_true", help="serve without opening a browser")
    args = ap.parse_args()

    session = pathlib.Path(args.session).resolve()
    if not session.exists():
        ap.error(f"{session} not found — run search.py first")
    slots = json.loads(session.read_text(encoding="utf-8")).get("slots", {})
    missing = [s for s in args.slot or [] if s not in slots]
    if missing:
        ap.error(f"no such slot(s): {', '.join(missing)} — have: {', '.join(slots) or 'none'}")

    order = list(SLOTS)
    shown = sorted(args.slot or slots, key=lambda k: order.index(k) if k in order else len(order))
    config = {"title": args.title, "headline": args.headline, "slots": shown}
    template = (ROOT / "scripts" / "board.html").read_text(encoding="utf-8")
    Handler.page = (template.replace("{{TITLE}}", html.escape(args.title))
                    .replace("{{CONFIG}}", json.dumps(config, ensure_ascii=False).replace("<", "\\u003c"))
                    .encode())
    Handler.vocab = json.dumps(load_vocabulary(), ensure_ascii=False).encode()
    Handler.session = session

    server = http.server.ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    print(url, flush=True)
    print(f"picks are saved to {session}", flush=True)
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
