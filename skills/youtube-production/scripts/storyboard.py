#!/usr/bin/env python3
"""Validate an episode storyboard and derive its lists.

    storyboard.py estimate <episode-dir|script.md>    spoken length per section and total
    storyboard.py check <episode-dir> [--write]       validate storyboard.json against script.md,
                                                      kinds.json and the source manifests;
                                                      --write fills timing.est per segment
    storyboard.py lists <episode-dir>                 write animations.md and assets.md
    storyboard.py recipes [<episode-dir>]             recipes available per element type (targets)

<episode-dir> holds script.md and storyboard.json. hf-studio is found from --studio,
HF_STUDIO, or by walking up from the episode dir to the folder holding kinds.json.
`check` exits 1 when there are errors.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ytlib import dump_json, load_json, normalize, parse_script  # noqa: E402

CHARS_PER_SEC = 4.5
LINE_PAUSE = 0.3
PICTURES = {"camera", "screen", "broll", "cutaway"}
MODES = {"as-is", "variables", "fork", "new"}
PLACEMENTS = {"top-left", "top-right", "bottom-left", "bottom-right",
              "left-third", "right-third", "lower-third", "center"}
ASSET_TYPES = {"screen", "broll", "image", "logo", "audio"}
SEG_ID = re.compile(r"^Seg_\d{2,3}[a-z]?$")
# Share of running time per picture tier: (min, max). Override per episode with "mix".
DEFAULT_MIX = {"footage": (0.60, 0.70), "template": (0.20, 0.30), "custom": (0.05, 0.10)}
MIX_LABELS = {"footage": "實拍（操作畫面、螢幕錄影）", "template": "模板化動態圖形", "custom": "客製化動畫"}
ZOOM_TYPES = {"zoom", "highlight"}


def spoken_units(text):
    """CJK characters count 1, Latin words 1.2, digits 1 each."""
    cjk = len(re.findall(r"[㐀-鿿]", text))
    latin = len(re.findall(r"[A-Za-z]+", text))
    digits = len(re.findall(r"\d", text))
    return cjk + 1.2 * latin + digits


def text_width(text):
    """Rough rendered width in em: CJK / full-width 1, everything else 0.55."""
    return sum(1 if ord(ch) > 0x2E80 else 0.55 for ch in text)


def estimate_seconds(lines):
    return round(sum(spoken_units(l["spoken"]) for l in lines) / CHARS_PER_SEC
                 + LINE_PAUSE * len(lines), 1)


def find_studio(arg, start):
    if arg or os.environ.get("HF_STUDIO"):
        return Path(os.path.expanduser(arg or os.environ["HF_STUDIO"]))
    for p in [start, *start.parents]:
        if (p / "kinds.json").exists():
            return p
    return Path(os.path.expanduser("~/Workspace/hyperframes/hf-studio"))


def fmt_dur(s):
    m, sec = divmod(round(s), 60)
    return f"{m}:{sec:02d}"


# ── estimate ────────────────────────────────────────────────────────────────


def cmd_estimate(args):
    p = Path(args.path)
    script = p / "script.md" if p.is_dir() else p
    lines = parse_script(script)
    sections = {}
    for l in lines:
        sections.setdefault(l["section"] or "(none)", []).append(l)
    print("| Section | Lines | Est |\n|---|---|---|")
    for name, ls in sections.items():
        print(f"| {name} | {ls[0]['id']}–{ls[-1]['id']} | {fmt_dur(estimate_seconds(ls))} |")
    print(f"| **Total** | {len(lines)} | **{fmt_dur(estimate_seconds(lines))}** |")
    long = [l for l in lines if spoken_units(l["spoken"]) > 40]
    for l in long:
        print(f"⚠ {l['id']} is long ({spoken_units(l['spoken']):.0f} units) — hard to record in one take")


# ── check ───────────────────────────────────────────────────────────────────


def animations_of(seg):
    """(slot id, expected layer, animation dict) for everything a segment animates."""
    out = []
    if seg.get("animation"):
        out.append((seg["id"], "cutaway", seg["animation"]))
    if seg.get("transition_in"):
        out.append((f"{seg['id']} (transition)", "transition", seg["transition_in"]))
    for ov in seg.get("overlays", []):
        out.append((ov.get("id", f"{seg['id']}.o?"), "overlay", ov))
    return out


def reuse_of(anim):
    """Transitions may use the short form {mode, from, dur}."""
    r = anim.get("reuse") or {}
    return {"mode": r.get("mode", anim.get("mode")), "from": r.get("from", anim.get("from")),
            "why": r.get("why", anim.get("why")), "ref": r.get("ref", []), "as": r.get("as")}


COMMON_PARAMS = {"speed": {"min": 0.5, "max": 2.0, "label": "速度", "fmt": "×{}"},
                 "color": {"label": "顏色", "fmt": "{}"}}
COLOR_RE = re.compile(r"^(#[0-9a-fA-F]{3,8}|[a-z][a-z0-9-]*)$")
_recipes = {}


def load_recipe(studio, rid):
    """{id, name, status, role, params, use} from recipes/<id>/RECIPE.md, or None."""
    key = (str(studio), rid)
    if key not in _recipes:
        f = Path(studio) / "recipes" / rid / "RECIPE.md"
        if not f.exists():
            _recipes[key] = None
        else:
            text = f.read_text(encoding="utf-8")
            field = lambda k: (re.search(rf"^{k}:\s*(.+)$", text, re.M) or [None, ""])[1].strip()
            try:
                params = json.loads(field("params") or "{}")
            except json.JSONDecodeError:
                params = {}
            body = text.split("---", 2)[-1]
            use = next((l.strip() for l in body.splitlines() if l.strip() and not l.startswith(("#", "|"))), "")
            targets = [t.strip() for t in field("targets").strip("[]").split(",") if t.strip()]
            _recipes[key] = {"id": rid, "name": field("name").split(" ")[0] or rid, "status": field("status") or "draft",
                             "role": field("role"), "params": params, "use": use, "targets": targets}
    return _recipes[key]


TARGET_NAMES = {"eyebrow": "眉標", "title": "標題／副標", "sentence": "句子", "keyword": "關鍵詞",
                "cards": "卡片群／節點", "number": "數字", "line": "連接線", "ghost": "背景大字"}


def all_recipes(studio):
    root = Path(studio) / "recipes"
    return [r for r in (load_recipe(studio, d.name) for d in sorted(root.iterdir()) if (d / "RECIPE.md").exists()) if r] \
        if root.is_dir() else []


def cmd_recipes(args):
    """Which recipes each element type can use — the menu A4 picks `motion` from."""
    start = Path(args.episode).resolve() if args.episode else Path.cwd()
    studio = find_studio(args.studio, start)
    recs = all_recipes(studio)
    if not recs:
        sys.exit(f"no recipes under {studio / 'recipes'}")
    by = {}
    for r in recs:
        for t in r["targets"] or ["?"]:
            by.setdefault(t, []).append(r)
    order = [*TARGET_NAMES, *sorted(set(by) - set(TARGET_NAMES))]
    print("| 元素 | target | 配方（狀態） |\n|---|---|---|")
    for t in order:
        if t in by:
            items = "、".join(f"{r['name']} `{r['id']}`（{r['status']}）" for r in by[t])
            print(f"| {TARGET_NAMES.get(t, t)} | `{t}` | {items} |")


def motion_entries(anim):
    """`motion` items as {recipe, params}; a bare string is a recipe with no overrides."""
    return [{"recipe": m, "params": {}} if isinstance(m, str) else {"recipe": m.get("recipe"), "params": m.get("params") or {}}
            for m in anim.get("motion", [])]


def check_motion(slot, anim, studio, errors, warnings):
    for m in motion_entries(anim):
        rec = load_recipe(studio, m["recipe"])
        if not rec:
            errors.append(f"{slot}: no recipe '{m['recipe']}' in {Path(studio) / 'recipes'}")
            continue
        if rec["status"] != "accepted":
            warnings.append(f"recipe '{m['recipe']}' is {rec['status']}, not accepted yet")
        for k, v in m["params"].items():
            spec = rec["params"].get(k) or COMMON_PARAMS.get(k)
            if spec is None:
                errors.append(f"{slot}: recipe '{m['recipe']}' has no parameter '{k}' "
                              f"(has {', '.join([*rec['params'], *COMMON_PARAMS])})")
            elif k == "color":
                if not isinstance(v, str) or not COLOR_RE.match(v):
                    errors.append(f"{slot}: color must be a theme token name (accent-soft) or #hex, got {v!r}")
            elif "options" in spec and v not in spec["options"]:
                errors.append(f"{slot}: {m['recipe']}.{k} must be one of {spec['options']}, got {v!r}")
            elif "min" in spec and (not isinstance(v, (int, float)) or not spec["min"] <= v <= spec["max"]):
                errors.append(f"{slot}: {m['recipe']}.{k} = {v!r} outside {spec['min']}–{spec['max']}")


def motion_label(anim, studio):
    """Display: 標題上浮 → 卡片依序淡入（位移 24px、速度 ×1.2）＋ 浮水印緩慢平移"""
    fg, bg = [], []
    for m in motion_entries(anim):
        rec = load_recipe(studio, m["recipe"]) or {"name": m["recipe"], "params": {}, "role": ""}
        notes = []
        for k, v in m["params"].items():
            spec = rec["params"].get(k) or COMMON_PARAMS.get(k, {})
            fmt = spec.get("fmt") or ("{}" + spec.get("unit", ""))
            notes.append(f"{spec.get('label', k)} {fmt.format(v)}")
        label = rec["name"] + (f"（{'、'.join(notes)}）" if notes else "")
        (bg if rec.get("role") == "background" else fg).append(label)
    return " → ".join(fg) + "".join(f" ＋ {b}" for b in bg)


def slot_dir(episode, slot):
    """Where a custom build lives: 'Seg_06.o1' → '<episode>/seg_06-o1'."""
    return f"{episode}/{slot.split(' ')[0].lower().replace('.', '-')}" + ("-transition" if "transition" in slot else "")


def planned_builds(sb):
    """{composition path: slot} for every `as` a new/fork animation will create."""
    planned = {}
    for seg in sb.get("segments", []):
        for slot, _, anim in animations_of(seg):
            target = reuse_of(anim)["as"]
            if target:
                planned.setdefault(target, []).append(slot)
    return planned


def tier_of(seg):
    """footage: real picture (overlays and zooms ride on it) · template: reused or kit
    composition · custom: one-off fork / new."""
    if seg.get("picture") != "cutaway":
        return "footage"
    r = reuse_of(seg.get("animation") or {})
    # building a kit piece is template work; building an episode-only piece is custom, even if reused later
    return "template" if r["mode"] in ("as-is", "variables") or (r["as"] or "").startswith("kit/") else "custom"


def mix_of(sb):
    """({tier: seconds}, total) using measured dur when present, else est."""
    secs = {k: 0.0 for k in DEFAULT_MIX}
    for seg in sb.get("segments", []):
        t = seg.get("timing", {})
        secs[tier_of(seg)] += t.get("dur", t.get("est", 0)) or 0
    return secs, sum(secs.values())


def mix_report(sb):
    secs, total = mix_of(sb)
    target = {**DEFAULT_MIX, **{k: tuple(v) for k, v in sb.get("mix", {}).items()}}
    rows, off = [], []
    for k, (lo, hi) in target.items():
        share = secs[k] / total if total else 0
        ok = lo <= share <= hi
        rows.append(f"| {MIX_LABELS[k]} | {fmt_dur(secs[k])} | {share:.0%} | {lo:.0%}–{hi:.0%} | {'✓' if ok else '✗'} |")
        if not ok:
            off.append(f"{MIX_LABELS[k]} {share:.0%} (target {lo:.0%}–{hi:.0%})")
    return ["| 類型 | 時間 | 佔比 | 目標 | |", "|---|---|---|---|---|", *rows], off


def cmd_check(args):
    ep = Path(args.episode)
    lines = parse_script(ep / "script.md")
    by_id = {l["id"]: l for l in lines}
    order = {l["id"]: i for i, l in enumerate(lines)}
    sb = load_json(ep / "storyboard.json")
    studio = find_studio(args.studio, ep.resolve())
    comps = studio / "compositions"
    kinds = load_json(studio / "kinds.json") if (studio / "kinds.json").exists() else None
    layers = {k["id"] for k in kinds["layers"]} if kinds else set()
    purposes = {k["id"] for k in kinds["purposes"]} if kinds else set()
    errors, warnings = [], []
    if not kinds:
        warnings.append(f"kinds.json not found under {studio} — kind ids not checked")

    planned = planned_builds(sb)
    for target, slots in planned.items():
        if len(slots) > 1:
            errors.append(f"{', '.join(slots)}: all build `as` {target} — build it once, reuse it elsewhere")
        # Only a planning error: after Stage B has built it, the composition existing is the point.
        measured = any("dur" in (seg.get("timing") or {}) for seg in sb.get("segments", []))
        if (comps / target / "manifest.json").exists() and not measured:
            errors.append(f"{slots[0]}: `as` {target} already exists — pick a new path or reuse it")
    style = sb.get("style", "../DESIGN.md")
    theme = sb.get("theme", "channel")
    own_style = Path(style).name == "DESIGN.md" and not style.startswith("..")
    episode_dir = ep.resolve().name
    seen_seg, seen_line, last = set(), {}, -1
    for seg in sb.get("segments", []):
        sid = seg.get("id", "?")
        if not SEG_ID.match(sid):
            errors.append(f"{sid}: id must look like Seg_01 (or Seg_01b)")
        if sid in seen_seg:
            errors.append(f"{sid}: duplicate segment id")
        seen_seg.add(sid)

        refs = seg.get("script") or []
        if not refs:
            errors.append(f"{sid}: no script lines")
        for lid in refs:
            if lid not in by_id:
                errors.append(f"{sid}: unknown line {lid}")
                continue
            if lid in seen_line:
                errors.append(f"{sid}: {lid} already belongs to {seen_line[lid]}")
            seen_line[lid] = sid
            if order[lid] <= last:
                errors.append(f"{sid}: {lid} is out of script order")
            last = max(last, order[lid])
        seg_lines = [by_id[l] for l in refs if l in by_id]
        seg_text = normalize(" ".join(l["spoken"] for l in seg_lines))

        pic = seg.get("picture")
        if pic not in PICTURES:
            errors.append(f"{sid}: picture must be one of {sorted(PICTURES)}")
        if pic == "cutaway" and not seg.get("animation"):
            errors.append(f"{sid}: cutaway segment needs an animation")
        if pic != "cutaway" and seg.get("animation"):
            errors.append(f"{sid}: animation is only for picture=cutaway — use overlays")
        if not seg.get("visual"):
            warnings.append(f"{sid}: no visual description")
        if pic in ("screen", "broll") and not seg.get("assets"):
            warnings.append(f"{sid}: {pic} segment lists no assets to record")
        for a in seg.get("assets", []):
            if a.get("type") not in ASSET_TYPES:
                errors.append(f"{sid}: asset type must be one of {sorted(ASSET_TYPES)}")

        for slot, layer, anim in animations_of(seg):
            kind = anim.get("kind") or {}
            if layer != "transition" or kind:
                if kind.get("layer") != layer:
                    errors.append(f"{slot}: kind.layer must be {layer}")
                elif layers and kind["layer"] not in layers:
                    errors.append(f"{slot}: unknown layer {kind['layer']}")
                for p in kind.get("purpose", []):
                    if purposes and p not in purposes:
                        errors.append(f"{slot}: unknown purpose {p}")
            r = reuse_of(anim)
            if r["mode"] not in MODES:
                errors.append(f"{slot}: reuse.mode must be one of {sorted(MODES)}")
                continue
            if layer != "transition" and not r["why"]:
                warnings.append(f"{slot}: reuse.why is empty")
            if r["as"] and r["mode"] not in ("new", "fork"):
                errors.append(f"{slot}: `as` only applies to new / fork")
            if r["mode"] == "new":
                warnings.append(f"{slot}: new animation — {r['why'] or 'no reason given'}")
                if not anim.get("elements"):
                    warnings.append(f"{slot}: new animation lists no elements")
            elif not r["from"]:
                errors.append(f"{slot}: reuse.from is required for mode {r['mode']}")
                continue
            # Which manifest the vars belong to: the source for as-is / variables; for new / fork the
            # composition the build creates (`as`, or <episode>/<slot>) once it exists.
            if r["mode"] in ("as-is", "variables"):
                target = r["from"]
                mf = comps / target / "manifest.json"
                if target in planned and not mf.exists():
                    target = None  # built in this episode; vars are checked once it exists
                elif not mf.exists():
                    errors.append(f"{slot}: {target} has no manifest.json in {comps}")
                    continue
            else:
                if r["mode"] == "fork":
                    if r["from"] in planned and not (comps / r["from"] / "manifest.json").exists():
                        errors.append(f"{slot}: fork of {r['from']}, which this episode builds — reuse it with variables")
                    elif not (comps / r["from"] / "manifest.json").exists():
                        errors.append(f"{slot}: {r['from']} has no manifest.json in {comps}")
                    if not (anim.get("elements") or anim.get("constraints")):
                        warnings.append(f"{slot}: fork without elements/constraints — what changes?")
                target = r["as"] or slot_dir(episode_dir, slot)
                if not (comps / target / "manifest.json").exists():
                    target = None
            if target:
                declared = {v["id"]: v for v in load_json(comps / target / "manifest.json").get("variables", []) if v.get("id")}
                is_kit = target.startswith("kit/") or "duration" in declared and "theme" in declared
                for key, val in (anim.get("vars") or {}).items():
                    if key not in declared:
                        errors.append(f"{slot}: {target} declares no variable '{key}'")
                        continue
                    default, cap = declared[key].get("default"), declared[key].get("max")
                    if is_kit and key in ("duration", "theme"):
                        errors.append(f"{slot}: don't set '{key}' — Stage B fills duration from the segment "
                                      f"length, theme comes from the storyboard's \"theme\"")
                    if isinstance(val, str) and isinstance(cap, (int, float)):
                        if len(val.replace("*", "")) > cap:
                            errors.append(f"{slot}: '{key}' has {len(val.replace('*', ''))} chars, "
                                          f"{target} fits at most {cap}")
                    elif isinstance(val, str) and isinstance(default, str) and default and \
                            text_width(val) > text_width(default) * 1.5 + 2:
                        warnings.append(f"{slot}: '{key}' is ~{text_width(val):.0f} em wide vs default "
                                        f"~{text_width(default):.0f} — may overflow")
                if is_kit:
                    themes = [o.get("value") for o in declared.get("theme", {}).get("options", [])]
                    if themes and theme not in themes:
                        errors.append(f"{slot}: {target} has no theme '{theme}' (has {', '.join(themes)})")
            if r["mode"] == "variables" and not anim.get("vars"):
                warnings.append(f"{slot}: mode variables but no vars — is it as-is?")
            if own_style and r["mode"] in ("as-is", "variables") and r["from"] \
                    and r["from"] not in planned and not r["from"].startswith(episode_dir + "/") \
                    and not r["from"].startswith("kit/"):
                warnings.append(f"{slot}: this episode has its own style; {r['from']} is drawn in "
                                f"another — fork to restyle unless it is themeable")
            if anim.get("cues") and layer != "overlay":
                warnings.append(f"{slot}: cues inside a {layer} — animations follow the segment length; "
                                f"put word-timed emphasis in an overlay or a cut instead")
            check_motion(slot, anim, studio, errors, warnings)
            if r["mode"] in ("fork", "new") and not r["as"] and not anim.get("motion"):
                warnings.append(f"{slot}: custom {r['mode']} with no `motion` — pick recipes so the build doesn't improvise")
            for c in anim.get("cues", []):
                if normalize(c.get("at", "")) not in seg_text:
                    errors.append(f"{slot}: cue phrase '{c.get('at')}' not in {sid}'s lines")

        for ov in seg.get("overlays", []):
            oid = ov.get("id", "?")
            if not oid.startswith(f"{sid}.o"):
                errors.append(f"{oid}: overlay id must be {sid}.o<n>")
            if normalize(ov.get("at", "")) not in seg_text:
                errors.append(f"{oid}: 'at' phrase '{ov.get('at')}' not in {sid}'s lines")
            if ov.get("placement") not in PLACEMENTS:
                errors.append(f"{oid}: placement must be one of {sorted(PLACEMENTS)}")
            elif pic == "camera" and ov["placement"] == "center":
                warnings.append(f"{oid}: centered overlay on a camera segment covers the face")
            if not isinstance(ov.get("dur"), (int, float)):
                errors.append(f"{oid}: dur (seconds) is required")

        for z in seg.get("zooms", []):
            if pic == "cutaway":
                errors.append(f"{sid}: zooms are for footage, not cutaways")
            if z.get("type", "zoom") not in ZOOM_TYPES:
                errors.append(f"{sid}: zoom type must be one of {sorted(ZOOM_TYPES)}")
            if normalize(z.get("at", "")) not in seg_text:
                errors.append(f"{sid}: zoom 'at' phrase '{z.get('at')}' not in {sid}'s lines")
            if not z.get("target"):
                errors.append(f"{sid}: zoom needs a target (what to enlarge)")

        est = estimate_seconds(seg_lines) if seg_lines else 0
        if pic == "cutaway" and seg_lines and not 2 <= est <= 20:
            warnings.append(f"{sid}: cutaway estimated at {est}s — "
                            f"{'too short to read' if est < 2 else 'long for one static scene'}")
        if args.write:
            seg.setdefault("timing", {})["est"] = est

    for l in lines:
        if l["id"] not in seen_line:
            errors.append(f"{l['id']} is in no segment")

    pending = sorted({w.split("'")[1] for w in warnings if w.startswith("recipe '") and "not accepted" in w})
    warnings = [w for w in warnings if not (w.startswith("recipe '") and "not accepted" in w)]
    if pending:
        warnings.append(f"{len(pending)} recipes not accepted yet: {', '.join(pending)}")
    table, off = mix_report(sb) if not errors else ([], [])
    for o in off:
        warnings.append(f"picture mix: {o}")
    if args.write:
        dump_json(sb, ep / "storyboard.json")
    if table:
        print("\n".join(table) + "\n")
    for w in warnings:
        print(f"⚠ {w}")
    for e in errors:
        print(f"✗ {e}")
    n = len(sb.get("segments", []))
    total = estimate_seconds(lines)
    print(f"{n} segments · {len(lines)} lines · est {fmt_dur(total)} · "
          f"{len(errors)} errors · {len(warnings)} warnings{' · timing.est written' if args.write else ''}")
    sys.exit(1 if errors else 0)


# ── lists ───────────────────────────────────────────────────────────────────


def cmd_lists(args):
    ep = Path(args.episode)
    lines = {l["id"]: l for l in parse_script(ep / "script.md")}
    sb = load_json(ep / "storyboard.json")

    def line_span(seg):
        ids = seg.get("script") or []
        return f"{ids[0]}–{ids[-1]}" if len(ids) > 1 else (ids[0] if ids else "")

    planned = planned_builds(sb)
    studio = find_studio(getattr(args, "studio", None), ep.resolve())
    groups = {"reuse": [], "fork": [], "new": []}
    used_recipes = []
    for seg in sb["segments"]:
        for _, _, anim in animations_of(seg):
            for m in motion_entries(anim):
                if m["recipe"] not in used_recipes:
                    used_recipes.append(m["recipe"])
    for seg in sb["segments"]:
        for slot, layer, anim in animations_of(seg):
            r = reuse_of(anim)
            kind = anim.get("kind") or {}
            kind_s = f"{kind.get('layer', layer)}/{','.join(kind.get('purpose', []))}".rstrip("/")
            row = {"slot": slot, "lines": line_span(seg), "kind": kind_s, "r": r, "anim": anim,
                   "visual": seg.get("visual", "") if layer == "cutaway" else ""}
            groups["reuse" if r["mode"] in ("as-is", "variables") else r["mode"]].append(row)

    def motion_s(anim, r):
        if anim.get("motion"):
            return motion_label(anim, studio)
        src = r["from"] if r["mode"] in ("as-is", "variables") else r["as"]
        return "（kit 內建）" if (src or "").startswith("kit/") else "（沿用原動畫）"

    def vars_s(anim):
        return "<br>".join(f"`{k}`: {v}" for k, v in (anim.get("vars") or {}).items()) or "—"

    def elems_s(anim):
        items = [e.get("label") or e.get("type", "") for e in anim.get("elements", [])]
        cons = anim.get("constraints", [])
        return "<br>".join([" · ".join(items)] * bool(items) + [f"⚠ {c}" for c in cons]) or "—"

    def as_s(r):
        if not r["as"]:
            return "—"
        uses = sum(1 for g in groups["reuse"] if g["r"]["from"] == r["as"])
        return f"`{r['as']}`" + (f" · reused ×{uses}" if uses else "")

    total = sum(len(g) for g in groups.values())
    md = [f"# Animations — {sb.get('episode', ep.name)}", "",
          "Generated from storyboard.json by `storyboard.py lists` — edit the storyboard, not this file.", "",
          f"**{total} animations** · reuse {len(groups['reuse'])} · fork {len(groups['fork'])} · "
          f"new {len(groups['new'])}", "", "## Picture mix", "", *mix_report(sb)[0], ""]
    mode_zh = {"as-is": "直接用", "variables": "改參數", "fork": "fork", "new": "新做"}
    pic_zh = {"screen": "螢幕錄影", "broll": "B-roll", "camera": "露臉", "cutaway": "cutaway"}
    md += ["## 分鏡總表", "", "| Seg | 句子 | 畫面 | 動畫（來源・模式） | 動態（配方） | 長度 |", "|---|---|---|---|---|---|"]
    for seg in sb["segments"]:
        t = seg.get("timing", {})
        length = f"{t.get('dur', t.get('est', 0)):.1f}s"
        pic = pic_zh.get(seg.get("picture"), seg.get("picture"))
        if seg.get("animation"):
            r = reuse_of(seg["animation"])
            src = r["from"] if r["mode"] in ("as-is", "variables") else (r["as"] or r["from"] or "—")
            md.append(f"| {seg['id']} | {line_span(seg)} | {pic} | `{src}`・{mode_zh[r['mode']]} | "
                      f"{motion_s(seg['animation'], r)} | {length} |")
        else:
            md.append(f"| {seg['id']} | {line_span(seg)} | {pic} | — | — | {length} |")
        for ov in seg.get("overlays", []):
            r = reuse_of(ov)
            src = r["from"] if r["mode"] in ("as-is", "variables") else (r["as"] or r["from"] or "—")
            text = (ov.get("vars") or {}).get("text") or (ov.get("vars") or {}).get("title") or ov.get("at")
            md.append(f"| ↳ {ov['id']} | 「{ov['at']}」 | 標註「{text}」 | `{src}`・{mode_zh[r['mode']]} | "
                      f"{motion_s(ov, r)} | {ov.get('timing', {}).get('dur', ov.get('dur', 0)):.1f}s |")
    md.append("")
    if used_recipes:
        md += ["## 配方說明", ""]
        for rid in used_recipes:
            rec = load_recipe(studio, rid)
            if not rec:
                md.append(f"- **{rid}**：找不到這個配方")
                continue
            demo = (f" ▶ [看示範](http://localhost:3025/app/player.html?c=recipes/{rid})"
                    if rec["status"] in ("built", "accepted") else f"（{rec['status']}，尚無示範）")
            alts = [a["name"] for a in all_recipes(studio)
                    if a["id"] != rid and set(a["targets"]) & set(rec["targets"])]
            alt = f"　同類可替換：{'、'.join(alts)}" if alts else ""
            md.append(f"- **{rec['name']}** `{rid}`：{rec['use']}{demo}{alt}")
        md.append("")
    if groups["reuse"]:
        md += ["## Reuse (as-is / variables)", "",
               "| Slot | Lines | Kind | From | Mode | Motion | Values |", "|---|---|---|---|---|---|---|"]
        md += [f"| {r['slot']} | {r['lines']} | {r['kind']} | `{r['r']['from']}`"
               f"{' (built by ' + planned[r['r']['from']][0] + ')' if r['r']['from'] in planned else ''} | "
               f"{r['r']['mode']} | {motion_s(r['anim'], r['r'])} | {vars_s(r['anim'])} |" for r in groups["reuse"]]
        md.append("")
    if groups["fork"]:
        md += ["## Fork (copy, then modify)", "",
               "| Slot | Lines | Kind | From | Builds | Motion | What changes | Visual |", "|---|---|---|---|---|---|---|---|"]
        md += [f"| {r['slot']} | {r['lines']} | {r['kind']} | `{r['r']['from']}` | {as_s(r['r'])} | "
               f"{motion_s(r['anim'], r['r'])} | {elems_s(r['anim'])} | {r['visual']} |" for r in groups["fork"]]
        md.append("")
    if groups["new"]:
        md += ["## New", "", "| Slot | Lines | Kind | Builds | Motion | Elements | Refs | Why new |",
               "|---|---|---|---|---|---|---|---|"]
        md += [f"| {r['slot']} | {r['lines']} | {r['kind']} | {as_s(r['r'])} | {motion_s(r['anim'], r['r'])} | {elems_s(r['anim'])} | "
               f"{', '.join(f'`{x}`' for x in r['r']['ref']) or '—'} | {r['r']['why'] or '—'} |"
               for r in groups["new"]]
        md.append("")
    (ep / "animations.md").write_text("\n".join(md), encoding="utf-8")

    labels = {"screen": "Screen recordings", "broll": "B-roll", "image": "Images",
              "logo": "Logos", "audio": "Audio"}
    assets = {k: [] for k in labels}
    camera = []
    for seg in sb["segments"]:
        said = " / ".join(lines[l]["text"] for l in seg.get("script", []) if l in lines)
        for a in seg.get("assets", []):
            assets.setdefault(a.get("type"), []).append((seg["id"], line_span(seg), a.get("what", ""), said))
        if seg.get("picture") == "camera":
            camera.append((seg["id"], line_span(seg), said))
    md = [f"# Assets — {sb.get('episode', ep.name)}", "",
          "Generated from storyboard.json by `storyboard.py lists` — edit the storyboard, not this file.", ""]
    for key, label in labels.items():
        if assets.get(key):
            md += [f"## {label}", "", "| Seg | Lines | Capture | While saying |", "|---|---|---|---|"]
            md += [f"| {s} | {ls} | {what} | {said} |" for s, ls, what, said in assets[key]]
            md.append("")
    zooms = [(seg["id"], z) for seg in sb["segments"] for z in seg.get("zooms", [])]
    if zooms:
        md += ["## 局部放大 / 強調（剪輯時做）", "", "| Seg | At | Type | Target |", "|---|---|---|---|"]
        md += [f"| {sid} | {z['at']} | {z.get('type', 'zoom')} | {z['target']} |" for sid, z in zooms]
        md.append("")
    if camera:
        md += ["## On camera", "", "| Seg | Lines | Said |", "|---|---|---|"]
        md += [f"| {s} | {ls} | {said} |" for s, ls, said in camera]
        md.append("")
    (ep / "assets.md").write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {ep}/animations.md ({total} animations) and assets.md "
          f"({sum(len(v) for v in assets.values())} assets, {len(camera)} camera segments)")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("estimate")
    p.add_argument("path")
    p = sub.add_parser("check")
    p.add_argument("episode")
    p.add_argument("--write", action="store_true")
    p.add_argument("--studio")
    p = sub.add_parser("recipes")
    p.add_argument("episode", nargs="?")
    p.add_argument("--studio")
    p = sub.add_parser("lists")
    p.add_argument("episode")
    p.add_argument("--studio")
    args = ap.parse_args()
    {"estimate": cmd_estimate, "check": cmd_check, "lists": cmd_lists, "recipes": cmd_recipes}[args.cmd](args)


if __name__ == "__main__":
    main()
