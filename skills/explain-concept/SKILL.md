---
name: explain-concept
description: Explain a technology, tool, protocol, format, or API as an evolution story — the problem it solves, how people did it before, what changed, a minimal runnable example, and whether this project actually needs it. Use for "what is X?", "why does X exist?", "should I use X?", "X vs Y" questions about a named technology (npx skills, MCP, BLE GATT, Remotion, a lock file, an API). For explaining code that already exists in the repo, use explain-code instead.
---

# Explain a technology, not just define it

A definition alone is useless. What makes a technology click is knowing what pain
it was born from, and whether that pain is yours.

Answer in 繁體中文, but keep technical terms in English — write "MCP 是一個讓 agent
連到外部 tool 的 protocol", never "模型上下文協定".

## The six sections

Use these as the shape of the answer, not as literal headings to fill in. Each one
earns its place or gets dropped.

### 1. 一句話定義

One or two sentences, plain language, no jargon that itself needs explaining.
This is the anchor — without it, everything after sounds like fog.

### 2. 為什麼會有它

The core of the answer. Tell it as one continuous story, not three bullet lists:

- **原本的痛點** — what specifically hurt. Be concrete: which manual step, which
  duplicated file, which thing that broke at 3am.
- **以前怎麼做** — the workaround people actually shipped before this existed.
  Name it if it has a name (`curl` + cron, copy-pasting the prompt into every repo,
  polling every 5 seconds).
- **它改掉了什麼** — the one structural thing that is different now. Not a feature
  list — the single shift that made the old workaround unnecessary.

If a technology has no interesting "before", say so plainly. Some things are just
a file format.

### 3. 最小可跑範例

Real, copy-pasteable, and as small as it can be while still doing something.
A command that runs, or a file with its full path and complete contents.

Not pseudocode. Not `// ... your config here`. If it genuinely needs three files
to do anything, show three small files rather than one fake one.

### 4. 你會踩的坑

One or two things that are counter-intuitive on first contact — a wrong mental
model, a silent failure mode, a thing that looks optional but isn't. Skip this
section rather than padding it with generic advice.

### 5. 這個專案需不需要

Give judgement criteria, both directions:

- **該用的訊號** — concrete conditions, e.g. 「同一份 prompt 已經複製到三個 repo」
- **不需要的訊號** — equally concrete, e.g. 「只有你一個人用、只有一台機器」

Read the current project's files only when the question is clearly about *this*
codebase (「我這個專案要不要上 MCP？」), or when the user asks directly. Check
`package.json`, the existing architecture, and what is already installed, then
answer for their actual setup. For a general question (「BLE GATT 是什麼？」),
the criteria list is the whole answer — don't go scanning files.

### 6. 一句話結論

Land it. 「你現在不需要，等到 X 發生再回來看」is a better ending than a summary
of what was already said.

## Calibration

- If the user compares two things (「X vs Y」), run section 2 once over both —
  they usually solve the same pain from different angles, and that contrast *is*
  the explanation.
- Diagrams only when structure is genuinely hard to say in words (a protocol
  handshake, a layered stack). Prose beats a box-and-arrow diagram of two boxes.
- Length follows the concept. A lock file is four sentences. BLE GATT is not.
- Never end with "希望這個解釋有幫助" or an offer to explain further.
