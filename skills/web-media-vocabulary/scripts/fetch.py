#!/usr/bin/env python3
"""Download the picks in a session file into a project and record their licenses.

    fetch.py --dest public/images/stock
    fetch.py --dest src/assets/media --slot hero icons --credits docs/CREDITS.md
    fetch.py --dest public/images/stock --dry-run

Per source:
  Pexels, Pixabay, Openverse   downloaded at the slot's target width
  Unsplash                     not downloaded: its API terms require using the CDN
                               link, so an <img srcset> snippet is printed instead,
                               and the download is reported to Unsplash as required
  Iconify                      each icon of the picked set saved as an SVG

Every pick is checked against the license whitelist again; anything outside it is
refused. A row per pick is added to the credits file (existing rows are kept).
Standard library only.
"""
import argparse
import datetime
import json
import pathlib
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sources  # noqa: E402

# Target width (px) per slot when --width is not given.
WIDTH = {"hero": 2400, "banner": 2400, "herovideo": 1280, "feature": 1600, "cover": 1600,
         "texture": 1600, "og": 1200, "card": 1000, "illustration": 1200, "avatar": 600}
VIDEO_WARN = 3 * 1024 * 1024
IMAGE_WARN = 600 * 1024

HEADER = """# 素材授權紀錄

網站使用的圖庫素材。全部為免費、可商用授權；「標註」欄寫「需要」的，請把標註文字放在頁尾或「關於／授權」頁。

| 檔案 | 版位 | 來源 | 作者 | 授權 | 標註 | 原始頁面 | 取得日期 |
|---|---|---|---|---|---|---|---|
"""


def download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": sources.UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        ctype = r.headers.get("Content-Type", "")
        if "html" in ctype:
            raise sources.SourceError(f"got a web page instead of a file ({url})")
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            while chunk := r.read(1 << 16):
                f.write(chunk)
    return path.stat().st_size


def ext_of(url, default):
    suffix = pathlib.PurePosixPath(urllib.parse.urlparse(url).path).suffix.lower()
    return {".jpeg": ".jpg"}.get(suffix, suffix) if suffix in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".mp4") else default


def pick_file(files, width):
    """The largest rendition no wider than width, else the smallest one."""
    fit = [f for f in files if f["width"] <= width]
    return max(fit, key=lambda f: f["width"]) if fit else min(files, key=lambda f: f["width"])


def refresh_pixabay(rec):
    """Pixabay URLs expire after 24 hours; look the item up again by id."""
    if not sources.available("pixabay"):
        raise sources.SourceError("set PIXABAY_API_KEY to download Pixabay picks")
    found = sources.pixabay(rec["kind"], "", 3, ids=rec["id"])
    if not found:
        raise sources.SourceError(f"Pixabay item {rec['id']} is no longer available")
    return found[0]


# Slots that sit in the first screen: load at once instead of lazily.
ABOVE_FOLD = {"hero", "banner", "og"}


def unsplash_snippet(rec, width, slot):
    raw = rec["download"]
    sep = "&" if "?" in raw else "?"
    steps = [w for w in (640, 1080, 1600, 2400) if w <= max(width, 640)]
    src = lambda w: f"{raw}{sep}w={w}&q=75&auto=format&fit=crop"
    srcset = ", ".join(f"{src(w)} {w}w" for w in steps)
    alt = (rec.get("alt") or "").replace('"', "'")
    load = 'fetchpriority="high"' if slot in ABOVE_FOLD else 'loading="lazy"'
    return f'<img src="{src(steps[-1])}" srcset="{srcset}" sizes="100vw" alt="{alt}" {load}>'


def fetch_one(rec, slot, dest, width, dry):
    """Return (file label, notes) for one pick."""
    src, kind = rec["source"], rec["kind"]
    stem = f"{slot}-{src}-{rec['id']}"
    notes = []
    if src == "iconify":
        prefix = rec["id"]
        saved = []
        for full in filter(None, rec["icons"]):
            p, name = full.split(":", 1)
            path = dest / "icons" / prefix / f"{name}.svg"
            if not dry:
                download(f"https://api.iconify.design/{p}/{name}.svg", path)
            saved.append(path)
        missing = [t.split("|")[0] for t, i in zip(rec["terms"], rec["icons"]) if not i]
        if missing:
            notes.append(f"這套沒有對應：{', '.join(missing)}（到 {rec['page']} 找替代名稱）")
        return str(dest / "icons" / prefix) + "/", notes
    if src == "unsplash":
        if not dry:
            if not sources.available("unsplash"):
                raise sources.SourceError("set UNSPLASH_ACCESS_KEY to report Unsplash downloads")
            sources.get_json(rec["track"], {"Authorization": f"Client-ID {sources.key('unsplash')}",
                                            "Accept-Version": "v1"})
        notes.append("Unsplash 依規定以 CDN 連結使用，貼上這段：\n    " + unsplash_snippet(rec, width, slot))
        return "（Unsplash CDN 連結）", notes
    if src == "pixabay" and not dry:
        rec = {**rec, **refresh_pixabay(rec)}
    if kind == "video":
        f = pick_file(rec["files"], width)
        path = dest / f"{stem}-{f['width']}.mp4"
        url = f["url"]
    elif src == "pexels":
        url = f"{rec['download']}?auto=compress&cs=tinysrgb&w={min(width, rec['width'])}"
        path = dest / f"{stem}.jpg"
    else:
        url = rec["download"]
        path = dest / f"{stem}{ext_of(url, '.jpg')}"
        cap = rec.get("max_download_width")
        if cap and cap < width:
            notes.append(f"這個來源最大只給 {cap}px，比建議的 {width}px 小，大螢幕可能會糊")
    if dry:
        return str(path), notes
    size = download(url, path)
    mb = size / 1024 / 1024
    if kind == "video" and size > VIDEO_WARN:
        notes.append(f"影片 {mb:.1f} MB，超過背景影片建議的 3 MB；壓縮方法見 references/video.md")
    elif kind != "video" and size > IMAGE_WARN:
        notes.append(f"圖片 {size // 1024} KB，上線前用 optimize-images 轉 WebP")
    return str(path), notes


def source_name(rec):
    name = {"pexels": "Pexels", "unsplash": "Unsplash", "pixabay": "Pixabay", "iconify": "Iconify"}.get(rec["source"])
    return name or f"Openverse（{rec.get('provider') or '?'}）"


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--session", default=".web-media/session.json", help="session file (default: %(default)s)")
    ap.add_argument("--dest", required=True, help="folder in the project for the files, e.g. public/images/stock")
    ap.add_argument("--slot", nargs="*", help="only these slots")
    ap.add_argument("--width", type=int, help="target width in px (default: per slot, e.g. hero 2400)")
    ap.add_argument("--credits", default="CREDITS.md", help="license record to append to (default: %(default)s)")
    ap.add_argument("--dry-run", action="store_true", help="show what would be saved; download nothing")
    args = ap.parse_args()

    session = json.loads(pathlib.Path(args.session).read_text(encoding="utf-8"))
    by_uid = {(k, r["uid"]): r for k, s in session["slots"].items() for g in s.get("groups", []) for r in g["items"]}
    picks = {k: v for k, v in session.get("picks", {}).items() if v and (not args.slot or k in args.slot)}
    if not picks:
        sys.exit("nothing picked yet — choose with ☆ on the board first")

    dest = pathlib.Path(args.dest)
    credits = pathlib.Path(args.credits)
    existing = credits.read_text(encoding="utf-8") if credits.exists() else ""
    today = datetime.date.today().isoformat()
    rows, attributions, failed = [], [], 0

    for slot, uids in picks.items():
        width = args.width or WIDTH.get(slot, 1600)
        for uid in uids:
            rec = by_uid.get((slot, uid))
            if not rec:
                print(f"✗ [{slot}] {uid}: not in the session any more (search was re-run?)")
                failed += 1
                continue
            if not sources.allowed(rec):
                print(f"✗ [{slot}] {uid}: license {rec.get('license')!r} is not on the whitelist — refused")
                failed += 1
                continue
            try:
                saved, notes = fetch_one(rec, slot, dest, width, args.dry_run)
            except (sources.SourceError, OSError) as e:
                print(f"✗ [{slot}] {uid}: {e}")
                failed += 1
                continue
            print(f"✓ [{slot}] {saved}")
            if rec["kind"] in ("photo", "illustration") and rec.get("alt"):
                label = "關鍵字" if rec["source"] == "pixabay" else "描述"
                print(f"    alt 參考（圖庫{label}）：{rec['alt']}；請改寫成這張圖在頁面上的用途")
            for n in notes:
                print(f"    {n}")
            line = sources.attribution_line(rec)
            if rec.get("attribution_required"):
                attributions.append(line)
            if rec["page"] not in existing:
                rows.append("| " + " | ".join(cell(c) for c in (
                    saved, slot, source_name(rec), rec["author"], f"[{rec['license']}]({rec['license_url']})" if rec.get("license_url") else rec["license"],
                    "需要：" + line if rec.get("attribution_required") else "免",
                    rec["page"], today)) + " |")

    if rows and not args.dry_run:
        credits.parent.mkdir(parents=True, exist_ok=True)
        text = existing if existing else HEADER
        credits.write_text(text.rstrip("\n") + "\n" + "\n".join(rows) + "\n", encoding="utf-8")
        print(f"\n授權紀錄：{credits}（新增 {len(rows)} 筆）")
    if attributions:
        print("\n需要放在網站上的標註：")
        for a in dict.fromkeys(attributions):
            print(f"  - {a}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
