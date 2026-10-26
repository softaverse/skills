#!/usr/bin/env python3
"""Refresh catalog/react-bits.md and catalog/magic-ui.md from the official component lists.

    sync_catalog.py            fetch both lists and rewrite the catalog
    sync_catalog.py --check    report what changed without writing

Each library publishes an llms.txt index (name, page URL, one-line description,
category). The Chinese one-liners and effect ids live in catalog/translations.json,
keyed by component name, so a refresh keeps them; components without one are listed
at the end so they can be translated. Only names, descriptions and links are stored —
never component code. Standard library only.
"""
import argparse
import datetime
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
TRANSLATIONS = CATALOG / "translations.json"
ENTRY = re.compile(r"^- \[(.+?)\]\((https?://[^)\s]+)\): (.*?)(?: CLI: `[^`]+`\.?)?$")

LIBRARIES = {
    "react-bits": {
        "title": "React Bits",
        "index": "https://reactbits.dev/llms.txt",
        "sections": {
            "Text Animations": "文字動畫",
            "Animations": "互動動畫",
            "Components": "元件",
            "Micro": "微互動",
            "Backgrounds": "背景",
        },
        "about": (
            "React 專用；每個元件有 JS／TS × CSS／Tailwind 四種版本，用 shadcn 或 jsrepo CLI 加進專案。"
            "授權 MIT + Commons Clause：可以用在任何網站或產品（含商用），但不能轉賣或轉散布元件本身。"
            "免費版之外另有付費的 React Bits Pro，不收在這裡。"
        ),
    },
    "magic-ui": {
        "title": "Magic UI",
        "index": "https://magicui.design/llms.txt",
        "sections": {"Components": "元件"},
        "about": "React 專用，需要 Tailwind CSS；用 shadcn CLI 把元件原始碼加進專案。授權 MIT。",
    },
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "web-motion-vocabulary/sync_catalog"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def parse(text, sections):
    items, section = [], None
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        m = ENTRY.match(line.strip())
        if m and section in sections:
            name, url, desc = m.groups()
            items.append({"section": section, "name": name, "url": url.replace("://www.", "://"), "en": desc})
    return items


def render(lib, items, known):
    lines = [
        f"# {lib['title']}",
        "",
        f"官方元件清單，由 `scripts/sync_catalog.py` 從 {lib['index']} 產生，"
        f"{datetime.date.today():%Y-%m-%d} 同步，共 {len(items)} 個。只收名稱、說明與連結，不含程式碼。",
        "",
        lib["about"],
        "",
        "格式：`**名稱** — 中文說明 → 對應效果 id · 官方頁面`。沒有中文說明的是新元件，暫列英文。",
    ]
    for section, label in lib["sections"].items():
        group = [i for i in items if i["section"] == section]
        if not group:
            continue
        lines += ["", f"## {label}（{section}）", ""]
        for i in group:
            t = known.get(i["name"])
            zh, ids = (t, []) if isinstance(t, str) else ((t or {}).get("zh"), (t or {}).get("ids", []))
            effect = f" → {'、'.join(f'`{x}`' for x in ids)}" if ids else ""
            lines.append(f"- **{i['name']}** — {zh or i['en']}{effect} · {i['url']}")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="report changes without writing files")
    args = ap.parse_args()

    translations = json.loads(TRANSLATIONS.read_text(encoding="utf-8"))
    missing = []
    for key, lib in LIBRARIES.items():
        try:
            items = parse(fetch(lib["index"]), lib["sections"])
        except OSError as e:
            sys.exit(f"{lib['title']}: could not fetch {lib['index']} ({e})")
        if not items:
            sys.exit(f"{lib['title']}: no components found — has the llms.txt format changed?")
        known = translations.get(key, {})
        names = {i["name"] for i in items}
        new = [i for i in items if i["name"] not in known]
        gone = sorted(set(known) - names)
        missing += [f"{key}: {i['name']} — {i['en']}" for i in new]
        print(f"{lib['title']}: {len(items)} components, {len(new)} without Chinese, {len(gone)} no longer listed")
        for name in gone:
            print(f"  removed upstream: {name}")
        if not args.check:
            (CATALOG / f"{key}.md").write_text(render(lib, items, known), encoding="utf-8")

    if missing:
        print("\nAdd these to catalog/translations.json, then run again:")
        print("\n".join(f"  {m}" for m in missing))


if __name__ == "__main__":
    main()
