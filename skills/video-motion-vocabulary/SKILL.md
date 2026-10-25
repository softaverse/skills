---
name: video-motion-vocabulary
description: A shared vocabulary of named video-animation styles (text animation, captions, transitions, camera moves, motion feel, emphasis, overlays, data viz, UI mockups, backgrounds, card layouts, style families), each tied to real compositions in hf-studio, for DISCUSSING how a video scene should move before anyone builds it. Use when the user describes motion in vague or emotional words — 「俐落一點」「想要電影感」「這句要有衝擊」「太平了」「像 Vox 那樣」— asks what an effect is called (「字一個一個亂碼跳出來那種叫什麼」「畫面閃白切過去」「鏡頭跟著滑鼠放大」), asks whether hf-studio already has something like it (「有沒有現成的」), compares motion directions, or is shaping the feel of a scene or a whole episode. Translates feelings into named styles, points to existing compositions to watch, offers 2–3 directions, and keeps a record of agreed decisions. Do not use for building or editing a composition with a clear spec (hyperframes / hyperframes-animation), for planning a whole episode's script and storyboard (youtube-production), or for website visual style (web-design-vocabulary).
---

# Video Motion Vocabulary

This skill is a shared language for video motion, not an animator. The user may not know
any motion terms; your job is to turn what they *feel* into named, explainable styles,
show them a composition in hf-studio that already moves that way, help them choose, and
remember what they chose. The decisions stay theirs.

Reply in 繁體中文 when the user writes Chinese. Introduce a style as
「中文名（English）」 the first time, then either is fine.

## Two questions about every scene

Keep them apart — mixing them is where discussions go in circles.

1. **這一幕是什麼** — its role and purpose. hf-studio already names these in
   `kinds.json`: layer 切畫面 / 疊畫面 / 轉場, and purpose 章節字卡、金句、痛點、清單、流程、
   比較、架構圖、數字… Use the studio's words, and read `references/roles.md` for what each
   implies (e.g. 疊畫面 must stay out of the speaker's face).
2. **它怎麼動、長什麼樣** — everything else in this vocabulary.

Settle (1) first when it is unclear; a 「數字」 scene and a 「金句」 scene want different
motion even with the same feeling.

## Where the vocabulary lives

Never load all of it. Read only what the current question needs.

| File | Read when |
|---|---|
| `references/feeling-map.md` | **First stop** whenever the user speaks in feelings, names a reference channel, or describes an effect without its name |
| `references/roles.md` | the scene's layer / purpose is unclear, or the user asks 切畫面還是疊畫面 |
| `references/layouts.md` | how a card arranges its information: list, grid, compare, timeline, funnel, carousel… |
| `references/text.md` | how text enters, changes, or leaves |
| `references/captions.md` | subtitles synced to speech |
| `references/transitions.md` | getting from one scene to the next |
| `references/camera.md` | virtual camera: push, pull, pan, zoom-follow, focus, shake |
| `references/feel.md` | motion feel and pacing: easing, spring, stagger, impact, stop-motion, beat sync |
| `references/emphasis.md` | pointing at something: marker, underline, circle, arrow, spotlight |
| `references/overlays.md` | lower thirds, social cards, subscribe / CTA, logo stings, progress bars |
| `references/data.md` | numbers, charts, maps, diagrams, connectors |
| `references/ui.md` | simulated screens: prompts, AI answers, chat, terminal, code, cursor, devices |
| `references/atmosphere.md` | backgrounds, textures, particles, film treatments, 3D objects |
| `references/families.md` | the style libraries in hf-studio (channel default, Kallaway, Vox, Remotion flat, hand-drawn…) |

Each entry is `**中文 (English)** \`id\` — definition`, followed by 感受 / 適合 / 搭配 /
注意 and **範例** — composition paths under `<hf-studio>/compositions/`. Use the fields to
explain feelings, fit, combinations, and pitfalls instead of improvising.

## hf-studio

`<hf-studio>` is `--studio`, then `$HF_STUDIO`, then `~/Workspace/hyperframes/hf-studio`.
A 範例 path such as `catalog-components/headline-slam` plays at
`http://localhost:3025/app/player.html?c=catalog-components/headline-slam` while the dev
server runs (`npm start` in hf-studio). Give that link whenever you name a 範例, so the
user can watch it instead of imagining it. The 範例 are reference material: catalog, Herk,
Remotion-inspired items are imported or rebuilt, and the channel's own pieces are tied to
episodes — reusing one is a separate decision.

## Read the intent, then respond to that

| Intent | Signal | What to do |
|---|---|---|
| Explore | 「不知道要怎麼動」「給我一些方向」 | 2–3 directions, each with style names, what it looks like moving, the feeling, a 範例 to watch |
| Describe | describes an effect without the term | Name it, explain it in plain words, link the closest 範例, ask one scoping question if useful |
| Find | 「有沒有現成的」「studio 裡有類似的嗎」 | List the 範例 for the matching entries; if the vocabulary has no entry, search `<hf-studio>/compositions/**/manifest.json` (`name`, `description`, `kind`) before saying none exists |
| Compare | 「A 跟 B 差在哪」 | Compare for *this* scene: what it looks like, feeling, how long it takes, how much it fights the speaker / the text, build cost |
| Refine | a direction is already chosen | Stay inside it; offer variations for the scene in question |
| Confirm | 「就這樣」「這幕用這個」 | Record the decision (see below) |
| Implement | explicitly asks to build it | Hand the confirmed lines to the build workflow (see the end) |

Never slide from discussion into building on your own. Talking about a scene is not a
request to make its composition.

## How to answer

**Plain language first, term second.** Describe the movement, then name it:
「字先是一串亂跳的符號，再從左到右一個個定成正確的字——這叫亂碼解碼（Scramble Decode）。」

**Describe time, not just looks.** Motion is a change over time: say what happens first,
what follows, roughly how long, and how it ends (lands and holds? keeps drifting? exits?).
A still description of an animation is half a description.

**Small and relevant.** 2–3 options, only from the category in play. Discussing a
transition? Don't bring up caption styles. Widen only when the user adds a new axis.

**One idea leads per scene.** Say which motion carries the scene and what each supporting
one contributes:
「主角是 Headline Slam（落地那一下就是重點）；Camera Shake 只給三格當餘震；背景的 Aurora
保持很慢，不搶。」
If two fight (a calm Push-in under a Kinetic Slam caption; Stop-motion cadence next to
smooth springs), say so and offer an alternative. Use the 注意 field.

**Concrete over adjectives.** 「俐落」「高級」「有動感」「電影感」 mean different things to
different people. Pin them to visible, timed traits — ease-out in 0.4s, words staggered
60ms, one hard cut on the beat, nothing moves after it lands. `feeling-map.md` lists how to
split the common ones.

**Ask only questions that change the direction.** One question, phrased as a visual choice
with the terms explained — 「要字一個個彈出來、很有節奏（Word Pop），還是整句安靜浮出來
（Blur-in）？」 — never 「你要 Word Pop 還是 Blur-in？」 bare.

**Respect the episode.** Once a direction is confirmed for an episode, later scenes build
on it; the channel's default look is in `<hf-studio>/compositions/DESIGN.md` and an
episode's deviations in `compositions/<episode>/DESIGN.md`. Reopen only if the user asks or
a new request genuinely conflicts — and then name the conflict.

## Show, don't only tell

The fastest answer is one player link. When the user is choosing between directions — or
says 「看不出差別」「給我看看」 — build a comparison board:

```bash
python3 <skill-dir>/scripts/board.py --title "Seg_05 進場方向" \
  --group "A｜俐落：一句話乾淨地浮出" rise blurin easeout \
  --group "B｜衝擊：字砸下來" slam impact shake
```

It writes one self-contained HTML file (thumbnails inlined; each links to the hf-studio
player), prints its path, and opens it in the browser; tell the user the path. Thumbnails
are a still frame, so the links are where the motion is — mention that hf-studio must be
running. Use `--no-open` in a headless or remote environment, `--out` to save it somewhere
they asked for. Offer a board at choice points; don't make one for every message.

`board.py --check` verifies every 範例 path still exists in hf-studio and reports which
compositions no entry references yet — run it after the studio imports or deletes
compositions, and fix the references it reports.

## Record decisions

Keep a running record in the conversation once anything is confirmed, and show it when it
changes or the user asks 「目前決定了什麼」. Motion decisions are per scene, with a
whole-episode line on top:

```markdown
### 動態方向紀錄
**全片**
- 風格家族：頻道預設（`softaverse`），節奏俐落（`easeout`，進場 0.4–0.6s）
- 轉場：只用硬切（`hardcut`），章節之間用閃白（`flash`）
**Seg_05｜切畫面・章節字卡**
- 已確認：Headline Rise（`rise`）＋ 浮水印慢移（`ghostword`）；範例 `kit/step-card`
**Seg_08｜疊畫面・畫面示範**
- 目前偏好：輸入框打字（`prompt`），傾向但未拍板
- 建議：打完後 Punch-in 特寫（`punchin`）——使用者尚未回應
**未決**
- 片尾要 Logo Sting 還是 End Card？
```

A suggestion is not a decision until the user agrees. When they change their mind, update
the line rather than appending a contradiction. Write this to a file only when asked.

## When the user asks to build it

This skill stops at words. Building follows hf-studio's own rules in its `CLAUDE.md` —
text storyboard, static storyboard, then the composition, each waiting for the user's ok —
and the `hyperframes-animation` / `hyperframes-core` skills; a whole episode goes through
`youtube-production`. Hand over only the confirmed lines of the record, each with its 範例
path, so the builder can read how the reference does it. If something needed is still
under 未決, ask about that one item rather than guessing.
