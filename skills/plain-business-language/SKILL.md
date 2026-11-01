---
name: plain-business-language
description: Rewrite engineering jargon into plain 繁體中文 that a small-business owner (老闆) who never touches tech can understand and repeat to others — for website copy, service pages, hero headlines, proposals, quotes, self-introductions, and engineer-speak in client messages (LINE replies, progress updates, meetings) aimed at non-technical clients. Use when the user says 「老闆看不懂」「太工程師了」「白話一點」「講人話」「客戶聽得懂的說法」「這個詞要怎麼跟客戶講」, asks how to explain API / AI Agent / MVP / 串接 / 自動化 to a client, wants to audit a site or proposal for jargon, or is writing a positioning line for a tech service sold to non-technical buyers. Scans for jargon and empty buzzwords, rewrites from the owner's daily pain, checks consistency, and shows a before/after table before touching any file. Do not use for content written for developers (technical articles, docs, READMEs), for English copy, or for visual design discussions (web-design-vocabulary).
---

# Plain Business Language

The reader is a shop or company owner who has run the business for ten years and does
not touch computers. They do not care what technology you use. They care what stops
hurting, what gets faster, and what money comes in. Your job is to turn what an
engineer *can build* into what the owner *will notice*.

Always write in 繁體中文 with Taiwan usage (資料, not 數據 for data records; 軟體,
not 軟件; 網路, not 網絡).

## Where the material lives

Read only what the current task needs.

| File | Read when |
|---|---|
| `references/glossary.md` | **First stop** for any rewrite. ~200 jargon terms by category, each with plain wording and when the original term may stay. Includes a blacklist of empty buzzwords and a section of spoken engineer slang and English abbreviations (rollback, blocker, ETA, scope creep…) |
| `references/pain-points.md` | Writing headlines, service intros, or problem sections. Owner pain points by business area, each mapped to the service behind it |
| `references/patterns.md` | Restructuring whole sentences or paragraphs: rewrite patterns, headline formulas, before/after examples, self-introductions. §10 converts metrics (99.9%, 人天, ms, token) into time and money; §11 rewrites spoken engineer slang in client messages |

A term missing from the glossary is not a reason to keep it. Translate it with the
same principles (what it does for the owner, in their words), and mention the gap to
the user so the glossary can be extended.

## Step 1: Decide who is reading

Before changing anything, sort each piece of content by reader:

| Reader | Examples | What to do |
|---|---|---|
| 老闆 (non-technical buyer) | hero, service pages, pricing, contact page, nav labels, SEO description, proposals, quotes | Rewrite fully |
| 開發者 | technical articles, open-source resources, docs, talks | Leave alone. Jargon here builds credibility with the people who refer clients |
| Mixed | about page, case studies | Lead with the owner's outcome; put tech stack in a secondary spot (a small 「使用技術」 line at the end) |
| 已合作的客戶 | LINE replies, progress updates, meeting explanations | Replace the jargon and keep the message's facts as they are. See `patterns.md` §11 |

If the user has already decided which pages are in scope, follow that and don't
reopen it.

## Step 2: Scan

List every problem in the target text before rewriting. Look for:

1. **Jargon**: any term in `glossary.md`, plus English abbreviations in general (API, MVP, SaaS, CMS…)
2. **Empty buzzwords**: 智慧、賦能、打造、解決方案、一站式、全方位、數位轉型 (see the blacklist in `glossary.md`)
3. **Feature-first sentences**: sentences that start from what you build (「我們提供 AI 串接」) instead of what the owner goes through
4. **Inconsistency**: the same idea worded differently in different places (hero says 「銷售」, SEO says 「回答」); mixed 「我」/「我們」; the same service with two names
5. **Headline/subhead mismatch**: the headline speaks engineer, the subhead speaks owner. The owner only reads the headline

Report the scan as a table: 位置 | 現在的文字 | 問題類型. Sort by impact. Headlines,
navigation, and meta descriptions come first because the most people see them.

## Step 3: Rewrite

Apply these in order:

1. **Start from their day, not your skill.** Open with a situation they recognize: 「同一筆資料要在三個地方各輸入一次」, not 「跨系統資料串接」. Use `pain-points.md`.
2. **Say what changes for them.** Time saved, mistakes avoided, customers not lost, money in. Use numbers only if they are real or clearly an example.
3. **Name the thing by what it does.** 「會自己回答客人問題的 AI 店員」, not 「AI Agent」. Use `glossary.md`.
4. **Mention technology last, if at all.** Only when it reassures (「用的是 Google 的服務，資料不會不見」) or when the owner will hear the word elsewhere and should recognize it. Then explain it once, in brackets: 「AI 助手（業界叫 AI Agent）」.
5. **Keep the attractive words.** 「AI」 itself draws owners in, so keep it. What has to go is the explanation of *how* the AI works.
6. **Convert numbers into time, money, or people.** 99.9% → 「一年加起來不超過 9 小時打不開」; 40 人天 → a total price and a number of weeks. See `patterns.md` §10.
7. **One voice.** For a solo consultant, default to 「我」, which reads as personal and trustworthy. Use 「我們」 only for a real team, or for 「我們一起…」 meaning you and the client.

### Ask when information is missing

The best rewrites need facts the jargon hides. Never invent them. Ask instead, in
one short message that lists everything missing:

- **Money**: total price, monthly fees, cost of the alternative. Needed for quotes, proposals, and 「建議不做」 messages
- **Industry and customer**: who the client sells to. Needed to pass the 換人測試. Without it, a generic sentence is the best you can do
- **Real numbers**: order volume, average order value, time currently spent. Needed before converting anything into 「每月省 X 小時／X 元」

If the user wants a draft anyway, write it with visible placeholders (「X 萬元」「每月約 X 元」) and list what to fill in. Never put in a plausible-looking number.

## Step 4: Self-check

Run every rewritten sentence through these. Any 「否」 means rewrite again.

- **轉述測試**: could the owner repeat this to their spouse or a friend in their own words?
- **電話測試**: would it make sense read aloud over the phone with no visuals?
- **「所以呢？」測試**: if the owner asks 「所以呢？」 after the sentence, does the sentence already answer it?
- **換人測試**: could any other agency write the exact same sentence? If yes, it is too generic. Add their specific situation.
- **一致性**: is the same service called the same thing in every place, and is the pronoun consistent?
- **沒有黑名單詞**: no word from the buzzword blacklist survived.
- **沒有編造**: every number, price, and outcome came from the user or is a marked placeholder.

## Step 5: Show before touching files

Present a before/after table per page or section: 位置 | 修改前 | 修改後 | 理由
(short). For a headline or positioning line, offer 2–4 directions with when each
fits, and recommend one. Ask about genuinely open decisions (service names, 我 vs
我們, scope). Only edit code or files after the user confirms.

When editing code, change only user-facing strings: text, `title`, `meta
description`, `alt`, button labels. Leave identifiers, routes, and slugs alone
unless the user asks, since renaming a URL can break SEO and links.

## Tone

- Short sentences. One idea per sentence.
- Concrete nouns: 訂單、預約、客人、Excel、LINE、發票, not 資料流、流程、場景.
- Talk to the reader as 「你」.
- Don't talk down. 「看不懂技術沒關係」 is fine once. Don't repeat it, and don't over-explain.
- Don't promise what can't be guaranteed (「保證業績翻倍」). Describe the mechanism instead: 「半夜來問的客人，也有人回答」.
