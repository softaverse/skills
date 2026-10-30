#!/usr/bin/env python3
"""Refresh catalog/icon-sets.md: every Iconify icon set a website may use commercially.

    sync_icon_sets.py            fetch the set list and rewrite the catalog
    sync_icon_sets.py --check    report what changed without writing

Sets come from Iconify's published set list (@iconify/collections on jsDelivr, with
https://api.iconify.design/collections as a fallback) and pass the same license
whitelist as search.py (sources.SPDX_OK); unmaintained and hidden sets are left out.
For each set it records the size, license, grid, and the variants usable with
`search.py --variant`, read from the set's own metadata or counted from icon names.
The Chinese one-liners and style ids live in catalog/translations.json, keyed by
prefix, so a refresh keeps them; sets without one are listed at the end so they can
be described. Only names, counts and links are stored, never icons. Standard library only.
"""
import argparse
import collections
import datetime
import json
import pathlib
import sys
import time
import urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sources  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
TRANSLATIONS = CATALOG / "translations.json"

SECTIONS = {
    "UI 24px": "介面圖示：24px 格線",
    "UI 16px / 32px": "介面圖示：16／32px 格線",
    "UI Other / Mixed Grid": "介面圖示：其他格線",
    "Material": "Material 系列",
    "UI Multicolor": "彩色圖示",
    "Emoji": "表情符號",
    "Thematic": "主題圖示",
    "Flags / Maps": "國旗與地圖",
    "Programming": "程式與開發",
    "Logos": "品牌 Logo",
    "": "其他",
}
NOTES = {
    "Logos": "Logo 圖檔多為 CC0，但 Logo 本身是對方的商標：只能用來指稱該品牌（整合列表、登入按鈕、社群連結），"
             "要遵守對方的品牌規範，不能拿來做假的「合作客戶」Logo 牆。",
    "Emoji": "下載成 SVG，各平台看起來才會一致。",
}
SHARE = 0.08  # a suffix counts as a variant when at least this share of icons carries it
PAUSE = 0.2   # seconds between sets, to stay polite to the CDN
CDN = "https://cdn.jsdelivr.net/npm"


def get_json(url, timeout=30):
    for wait in (15, 30, 60, None):
        try:
            return sources.get_json(url, timeout=timeout)
        except sources.SourceError as e:
            if not ("429" in str(e) or "timed out" in str(e)) or wait is None:
                raise
            time.sleep(wait)


def variants(prefix):
    """Variant suffixes for --variant, from the set's metadata or its icon names."""
    # Per-set files come from the @iconify-json npm packages on jsDelivr: the API's
    # /collection endpoint rate-limits a 199-set run into hours of 429s.
    base = f"{CDN}/@iconify-json/{urllib.parse.quote(prefix)}"
    data = get_json(f"{base}/metadata.json")
    if data.get("suffixes"):
        return [k or "base" for k in data["suffixes"]], ""
    if data.get("prefixes"):
        # Variants written before the name (e.g. ic:outline-home); --variant cannot pick these.
        return [], "、".join(k for k in data["prefixes"] if k)
    names = []
    for group in (data.get("categories") or {}).values():
        names += group
    if not names:
        names = list(get_json(f"{base}/icons.json", timeout=120).get("icons", {}))
    if not names:
        return [], ""
    # Count a few more endings than search's base filter knows; "-line" there would hide
    # ordinary names such as tabler:chart-line.
    extra = ("-outlined", "-regular", "-line", "-f")
    tail = lambda n: sources.variant_of(n) or next((e[1:] for e in extra if n.endswith(e)), "")
    counts = collections.Counter(tail(n) for n in set(names))
    found = [v for v, c in counts.most_common() if v and c / len(set(names)) >= SHARE]
    return (["base", *found] if found else []), ""


def describe(prefix, info, known, extra):
    spdx = info["license"]["spdx"]
    t = known.get(prefix)
    zh, ids = (t, []) if isinstance(t, str) else ((t or {}).get("zh"), (t or {}).get("ids", []))
    tags = info.get("tags") or []
    look = "彩色" if info.get("palette") else "描邊" if "Uses Stroke" in tags else "單色"
    grid = f"{info['height']}px" if isinstance(info.get("height"), int) else "混合格線"
    vs, front = extra
    parts = [f"{info['total']:,} 個", f"{spdx}{'（需標註）' if sources.SPDX_OK[spdx] else ''}", f"{grid} {look}"]
    if vs:
        parts.append("變體 " + " ".join(f"`{v}`" for v in vs))
    elif front:
        parts.append(f"變體寫在名稱前面（{front}）")
    style = f" → {'、'.join(f'`{x}`' for x in ids)}" if ids else ""
    return (f"- **{info['name']}** `{prefix}` — {zh or '（待補中文說明）'}{style} · "
            + " · ".join(parts) + f" · https://icon-sets.iconify.design/{prefix}/")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="report changes without writing files")
    args = ap.parse_args()

    try:
        all_sets = get_json(f"{CDN}/@iconify/collections/collections.json")
    except sources.SourceError:
        try:
            all_sets = get_json("https://api.iconify.design/collections")
        except sources.SourceError as e:
            sys.exit(f"could not fetch the Iconify set list ({e})")
    sets = {p: i for p, i in all_sets.items()
            if i.get("license", {}).get("spdx") in sources.SPDX_OK
            and i.get("category") != "Archive / Unmaintained" and not i.get("hidden")}
    translations = json.loads(TRANSLATIONS.read_text(encoding="utf-8")) if TRANSLATIONS.exists() else {}
    known = translations.get("icon-sets", {})
    new = sorted(p for p in sets if p not in known)
    gone = sorted(set(known) - set(sets))
    print(f"Iconify: {len(sets)} usable sets of {len(all_sets)}, {len(new)} without Chinese, {len(gone)} no longer listed")
    for p in gone:
        print(f"  removed or no longer allowed: {p}")
    if args.check:
        return

    extra, failed = {}, []
    for n, p in enumerate(sets, 1):
        try:
            extra[p] = variants(p)
        except sources.SourceError as e:
            failed.append(f"{p} ({e})")
            extra[p] = ([], "")
        print(f"\r  reading variants {n}/{len(sets)}", end="", flush=True)
        time.sleep(PAUSE)
    print()
    if failed:
        print(f"  variants unknown for {len(failed)} set(s), run again later: {', '.join(failed)}")

    lines = [
        "# Iconify 圖示集",
        "",
        f"可以商用的 Iconify 圖示集，由 `scripts/sync_icon_sets.py` 從 Iconify 公開的圖示集清單產生，"
        f"{datetime.date.today():%Y-%m-%d} 同步，共 {len(sets)} 套。只收名稱、數量、授權與連結，不含圖示本身。",
        "",
        "已用和 `search.py` 相同的白名單過濾：MIT、ISC、Apache-2.0、BSD-3-Clause、Unlicense、OFL-1.1、CC0、CC BY。"
        "GPL、MPL、CC BY-SA、CC BY-NC，以及停止維護的圖示集不在這裡。",
        "",
        "格式：`**名稱** \\`prefix\\` — 中文說明 → 對應風格 id · 數量 · 授權 · 格線與樣式 · 變體 · 官方頁面`。"
        "prefix 用在 `search.py --prefixes`；變體用在 `--variant`（`base`＝沒有後綴的預設版）。"
        "官方頁面可以直接瀏覽整套圖示。",
    ]
    for cat, label in SECTIONS.items():
        group = sorted((p for p, i in sets.items() if (i.get("category") or "") == cat),
                       key=lambda p: -sets[p]["total"])
        if not group:
            continue
        lines += ["", f"## {label}" + (f"（{cat}）" if cat else ""), ""]
        if cat in NOTES:
            lines += [NOTES[cat], ""]
        lines += [describe(p, sets[p], known, extra[p]) for p in group]
    (CATALOG / "icon-sets.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {CATALOG / 'icon-sets.md'}")

    if new:
        print("\nAdd these to catalog/translations.json under \"icon-sets\", then run again:")
        for p in new:
            print(f"  {p} — {sets[p]['name']} ({sets[p].get('category', '')})")


if __name__ == "__main__":
    main()
