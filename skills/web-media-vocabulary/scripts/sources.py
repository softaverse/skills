"""Search free stock libraries and normalize every result to one record shape.

Shared by search.py and fetch.py. Standard library only.

Every record that leaves this module has passed the license whitelist: free and
usable commercially. Anything else is dropped here, so no later step ever sees it.

Keys come from the environment; a source without its key is skipped:
    PEXELS_API_KEY        https://www.pexels.com/api/
    UNSPLASH_ACCESS_KEY   https://unsplash.com/developers
    PIXABAY_API_KEY       https://pixabay.com/api/docs/
Openverse and Iconify need no key.
"""
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

UA = "web-media-vocabulary/1.0 (+https://github.com/softaverse/skills)"
APP = "web_media_vocabulary"  # utm_source for Unsplash attribution links

KEYS = {
    "pexels": "PEXELS_API_KEY",
    "unsplash": "UNSPLASH_ACCESS_KEY",
    "pixabay": "PIXABAY_API_KEY",
}

# Which sources can answer which kind of search, in default order.
KINDS = {
    "photo": ["pexels", "unsplash", "pixabay", "openverse"],
    "video": ["pexels", "pixabay"],
    "illustration": ["pixabay", "openverse"],
    "icon": ["iconify"],
}

# Library licenses: free for commercial use, attribution not required.
HOUSE = {
    "pexels": ("Pexels License", "https://www.pexels.com/license/"),
    "unsplash": ("Unsplash License", "https://unsplash.com/license"),
    "pixabay": ("Pixabay Content License", "https://pixabay.com/service/license-summary/"),
}

# Openverse license codes allowed: public domain or attribution only.
# Excluded: NC (no commercial use), ND (no cropping or color grading), SA (share-alike).
CC_OK = {"cc0": False, "pdm": False, "by": True}  # code -> attribution required

# Iconify icon-set licenses (SPDX) allowed. GPL, MPL, SA, and NC sets are excluded.
SPDX_OK = {
    "MIT": False, "ISC": False, "Apache-2.0": False, "BSD-3-Clause": False,
    "Unlicense": False, "CC0-1.0": False, "OFL-1.1": False,
    "CC-BY-4.0": True, "CC-BY-3.0": True,
}

# Words in alt text or tags that suggest a risk the license does not cover.
PEOPLE = re.compile(r"\b(people|person|man|men|woman|women|girl|boy|child|children|kid|kids|"
                    r"face|portrait|selfie|couple|family|team|businessman|businesswoman|model)\b", re.I)
# Only words that name the brand itself: "apple" and "amazon" are mostly fruit and rainforest.
BRAND = re.compile(r"\b(logo|logos|brand|trademark|iphone|ipad|macbook|imac|airpods|samsung|nike|"
                   r"adidas|starbucks|coca[- ]?cola|tesla|google|microsoft)\b", re.I)

# Icon-name suffixes that mark a variant of the same glyph.
VARIANTS = ("-20-solid", "-16-solid", "-bold-duotone", "-line-duotone", "-duotone", "-twotone",
            "-filled", "-fill", "-solid", "-outline-rounded", "-outline-sharp", "-outline",
            "-rounded", "-sharp", "-bold", "-light", "-thin", "-linear", "-broken")


# One spelling for black and white across sources.
GRAY = {"bw", "black_and_white", "grayscale", "greyscale"}
PEXELS_COLORS = {"red", "orange", "yellow", "green", "turquoise", "blue", "violet", "pink",
                 "brown", "black", "gray", "white"}
# Names one source spells differently; anything still unknown to a source is not sent.
ALIASES = {
    "pexels": {"purple": "violet", "magenta": "pink", "teal": "turquoise", "lilac": "violet", "grey": "gray"},
    "unsplash": {"violet": "purple", "lilac": "purple", "turquoise": "teal", "pink": "magenta"},
    "pixabay": {"purple": "lilac", "violet": "lilac", "magenta": "pink", "teal": "turquoise", "grey": "gray"},
}


def color_for(source, color):
    if not color:
        return None
    if color.lower() in GRAY:
        return {"unsplash": "black_and_white", "pixabay": "grayscale"}.get(source)
    if source == "pexels" and color.startswith("#"):
        return color
    color = ALIASES[source].get(color.lower(), color.lower())
    allowed = {"pexels": PEXELS_COLORS, "unsplash": UNSPLASH_COLORS, "pixabay": PIXABAY_COLORS}[source]
    return color if color in allowed else None


class SourceError(Exception):
    pass


PLACEHOLDER = re.compile(r"^[.\-x*<> ]*$|your|placeholder|changeme", re.I)


def key(source):
    env = KEYS.get(source)
    if not env:
        return None
    value = os.environ.get(env, "").strip()
    return "" if PLACEHOLDER.search(value) else value  # e.g. export PEXELS_API_KEY="..."


def available(source):
    return source not in KEYS or bool(key(source))


def get_json(url, headers=None, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        hint = {401: "key rejected", 403: "key rejected or rate limited", 429: "rate limited"}.get(e.code, "")
        raise SourceError(f"HTTP {e.code} {hint}".strip()) from None
    except (urllib.error.URLError, TimeoutError) as e:
        raise SourceError(f"unreachable ({getattr(e, 'reason', e)})") from None


def flags_for(text):
    out = []
    if PEOPLE.search(text):
        out.append("people")
    if BRAND.search(text):
        out.append("brand")
    return out


def record(**kw):
    kw.setdefault("tags", [])
    kw.setdefault("alt", "")
    kw["flags"] = flags_for(" ".join([kw["alt"], *kw["tags"]]))
    if kw.get("kind") == "illustration":
        kw["flags"] = [f for f in kw["flags"] if f != "people"]  # drawn people carry no likeness rights
    return kw


def house(source, rec_kw):
    name, url = HOUSE[source]
    rec_kw.update(license=name, license_url=url, attribution_required=False)
    return rec_kw


# --- Pexels -----------------------------------------------------------------

PEXELS_ORIENT = {"landscape": "landscape", "portrait": "portrait", "square": "square"}


def pexels(kind, q, n, orientation=None, color=None, min_width=0):
    headers = {"Authorization": key("pexels")}
    params = {"query": q, "per_page": min(n, 80)}
    if orientation:
        params["orientation"] = PEXELS_ORIENT[orientation]
    if kind == "photo":
        if color_for("pexels", color):
            params["color"] = color_for("pexels", color)  # a name or a hex like #f5e6d3
        data = get_json("https://api.pexels.com/v1/search?" + urllib.parse.urlencode(params), headers)
        out = []
        for p in data.get("photos", []):
            if p["width"] < min_width:
                continue
            base = p["src"]["original"]
            out.append(record(**house("pexels", dict(
                uid=f"pexels:{p['id']}", source="pexels", kind="photo", id=str(p["id"]),
                alt=p.get("alt") or "", width=p["width"], height=p["height"],
                thumb=p["src"]["medium"], preview=p["src"]["large"],
                download=base, sizable="pexels", page=p["url"],
                author=p["photographer"], author_url=p["photographer_url"],
                color=p.get("avg_color")))))
        return out
    if kind == "video":
        data = get_json("https://api.pexels.com/videos/search?" + urllib.parse.urlencode(params), headers)
        out = []
        for v in data.get("videos", []):
            if v["width"] < min_width:
                continue
            files = sorted(({"width": f["width"], "height": f["height"], "url": f["link"]}
                            for f in v.get("video_files", [])
                            if f.get("file_type") == "video/mp4" and f.get("width")),
                           key=lambda f: f["width"])
            if not files:
                continue
            small = next((f for f in files if f["width"] >= 640), files[-1])
            slug = v["url"].rstrip("/").rsplit("/", 1)[-1]
            out.append(record(**house("pexels", dict(
                uid=f"pexels-video:{v['id']}", source="pexels", kind="video", id=str(v["id"]),
                alt=re.sub(r"-?\d+$", "", slug).replace("-", " "),
                width=v["width"], height=v["height"], duration=v.get("duration"),
                thumb=v["image"], preview=v["image"], video_preview=small["url"], files=files,
                page=v["url"], author=v["user"]["name"], author_url=v["user"]["url"]))))
        return out
    return []


# --- Unsplash ---------------------------------------------------------------

UNSPLASH_ORIENT = {"landscape": "landscape", "portrait": "portrait", "square": "squarish"}
UNSPLASH_COLORS = {"black_and_white", "black", "white", "yellow", "orange", "red", "purple",
                   "magenta", "green", "teal", "blue"}


def utm(url):
    return f"{url}?utm_source={APP}&utm_medium=referral"


def unsplash(kind, q, n, orientation=None, color=None, min_width=0):
    if kind != "photo":
        return []
    headers = {"Authorization": f"Client-ID {key('unsplash')}", "Accept-Version": "v1"}
    params = {"query": q, "per_page": min(n, 30), "content_filter": "high"}
    if orientation:
        params["orientation"] = UNSPLASH_ORIENT[orientation]
    if color_for("unsplash", color):
        params["color"] = color_for("unsplash", color)
    data = get_json("https://api.unsplash.com/search/photos?" + urllib.parse.urlencode(params), headers)
    out = []
    for p in data.get("results", []):
        if p.get("premium") or p.get("plus"):
            continue  # Unsplash+ images are paid
        if p["width"] < min_width:
            continue
        u = p["user"]
        rec = house("unsplash", dict(
            uid=f"unsplash:{p['id']}", source="unsplash", kind="photo", id=p["id"],
            alt=p.get("alt_description") or p.get("description") or "",
            tags=[t["title"] for t in p.get("tags", []) if t.get("title")],
            width=p["width"], height=p["height"],
            thumb=p["urls"]["small"], preview=p["urls"]["regular"], download=p["urls"]["raw"],
            hotlink=True, track=p["links"]["download_location"],
            page=utm(p["links"]["html"]), author=u["name"], author_url=utm(u["links"]["html"]),
            color=p.get("color")))
        # The license needs no credit, but the API guidelines do whenever the photo is shown.
        rec["attribution_required"] = True
        out.append(record(**rec))
    return out


# --- Pixabay ----------------------------------------------------------------

PIXABAY_ORIENT = {"landscape": "horizontal", "portrait": "vertical"}
PIXABAY_COLORS = {"grayscale", "transparent", "red", "orange", "yellow", "green", "turquoise",
                  "blue", "lilac", "pink", "white", "gray", "black", "brown"}


def pixabay_tags(h):
    """Pixabay repeats tags; keep each once, in order."""
    return list(dict.fromkeys(t.strip() for t in h.get("tags", "").split(",") if t.strip()))


def pixabay_photo(h, kind):
    tags = pixabay_tags(h)
    return record(**house("pixabay", dict(
        uid=f"pixabay:{h['id']}", source="pixabay", kind=kind, id=str(h["id"]),
        alt=", ".join(tags[:6]), tags=tags, width=h["imageWidth"], height=h["imageHeight"],
        thumb=h["webformatURL"], preview=h["webformatURL"], download=h["largeImageURL"],
        max_download_width=1280, page=h["pageURL"], author=h["user"],
        author_url=f"https://pixabay.com/users/{h['user']}-{h['user_id']}/")))


def pixabay(kind, q, n, orientation=None, color=None, min_width=0, ids=None):
    params = {"key": key("pixabay"), "q": q[:100], "per_page": max(3, min(n, 200)), "safesearch": "true"}
    if ids:
        params = {"key": key("pixabay"), "id": ids}
    if kind in ("photo", "illustration"):
        if not ids:
            params["image_type"] = "photo" if kind == "photo" else "illustration"
            if orientation in PIXABAY_ORIENT:
                params["orientation"] = PIXABAY_ORIENT[orientation]
            if color_for("pixabay", color):
                params["colors"] = color_for("pixabay", color)
            if min_width:
                params["min_width"] = min_width
        data = get_json("https://pixabay.com/api/?" + urllib.parse.urlencode(params))
        return [pixabay_photo(h, kind) for h in data.get("hits", [])]
    if kind == "video":
        if min_width and not ids:
            params["min_width"] = min_width
        data = get_json("https://pixabay.com/api/videos/?" + urllib.parse.urlencode(params))
        out = []
        for h in data.get("hits", []):
            vids = h.get("videos", {})
            files = sorted(({"width": f["width"], "height": f["height"], "url": f["url"], "size": f.get("size")}
                            for f in vids.values() if f.get("url")), key=lambda f: f["width"])
            if not files:
                continue
            w, hgt = files[-1]["width"], files[-1]["height"]
            if orientation == "landscape" and w < hgt or orientation == "portrait" and w > hgt:
                continue
            small = next((f for f in files if f["width"] >= 640), files[-1])
            thumb = next((f.get("thumbnail") for f in vids.values() if f.get("thumbnail")), None)
            tags = pixabay_tags(h)
            out.append(record(**house("pixabay", dict(
                uid=f"pixabay-video:{h['id']}", source="pixabay", kind="video", id=str(h["id"]),
                alt=", ".join(tags[:6]), tags=tags, width=w, height=hgt, duration=h.get("duration"),
                thumb=thumb, preview=thumb, video_preview=small["url"], files=files,
                page=h["pageURL"], author=h["user"],
                author_url=f"https://pixabay.com/users/{h['user']}-{h['user_id']}/"))))
        return out
    return []


# --- Openverse --------------------------------------------------------------

OPENVERSE_ASPECT = {"landscape": "wide", "portrait": "tall", "square": "square"}


def openverse(kind, q, n, orientation=None, color=None, min_width=0):
    if kind not in ("photo", "illustration"):
        return []
    params = {"q": q, "page_size": min(n, 20), "license": ",".join(CC_OK), "mature": "false",
              "category": "photograph" if kind == "photo" else "illustration,digitized_artwork"}
    if orientation:
        params["aspect_ratio"] = OPENVERSE_ASPECT[orientation]
    data = get_json("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(params), timeout=12)
    out = []
    for r in data.get("results", []):
        code = (r.get("license") or "").lower()
        if code not in CC_OK:
            continue  # belt and braces: the query already filters
        if (r.get("width") or 0) < min_width:
            continue
        ver = r.get("license_version") or ""
        name = "CC0" if code == "cc0" else "Public Domain Mark" if code == "pdm" else f"CC BY {ver}".strip()
        out.append(record(
            uid=f"openverse:{r['id']}", source="openverse", kind=kind, id=r["id"],
            alt=r.get("title") or "", tags=[t["name"] for t in r.get("tags") or [] if t.get("name")],
            width=r.get("width") or 0, height=r.get("height") or 0,
            thumb=r.get("thumbnail") or r["url"], preview=r.get("thumbnail") or r["url"], download=r["url"],
            page=r.get("foreign_landing_url") or r["url"], provider=r.get("provider"),
            author=r.get("creator") or "unknown", author_url=r.get("creator_url") or "",
            license=name, license_url=r.get("license_url") or "", attribution_required=CC_OK[code],
            attribution=r.get("attribution") or ""))
    return out


# --- Iconify ----------------------------------------------------------------

def variant_of(name):
    return next((s.lstrip("-") for s in VARIANTS if name.endswith(s)), "")


def iconify(terms, n_sets=8, prefixes=None, variant=None):
    """Search each term, then group hits by icon set: one record per set, one icon per term.

    A term may list synonyms as "home|house": sets name the same glyph differently.
    variant: keep only names ending in -<variant> (so "duotone" also takes "-bold-duotone"); "base" keeps names with no variant suffix.
    """
    sets, meta = {}, {}
    for term in terms:
        for word in term.split("|"):
            params = {"query": word.strip(), "limit": 96 if prefixes else 400}
            if prefixes:
                params["prefixes"] = ",".join(prefixes)
            data = get_json("https://api.iconify.design/search?" + urllib.parse.urlencode(params))
            meta.update(data.get("collections", {}))
            for full in data.get("icons", []):
                prefix, name = full.split(":", 1)
                if variant and (variant_of(name) if variant == "base" else not name.endswith("-" + variant)):
                    continue
                hits = sets.setdefault(prefix, {})
                hits.setdefault(term, full)  # results are ranked; keep the first per term
    out = []
    for prefix, hits in sets.items():
        info = meta.get(prefix, {})
        spdx = info.get("license", {}).get("spdx", "")
        if spdx not in SPDX_OK:
            continue
        if info.get("category") == "Archive / Unmaintained":
            continue
        author = info.get("author", {})
        icons = [hits.get(t) for t in terms]
        out.append(record(
            uid=f"iconify:{prefix}" + (f"~{variant}" if variant else ""), source="iconify", kind="icon",
            id=prefix, alt=info.get("name", prefix), set_name=info.get("name", prefix),
            set_total=info.get("total"), terms=terms, icons=icons,
            coverage=sum(1 for i in icons if i), category=info.get("category", ""),
            page=f"https://icon-sets.iconify.design/{prefix}/", author=author.get("name", ""),
            author_url=author.get("url", ""), license=info.get("license", {}).get("title", spdx),
            license_url=info.get("license", {}).get("url", ""), attribution_required=SPDX_OK[spdx],
            logos=info.get("category") == "Logos"))
    out.sort(key=lambda r: (-r["coverage"], -(r["set_total"] or 0)))
    for r in out:
        if r.get("logos"):
            r["flags"].append("brand")
    return out[:n_sets]


SEARCH = {"pexels": pexels, "unsplash": unsplash, "pixabay": pixabay, "openverse": openverse}


def allowed(rec):
    """The whitelist, checked again at download time."""
    src = rec.get("source")
    if src in HOUSE:
        return rec.get("license") == HOUSE[src][0]
    if src == "openverse":
        return bool(re.fullmatch(r"CC0|Public Domain Mark|CC BY( [\d.]+)?", rec.get("license", "")))
    if src == "iconify":
        return True  # filtered by SPDX at search time; titles vary, so no second check here
    return False


def attribution_line(rec):
    if rec.get("attribution"):
        return rec["attribution"]
    if rec["source"] == "unsplash":
        return (f'Photo by <a href="{rec["author_url"]}">{rec["author"]}</a> on '
                f'<a href="{utm("https://unsplash.com/")}">Unsplash</a>')
    where = {"pexels": "Pexels", "unsplash": "Unsplash", "pixabay": "Pixabay"}.get(rec["source"])
    if rec["kind"] == "icon":
        return f"Icons: {rec['set_name']} by {rec['author']}, {rec['license']}"
    what = {"video": "Video", "illustration": "Illustration"}.get(rec["kind"], "Photo")
    return f"{what} by {rec['author']} on {where}" if where else f"{rec['alt']} by {rec['author']}, {rec['license']}"
