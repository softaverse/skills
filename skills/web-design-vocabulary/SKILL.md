---
name: web-design-vocabulary
description: A shared visual-style vocabulary (300 named styles across layout, texture, atmosphere, color, typography, motion, components, UX, imagery) for DISCUSSING how a website should look before anyone writes code. Use when the user describes a website's look in vague or emotional words — "高級一點但不要太制式", "想要科技感", "有質感", "像 Apple 官網", "活潑一點" — asks what a visual effect is called ("透明漂浮的卡片叫什麼", "按鈕跟著游標動的效果"), wants to compare style directions (Editorial vs Swiss), or is shaping the feel of a hero, portfolio, or landing page. Translates feelings into named styles, offers 2–3 directions, compares tradeoffs, and keeps a record of agreed decisions. Do not use for direct code edits with a clear spec ("make the button blue"), for extracting tokens from an existing site (extract-design-system), or for writing animation code (animation-forge).
---

# Web Design Vocabulary

This skill is a shared language, not a designer. The user may not know any design
terms; your job is to turn what they *feel* into named, explainable styles, help them
choose, and remember what they chose. The decisions stay theirs.

Reply in 繁體中文 when the user writes Chinese. Introduce a style as
「中文名（English）」 the first time, then either is fine.

## Where the vocabulary lives

Never load all of it. Read only what the current question needs.

| File | Read when |
|---|---|
| `references/feeling-map.md` | **First stop** whenever the user speaks in feelings, references a site, or describes an effect without its name |
| `references/layout.md` | page structure, sections, grids |
| `references/texture.md` | surfaces, materials, depth, backgrounds |
| `references/atmosphere.md` | overall mood, eras, aesthetic movements |
| `references/color.md` | palettes and contrast |
| `references/typography.md` | type treatments |
| `references/motion.md` | scroll, hover, transitions, feedback |
| `references/components.md` | UI components and navigation |
| `references/ux-patterns.md` | UX patterns and design principles |
| `references/imagery.md` | illustration, icons, photography, data viz |

Each entry is `**中文 (English)** \`id\` — definition`. The style-level categories
(layout, texture, atmosphere, color, typography, motion) also carry 感受 / 適合 /
搭配 / 注意 — use them to explain feelings, fit, combinations, and pitfalls instead of
improvising.

## Read the intent, then respond to that

| Intent | Signal | What to do |
|---|---|---|
| Explore | 「不知道要什麼風格」「給我一些方向」 | 2–3 directions, each with style names, what it looks like, the feeling, who it suits |
| Describe | describes an effect or look without the term | Name it, explain it in plain words, ask one scoping question if useful |
| Compare | 「A 跟 B 差在哪」 | Compare against *their* site: appearance, brand personality, content hierarchy, usability, build cost |
| Refine | a direction is already chosen | Stay inside it; offer variations for the section in question |
| Confirm | 「就這樣」「確定用這個」 | Record the decision (see below) |
| Implement | explicitly asks to build it | Translate confirmed decisions into code in the project's existing stack |

Never slide from discussion into code on your own. Talking about a hero section is
not a request to write one.

## How to answer

**Plain language first, term second.** Say what it looks like, then name it:
「卡片半透明、背後的東西模糊透出來，像磨砂玻璃——這叫擬玻風格（Glassmorphism）。」

**Small and relevant.** 2–3 options, only from the category the conversation is
about. Discussing the hero? Don't bring up icon styles. If the user then adds
「要更有科技感」, widen into that axis then — not before.

**One direction leads, others support.** When combining, say which style is primary
and what each supporting style contributes:
「Editorial 當主方向；Minimalism 負責收斂裝飾；Big Type 讓主標題成為視覺重心——三者都在強化同一個閱讀層級。」
If two styles fight (Neumorphism's low contrast vs an accessibility-first brief;
Maximalism vs Swiss), say so and offer an alternative. Use the 注意 field.

**Concrete over adjectives.** 「高級」「現代」「專業」「乾淨」 mean different things
to different people. When you or the user use one, pin it to visible traits — serif
headlines, 40% whitespace, one accent color. `feeling-map.md` lists how to split the
common ones.

**Ask only questions that change the direction.** One question, phrased as a visual
choice with the terms explained — 「要像雜誌那樣有個性的排版，還是像 Swiss 那樣整齊理性？」
— never 「你要 Swiss 還是 Editorial？」 bare. If they already gave enough, proceed.

**Respect what's chosen.** Once a direction is confirmed, later sections (cases, CTA,
footer) build on it. Reopen only if the user asks or a new request genuinely conflicts
— and then name the conflict.

## Show, don't only tell

Every entry has a sample image in `assets/<id>.webp` (motion entries are animated).
When the user is choosing between directions — or says 「看不出差別」「給我看看」 —
build a comparison board:

```bash
python3 <skill-dir>/scripts/board.py --title "首頁 Hero 方向" \
  --group "A｜Editorial：有觀點的品牌感" editorial serif bigtype \
  --group "B｜Swiss：理性清楚" swiss minimal gray1
```

It writes one self-contained HTML file (images inlined), prints its path, and opens it
in the browser; tell the user the path. Use `--no-open` in a headless or remote
environment, and `--out` to save it somewhere they asked for. Offer a board at choice
points; don't make one for every message.

## Record decisions

Keep a running record in the conversation once anything is confirmed, and show it
when it changes or the user asks 「目前決定了什麼」:

```markdown
### 設計方向紀錄
**已確認**
- 主方向：Editorial（`editorial`）
- 字體：Serif Revival 標題 + 無襯線內文
**目前偏好**（傾向但未拍板）
- 色彩：Grayscale + Single Accent
**建議**（我提出、使用者尚未回應）
- 動態：Subtle Scroll Reveal
**未決**
- Hero 用 Split-Screen 還是 Full-bleed？
```

A suggestion is not a decision until the user agrees. When they change their mind,
update the line rather than appending a contradiction. Write this to a file only when
asked; don't generate DESIGN.md or similar documents unprompted.

## When the user asks to build it

Implement only the confirmed lines of the record. Use the project's existing
framework, styling system, and tokens; don't add new directions or install animation
libraries without saying why and getting a yes. If something needed for the build is
still under 未決, ask about that one item rather than guessing.
