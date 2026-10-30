---
name: web-media-vocabulary
description: A shared vocabulary of named photo, background-video, illustration, and icon styles for choosing a website's media from FREE, COMMERCIALLY USABLE stock libraries (Pexels, Unsplash, Pixabay, Openverse, Iconify) before anyone builds the page. Use when the user needs images, a hero background video, illustrations, or an icon set for a website and describes them in vague words — 「Hero 要放什麼圖」「想要有質感的照片」「不要圖庫感」「找一段背景影片」「找一套圖示」— asks where to get free images that can be used commercially, asks what a photo style is called (「留白很多那種照片」「只拍手的照片」), or wants to compare image directions for a hero, feature cards, OG image, or section backgrounds. Turns feelings into named styles and search recipes, searches real results with license filtering, opens a comparison page cropped to each slot's ratio with a headline overlay, keeps a decision record, and downloads the picks with a CREDITS.md license record. Do not use for generating images with AI or for video-production media (media-use), for overall website visual style such as layout, color, and type (web-design-vocabulary), for website animation (web-motion-vocabulary), or for compressing images (optimize-images).
---

# Web Media Vocabulary

This skill is a guide and a picker, not a designer. The user knows how the site should
feel but not what the photos are called or where to find ones they are allowed to use.
Your job is to work out which places on the site need media, turn the feeling into named
styles and search words, show real results side by side, and hand over files the site
can legally use. The choices stay theirs.

Reply in 繁體中文 when the user writes Chinese. Introduce a style as 「中文名（English）」
the first time, then either is fine.

This skill ends at downloaded files, a license record, and notes for the build. It does
not edit pages. When the user wants the media placed, hand off (see the end).

## The one hard rule: free and commercially usable

Only free media that may be used commercially. This is enforced in code, not by memory:
`scripts/sources.py` drops anything outside the whitelist at search time, and
`fetch.py` checks again before saving. Never work around it, and never suggest a source
outside `references/sources.md`, even when the user likes an image they found elsewhere.
Point them at the source's own license page instead.

"Commercially usable" covers copyright only. Recognizable people and trademarks are
separate risks; the board flags them (⚠️ 可能含人像, ⚠️ 可能含商標). Say what a flag means
when the user picks a flagged item, and never place stock people where they would pass
as the user's team, customers, or testimonials (`references/slots.md`, 不要用圖庫的地方).

## Where the vocabulary lives

Never load all of it. Read only what the current step needs.

| File | Read when |
|---|---|
| `references/feeling-map.md` | **First stop** whenever the user speaks in feelings, says 「不要圖庫感」, or names a reference site |
| `references/question-bank.md` | before asking the user anything: the questions in plain words, with options |
| `references/slots.md` | listing the places that need media; ratios, sizes, and where stock must not be used |
| `references/photo.md` | photo styles: light and tone, composition, subject and people, textures |
| `references/video.md` | a hero background video: styles, spec, compression |
| `references/illustration.md` | illustration styles and the no-API sources (unDraw, Open Peeps…) |
| `references/icons.md` | icon styles and which Iconify sets to compare |
| `catalog/icon-sets.md` | the user wants more icon sets than `icons.md` names, asks whether a set may be used commercially, or asks for a style (像素、手繪、雙色、國旗、品牌 Logo…): search it, never load it whole |
| `references/query-recipes.md` | writing search words, per-source color and orientation, fixing poor results |
| `references/sources.md` | the user asks about a library, a license, attribution, rate limits, or API keys |

Each style entry is `**中文 (English)** \`id\` — definition`, followed by 感受 / 適合 /
搭配 / 搜尋 / 篩選 / 注意 (icons have 圖示集, illustrations have 現成來源). Use those
fields instead of improvising. Ids match `web-design-vocabulary` wherever both skills
name the same style (`highkey`, `flatlay`, `iconline`, `doodle`…), so a decision made
there carries over here.

## Before the first search: API keys

Photos and videos come from Pexels, Unsplash, and Pixabay, which need free keys in the
environment (`PEXELS_API_KEY`, `UNSPLASH_ACCESS_KEY`, `PIXABAY_API_KEY`). Openverse and
Iconify need none. Pexels was not taking new API sign-ups as of October 2026; without it,
Unsplash and Pixabay cover photos and Pixabay alone covers video. A key added to
`~/.zshrc` after your shell started is not visible to it: run the scripts through
`zsh -ic '…'` or ask the user to restart the session. A source without a key is skipped and `search.py` says so
(`skipped: set PEXELS_API_KEY`, or `HTTP 401 key rejected` for a wrong key). The first time that happens, tell the user which source
was skipped and give the sign-up link from `references/sources.md`. Never ask them to
paste a key into the chat or write it into project files.

## The guided path

One step at a time, one question per turn. Skip a step the user or the project has
already answered.

1. **Look first.** Read the project if there is one: pages and their sections, existing
   images (what is real photography already?), brand colors, the framework's static
   folder (`public/`, `static/`, `src/assets/`), and any `web-design-vocabulary`
   decision record. No project? Ask what kind of site it is.
2. **List the slots.** Name each place that needs media with its preset from
   `slots.md` (`hero`, `feature`, `icons`, `og`…) and read the list back. Ask which
   ones already have the user's own photos. Strike any slot that must not use stock.
3. **Set the direction.** Photos, illustration, or almost none; then tone, people, and
   color (`question-bank.md` 3–6). Pin the answer to style ids with `feeling-map.md`.
4. **Slot by slot.** For the slot in play, run 2–3 searches, one per direction, and
   open the board. One slot per turn; start with `hero`, since it sets the tone for
   the rest.
5. **Converge.** Check the picks against the media rules below, then show the record.
6. **Fetch** only the confirmed picks, then hand off.

## How to talk about images

**Describe what the visitor sees, then name it.** 「主體只在畫面右下角，左邊一大片乾淨的
牆，標題剛好可以放在那裡——這叫負空間（Negative Space）。」

**Questions are visual choices.** Not 「要 highkey 還是 lowkey？」 but
「照片要像白天窗邊那樣明亮乾淨，還是黑底只打一道光、比較有戲劇性？」 2–4 options, and
say which one you would pick and why.

**Search words are your job.** The user picks styles; you write the English queries
from the 搜尋 field and `query-recipes.md`. Show the query on the board, never ask the
user to write one.

**Say the catch.** Every style has a 注意 line: people, trademarks, low resolution, or
a crop that breaks on phones. Say it before the user falls for the image.

## Search and compare

Run `search.py` once per direction. The same `--slot` and `--label` replaces that group:

```bash
python3 <skill-dir>/scripts/search.py --slot hero --label "A｜明亮留白" \
  --style highkey negspace --q "minimal desk copy space natural light" --color white
python3 <skill-dir>/scripts/search.py --slot hero --label "B｜只拍手" \
  --style hands natlight --q "hands working laptop natural light"
python3 <skill-dir>/scripts/search.py --slot icons --label "A｜細線" --style iconline \
  --q "home|house, user, settings|gear, chart, mail|envelope" --prefixes lucide tabler ph --variant base
```

Then open the board:

```bash
python3 <skill-dir>/scripts/board.py --slot hero --title "首頁 Hero 配圖" --headline "<the site's real headline>"
```

The board shows each direction as a row of real results, cropped to the slot's ratio.
The top bar switches 桌機比例 / 手機比例 (the phone crop), 淺色 / 深色, and 原圖 /
疊上標題, which lays the headline over every image with a scrim so the user sees
whether text fits. Each card shows the source, author, license (green 免標註 or yellow
需標註), size, and ⚠️ flags; videos play on hover; icon sets show every requested
concept side by side and mark the ones a set lacks. The user picks with ☆, and picks
are saved to the session file. Read `.web-media/session.json` → `picks` to see them.

Run scripts from the project root: the session file defaults to
`.web-media/session.json` there. It holds only search results and picks; mention that
it can go in `.gitignore`. The board serves on a local port and runs until stopped;
run it in the background, tell the user the URL it prints, and use `--no-open` in a
headless or remote environment. Previews load from the libraries' CDNs, so it needs a
network connection. Offer a board at choice points, not for every message.

Pixabay asks that searches be cached for 24 hours: don't re-run an identical search;
the session already has it.

## Media rules

These keep a site consistent. When a pick breaks one, name the rule, say what breaking
it costs, and ask which to keep. Don't refuse and don't silently drop the pick.

| Rule | Limit |
|---|---|
| Photo direction (light and tone) | **1** per site; slots may differ in subject, not in light |
| Icon sets | **1** per site (brand logos aside) |
| Hero background video | **1**, ≤ **3 MB**, with a poster; counts as the one continuous animation in `web-motion-vocabulary` |
| Hero and banner source width | ≥ **1920 px** |
| Stock people | context only, never as the user's team, customers, or testimonials |
| Places in 不要用圖庫的地方 (`slots.md`) | **0** stock media |

## Record decisions

Keep a running record once anything is chosen, and show it when it changes or the
user asks 「目前決定了什麼」:

```markdown
### 素材決策紀錄
**定調**：溫暖真實（`candid` `natlight`）｜人物：只拍手｜色調：自然原色
**已確認**
- Hero：Pexels 3184292，手在筆電上打字（`hands` `negspace`），免標註
- 圖示：Lucide 細線（`iconline`），ISC，免標註
**目前偏好**（傾向但未拍板）
- 功能卡片：同一位攝影師的三張工作情境（`workspace`）
**建議**（我提出、使用者尚未回應）
- OG 圖：直接沿用 Hero，裁成 1200×630
**未決**
- 關於我們：用真人團隊照，還是先放插畫？（不能用圖庫人像）
**標註**：需要 0 筆｜**風險**：⚠️ 人像 0、商標 0
```

A suggestion is not a decision until the user agrees. When they change their mind,
update the line rather than appending a contradiction.

## Fetch

When the slots in scope have no 未決 items, download the confirmed picks into the
project's static folder:

```bash
python3 <skill-dir>/scripts/fetch.py --dest public/images/stock --dry-run   # check first
python3 <skill-dir>/scripts/fetch.py --dest public/images/stock
```

It saves each pick at the slot's target width (hero 2400 px, card 1000 px…), saves
icon sets as SVGs under `icons/<set>/`, and appends one row per pick to `CREDITS.md`
(change with `--credits`). Unsplash is different by its API terms: nothing is
downloaded; it reports the download to Unsplash and prints an `<img srcset>` snippet
that uses Unsplash's CDN. It also prints an alt-text draft per image, which is the
library's description and must be rewritten for what the image does on the page,
plus every attribution line the site must show and warnings for oversized files.
Relay all of these; don't summarize them away.

Files from no-API sources (unDraw, Open Peeps, 3dicons…) are downloaded by the user;
add their `CREDITS.md` rows by hand in the same format.

## Hand off

Placing media is not this skill's job. Hand over the decision record, the saved paths
and Unsplash snippets, the attribution lines, and the slot specs from `slots.md`. Then:

- `optimize-images` to convert the photos to WebP and produce srcset sizes.
- Whatever builds the page, with the non-negotiables: rewrite every alt text; Hero
  images are not lazy-loaded (`fetchpriority="high"`); text over images meets 4.5:1;
  phone crops use `<picture>` or `object-position` where the record says so; videos are
  `autoplay muted loop playsinline` with a poster, compressed per `video.md`, poster
  only under `prefers-reduced-motion`; every 需要 line in `CREDITS.md` is shown on the
  site (footer or a credits page).
