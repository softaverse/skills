#!/usr/bin/env python3
"""One composition per storyboard animation, with this episode's content baked in as defaults.

    instances.py <episode-dir> [--studio <hf-studio>] [--dry-run]

Run after B4 (every component is built) and again whenever the storyboard changes (a B3
re-run, edited vars). For each cutaway / transition / overlay it writes
<episode>/<slot> (Seg_06.o1 → seg_06-o1, Seg_05's transition → seg_05-transition):

  - a copy of the source composition (reuse.from, reuse.as, or the custom build itself);
  - the variable defaults replaced by the slot's vars, plus — for kit components — the measured
    `duration`, the episode `theme`, the overlay `placement` and `motion` overrides;
  - a manifest with `instance: {of, slot}` so the Gallery shows it and this script can clean up.

Nothing about layout or motion changes, so an instance is exactly as correct as the component
it copies (already verified) with data that `storyboard.py check` already validated.
Custom builds that live at the slot path already (e.g. EP3-stitch/seg_03) are updated in place.
Instances whose slot no longer exists are removed. Never edit an instance by hand — edit the
storyboard (or the component) and re-run.
"""

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from storyboard import animations_of, find_studio, motion_entries, reuse_of, slot_dir  # noqa: E402
from ytlib import load_json  # noqa: E402

VARS_RE = re.compile(r"data-composition-variables='([^']*)'")
NOTE = "<!-- 由 youtube-production instances.py 產生（{slot} ← {src}）。不要手改：改分鏡表或元件後重跑。 -->"


def relink(dst, src):
    """Copied relative symlinks point one level off; re-point each at what it meant in the source."""
    for link in [p for p in dst.rglob("*") if p.is_symlink()]:
        rel = link.relative_to(dst)
        target = os.path.realpath(src / rel)
        link.unlink()
        link.symlink_to(os.path.relpath(target, link.parent))


def meta_first(html):
    """Put <meta charset> right after the doctype, before <html>.

    The variables live on <html data-composition-variables='…'>, which easily pushes a <meta charset>
    inside <head> past the first 1024 bytes — where browsers stop looking for it. Without a charset
    header (HyperFrames' snapshot / render server) the browser then guesses, and a file whose first
    1 KB is mostly ASCII renders its Chinese as mojibake. A meta before <html> is valid HTML (the
    later <html> tag's attributes still land on the root); a BOM is not an option because the
    renderer rewrites the file and the BOM ends up mid-document (quirks mode).
    """
    if html.startswith("\ufeff"):
        html = html[1:]
    if re.match(r"<!DOCTYPE html>\s*<meta charset", html, re.I):
        return html
    html = re.sub(r"\s*<meta charset=\"[^\"]*\">", "", html, count=1)
    return re.sub(r"(<!DOCTYPE html>)\s*", r'\1\n<meta charset="UTF-8">\n', html, count=1, flags=re.I)


def bake(html, values):
    """Replace variable defaults in <html data-composition-variables>; returns (html, declared ids)."""
    m = VARS_RE.search(html)
    if not m:
        return html, set()
    declared = json.loads(m.group(1))
    for v in declared:
        if v.get("id") in values:
            v["default"] = values[v["id"]]
    js = json.dumps(declared, ensure_ascii=False).replace("'", "&#39;")
    return html[:m.start(1)] + js + html[m.end(1):], {v.get("id") for v in declared}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--studio")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ep = Path(args.episode).resolve()
    sb = load_json(ep / "storyboard.json")
    studio = find_studio(args.studio, ep)
    comps = studio / "compositions"
    episode = sb.get("episode", ep.name)
    theme = sb.get("theme", "channel")

    wanted, rows = set(), []
    for seg in sb["segments"]:
        seg_dur = (seg.get("timing") or {}).get("dur")
        for slot, layer, anim in animations_of(seg):
            r = reuse_of(anim)
            src_rel = r["from"] if r["mode"] in ("as-is", "variables") else (r["as"] or slot_dir(episode, slot))
            dst_rel = slot_dir(episode, slot)
            src, dst = comps / src_rel, comps / dst_rel
            if not (src / "index.html").exists():
                rows.append((slot, src_rel, "skipped — source not built")); continue
            manifest = load_json(src / "manifest.json") if (src / "manifest.json").exists() else {}
            is_kit = "kit" in manifest
            dur = (anim.get("timing") or {}).get("dur") if layer == "overlay" else \
                  (anim.get("dur") if layer == "transition" else seg_dur)
            values = dict(anim.get("vars") or {})
            if is_kit:
                if dur is not None:
                    values["duration"] = round(dur, 3)
                values["theme"] = theme
                if layer == "overlay" and anim.get("placement"):
                    values["placement"] = anim["placement"]
                overrides = {m["recipe"]: m["params"] for m in motion_entries(anim) if m["params"]}
                if overrides:
                    values["motion"] = json.dumps(overrides, ensure_ascii=False)
            wanted.add(dst_rel)
            in_place = src.resolve() == dst.resolve()
            if args.dry_run:
                rows.append((slot, src_rel, "update in place" if in_place else f"→ {dst_rel}")); continue
            if not in_place:
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst, symlinks=True, ignore=shutil.ignore_patterns(".hyperframes", "storyboard"))
                relink(dst, src)
            html = (dst / "index.html").read_text(encoding="utf-8")
            html, declared = bake(meta_first(html), values)
            missing = sorted(set(values) - declared)
            if not in_place:
                html = re.sub(r"<!-- 由 youtube-production instances\.py 產生.*?-->\n", "", html)
                html = html.replace("<head>", "<head>\n" + NOTE.format(slot=slot, src=src_rel), 1)
            (dst / "index.html").write_text(html, encoding="utf-8")
            if manifest:
                for v in manifest.get("variables", []):
                    if v.get("id") in values:
                        v["default"] = values[v["id"]]
                if not in_place:
                    # Name after what this slot shows, not after the source's own demo copy
                    if layer == "overlay":
                        text = next((str(values[k]) for k in ("text", "title") if values.get(k)), anim.get("at", ""))
                        label = f"標註「{text}」"
                    elif layer == "transition":
                        label = f"轉場（{src_rel}）"
                    else:
                        label = seg.get("visual", "")[:40]
                    manifest["description"] = f"{src_rel} 的實例：{manifest.get('name', src_rel)}"
                    manifest["name"] = f"{slot}｜{label}"
                    manifest["instance"] = {"of": src_rel, "slot": slot}
                    manifest.pop("kit", None) if not is_kit else None
                (dst / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            note = "updated in place" if in_place else f"→ {dst_rel}"
            if missing:
                note += f" (not declared, left out: {', '.join(missing)})"
            rows.append((slot, src_rel, note))

    removed = []
    for mf in (comps / episode).glob("*/manifest.json"):
        rel = mf.parent.relative_to(comps).as_posix()
        try:
            inst = load_json(mf).get("instance")
        except json.JSONDecodeError:
            continue
        if inst and rel not in wanted:
            removed.append(rel)
            if not args.dry_run:
                shutil.rmtree(mf.parent)

    for slot, src, note in rows:
        print(f"{slot:<22} {src:<34} {note}")
    print(f"— {len(rows)} slots · {len(removed)} stale instances removed{' (dry run)' if args.dry_run else ''}")
    for r in removed:
        print(f"  removed {r}")


if __name__ == "__main__":
    main()
