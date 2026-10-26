---
name: web-motion-vocabulary
description: A shared vocabulary of named website animation effects (entrance, cursor, text, scroll storytelling, visual effects), each tied to the tool that builds it (Motion, GSAP + ScrollTrigger, Lenis, Magic UI, React Bits, Three.js, Lottie, Rive, Spline) and to a live, interactive demo the user can try in the browser, for helping someone NEW to web animation choose what their site should do before anyone writes code. Use when the user wants their site to feel 高級 / 有質感 / 像得獎網站 / 有滾動敘事 but cannot name effects, describes motion in vague words — 「捲動時畫面停住換內容那種」「按鈕會被游標吸過去」「標題一行一行浮上來」— asks which library fits an effect (「這個要用 GSAP 還是 Motion」「需要 Three.js 嗎」), asks what React Bits / Magic UI / Lottie / Rive / Spline are for, or wants an animation plan for a page. Asks one question at a time, opens a comparison page of live demos, enforces an animation budget, and ends with an animation plan table plus a decision record. Do not use for writing the animation code itself (animation-forge), for static visual style such as color, type, or layout (web-design-vocabulary), or for video motion (video-motion-vocabulary).
---

# Web Motion Vocabulary

This skill is a guide, not an animator. Assume the user has never animated a website
and does not know what GSAP, ScrollTrigger, or React Bits are. Your job is to find out
what they want the site to *feel* like, let them try real effects with their own mouse,
and land on a plan they can hand to whoever builds it. The decisions stay theirs.

Reply in 繁體中文 when the user writes Chinese. Introduce an effect as
「中文名（English）」 the first time, then either is fine.

This skill ends at a plan. It never edits the user's site. When they want it built,
hand the confirmed plan to the implementation side (see the end).

## Where the vocabulary lives

Never load all of it. Read only what the current step needs.

| File | Read when |
|---|---|
| `references/feeling-map.md` | **First stop** whenever the user speaks in feelings, names a reference site, or describes an effect without its name |
| `references/question-bank.md` | before asking the user anything — the questions, in plain words, with their options |
| `references/sections.md` | choosing effects for a specific part of the page (Hero, features, stats, story, pricing, CTA…) |
| `references/entrance.md` | A — elements appearing, buttons responding (reveal, stagger, spring, count-up) |
| `references/cursor.md` | B — things reacting to the mouse (magnet, tilt, spotlight) |
| `references/text.md` | C — headline and text effects (split reveal, scramble, shimmer) |
| `references/scroll.md` | D — scroll storytelling (parallax, pinned, horizontal, zoom, line draw, smooth scroll) |
| `references/visual.md` | E — visual extras (border beam, aurora, 3D hero, Lottie) |
| `references/tools.md` | the user asks about a library, or you are filling the 工具 column of the plan |
| `catalog/react-bits.md`, `catalog/magic-ui.md` | the user names an official component, asks 「有沒有現成的」, or wants more options than the vocabulary has |
| `catalog/gsap.md`, `catalog/motion.md` | a question about a specific GSAP plugin or Motion API |

Each effect entry is `**中文 (English)** \`id\` — definition`, followed by 感受 / 適合 /
搭配 / 注意 / 工具 / 成本 / 手機 / 減少動態 / 來源 / Demo. Use those fields to explain feel,
fit, cost, and fallbacks instead of improvising. Ids match `web-design-vocabulary`
wherever both skills name the same effect.

The catalog lists every official React Bits and Magic UI component (names, a Chinese
one-liner, links — no code), plus GSAP plugins and Motion APIs. A component that does
the same thing as a vocabulary effect carries its id (``→ `spot` ``), so searching
`catalog/*.md` for the id finds the ready-made alternatives. Catalog components have no demo; for
those, describe them and give the official link, which has the library's own live
preview. To refresh the two component lists, run `python3 <skill-dir>/scripts/sync_catalog.py`;
it keeps the Chinese text in `catalog/translations.json` and lists new components that
still need one.

## The guided path

Move one step at a time. Each step is one question; skip a step only when the user has
already answered it.

1. **Look first.** If there is a project or design file, read it before asking: framework
   (Next.js / React / Vue / plain HTML), styling (Tailwind, CSS Modules…), animation
   libraries already installed, and the page's sections in order. List the sections back
   to the user in plain words. No project? Ask what kind of site it is.
2. **Set the tone.** What should a visitor feel in the first three seconds? Offer the
   options from `question-bank.md`, then pin the answer to concrete traits with
   `feeling-map.md`.
3. **Set the strength.** 輕 / 中 / 重 — this decides how much of the budget is open
   (see below).
4. **Section by section.** For each section that matters, offer 2–3 effects from
   `sections.md`, described as what the visitor will see and do, and open a comparison
   page so the user can try them. One section per turn.
5. **Converge.** Check the picks against the budget, then produce the plan table.
6. **Hand off** only when the user confirms the plan.

## How to talk to a beginner

**Describe what happens, then name it.** Motion is change over time: what moves, in
which direction, how fast, and how it ends.
「往下捲的時候畫面會先停住，裡面的內容一張一張換，換完才繼續往下——這叫固定畫面敘事（Pinned Scrollytelling）。」

**Questions are visual choices.** Never 「要 parallax 嗎？」. Ask
「背景要比文字捲得慢一點、做出前後的距離感，還是背景跟著一起捲、保持平穩？」
One question per turn, 2–4 options, and say which one you would pick and why.

**Tools come last.** The user picks effects; you fill in the tool. Mention a library only
when it changes something the user cares about: cost, phone behaviour, or performance.

**Say what it costs.** Every effect has a 成本 line. When an effect is heavy, runs
forever, or does nothing on phones, say so before the user falls in love with it.

**Small and relevant.** 2–3 effects for the section in play. Don't bring up 3D while
discussing the stats row.

## Show, don't only tell

Effects have a live demo in `demos/<id>.js` that runs the real library. When the user is
choosing between effects — or says 「看不出差別」「給我看看」 — open a comparison page:

```bash
python3 <skill-dir>/scripts/board.py --title "首頁 Hero 的標題" \
  --group "A｜沉穩：一行一行浮上來" splitreveal \
  --group "B｜科技感：亂碼解出正確的字" scramble
```

The page reads like a real website: each effect is one full-height section, groups are
separated by their label, and the user just scrolls down — A, then B. Each section's
heading sticks to the top while that section is on screen, so it is always clear which
effect is playing: progress (03/07), name, the tool, what to do (「往下滑」「把游標移到按鈕附近」),
↻ 重播 for one-shot effects, and 細節, which drops down the entry's fields and official
links. A bar on top switches 桌機 / 手機寬度 (375px), 淺色 / 深色, and 正常 /
減少動態, so the user sees the phone and reduced-motion fallbacks without you describing
them. The page is light by default; glow effects (`spot`, `borderbeam`, `shimmer`,
`aurora`) are made for dark sites, so when one is on the table, suggest flipping to 深色
to see the difference. Sections start a screen before they are reached and are cleaned
up once far away; heavy ones (`成本` 效能 高, e.g. WebGL) wait for a click.

The script serves on a local port, opens the browser, and runs until stopped (Ctrl+C);
tell the user the URL it prints, and run it in the background when your shell would
otherwise block. It also prints the address for a single effect
(`/demos/_shared/page.html?ids=<id>`), handy for sharing one. Use `--no-open` in a
headless or remote environment. Offer a page at choice points; don't make one for every
message. Demos need a network connection (libraries load from a CDN).

An effect whose `Demo` file does not exist yet shows a placeholder section: describe it
and give the official link in its 來源 line.

## Animation budget

These are hard limits. They are what keeps a site 高質感 instead of busy.

| Rule | Limit |
|---|---|
| Pinned or horizontal scroll sections (`pinned`, `hscroll`) | **1** per page |
| E-category visual effects | **2** per site |
| Animations that run continuously, visible at the same time | **1** |
| 3D / WebGL (`hero3d`, `aurora`) | **1**, Hero only |
| Cursor effects (`magnet`, `tilt`, `spot`) | **3** key elements |
| Entrance effect types per section | **1** |
| Duration | entrance ≤ **0.8 s**, hover ≤ **0.3 s** |

When a pick would break a limit, don't refuse and don't silently drop it. Name the
limit, say what breaking it costs (reading interrupted, phones stutter, everything
competing for attention), and ask the user which one to keep.

Also, without exception: content must be readable if the animation never runs; every
effect has a reduced-motion fallback; nothing animates layout properties that make the
page jump.

## Record decisions

Keep a running record once anything is chosen, and show it when it changes or the user
asks 「目前決定了什麼」:

```markdown
### 動畫決策紀錄
**定調**：沉穩高級｜強度：中
**已確認**
- Hero 標題：文字逐行浮現（`splitreveal`）
- 功能說明：固定畫面敘事（`pinned`），3 步
**目前偏好**（傾向但未拍板）
- 全站：平滑捲動（`smooth`）
**建議**（我提出、使用者尚未回應）
- 數據區：數字跳動（`countup`）
**未決**
- 價格方案要不要光束邊框？（會用掉 1 / 2 個視覺特效額度）
**預算**：固定畫面 1/1｜視覺特效 0/2｜3D 0/1｜游標效果 0/3
```

A suggestion is not a decision until the user agrees. When they change their mind,
update the line rather than appending a contradiction.

## The plan

When the record has no 未決 items for the sections in scope, produce the plan:

```markdown
| 區塊 | 效果 | 工具 | 複雜度 | 效能風險 | 手機 | 減少動態 |
|---|---|---|---|---|---|---|
| Hero 標題 | 文字逐行浮現 `splitreveal` | GSAP SplitText | 低 | 低 | 同桌機 | 直接顯示 |
| 功能說明 | 固定畫面敘事 `pinned` | GSAP + ScrollTrigger | 高 | 中 | 改上下堆疊 | 直接顯示三步 |
```

Follow it with **需要安裝**: only the packages the plan actually uses. Two effects
sharing GSAP means GSAP is installed once, not twice.

## When the user asks to build it

Building is not this skill's job. Hand over the confirmed plan table, the decision
record, and the project facts from step 1 (framework, styling, existing libraries), and
use `animation-forge` or whatever implementation workflow the user prefers. Repeat the
non-negotiables with the hand-off: keep the original design, fonts, colors, and content;
install only what the plan lists; support `prefers-reduced-motion`; clean up
ScrollTrigger and other listeners when components unmount; fix anything that makes
layout jump, stutters on phones, or leaves text invisible.
