# Discovery — question banks and technique

Read when Discovery is needed. Remember the governing rule from SKILL.md:

> **If the answer would not change the implementation, do not ask it.**

Max 3 questions per round. Prefer `AskUserQuestion` when options are enumerable.

## Step 0 — infer before asking

In an existing codebase, most technical answers are already on disk. Read, then ask only
about the gaps.

| Question you were about to ask | Where the repo already answers it |
|---|---|
| What's the tech stack? | `package.json`, `go.mod`, `pyproject.toml`, `Gemfile` |
| What are the core entities? | `prisma/schema.prisma`, `migrations/`, `entities/`, `models/` |
| How is auth handled? | middleware, guards, `auth/` module, session config |
| Where does it deploy? | `Dockerfile`, `vercel.json`, `fly.toml`, `.github/workflows/` |
| What conventions apply? | `CLAUDE.md`, `AGENTS.md`, `.eslintrc`, existing sibling modules |
| Is there an existing test strategy? | `__tests__/`, `*.spec.ts`, CI config |

Asking the user something the code states plainly is the fastest way to make this skill
feel like overhead.

## Question banks by state

Pick from the axis that is missing. Do not run the whole bank.

### Problem — is this real?

- 現在沒有這個東西的時候，他們怎麼解決？
- 這件事一週發生幾次？（頻率決定值不值得自動化）
- 上一次因為這個問題出事，損失是什麼？

### User — who is v1 for?

- 第一批使用者是誰？具體到「哪家公司的哪個角色」的程度。
- 他們現在用什麼工具？我們要取代還是接上去？
- 有幾種角色？如果超過兩種，哪一種是 v1 唯一要服務的？

### Outcome — what must work?

- 如果只有一件事能成功，那件事是什麼？
- 使用者做完什麼動作，你就知道這個想法成立？
- 怎麼衡量？（一個數字，不是形容詞）

### Scope — what's in v1?

- 如果一週後就要上線，只能做三件事，是哪三件？
- 哪些功能你「知道最後會需要」但 v1 可以不要？
- 有沒有東西是設計上要預留、但先不實作的？

### Constraint — what boxes us in?

- 有沒有不能用的技術、平台、雲？
- 現有系統要接嗎？哪一個？
- 有沒有法規、稽核、資料落地的要求？
- 有沒有硬性期限？

### Technical (only when it changes architecture)

- 預期規模？（決定要不要現在就處理 queue / cache / sharding）
- 有沒有即時性需求？（聊天、通知、狀態同步 → WebSocket vs polling）
- 要接哪些外部服務？金流、通知、第三方 API？

## Questioning technique

The difference between a useful question and an interview question:

**Use a concrete scenario, not a category.**
- ❌ 需要通知功能嗎？
- ✅ 小明報名成功後，他在哪裡看到確認？Email？簡訊？站內？

**Anchor with an analogy the user already knows.**
- ✅ 這個模式比較像 Meetup（公開報名）還是 Discord（邀請制）？

**Offer options instead of an open field.** (This is what `AskUserQuestion` is for.)
- ✅ 付款時機有三種：A. 報名當下付清 B. 先付訂金 C. 事後付款 — 你要哪種？

**Expose hidden complexity behind a "simple" word.**
- ✅ 「線上付款」包含：多種付款方式、退款、分潤、發票、對帳 — v1 要做到哪一層？

**Challenge an assumption in the same breath as asking.**
- ✅ 你提到保險，但那通常需要跟保險公司簽約加上法遵。有合作對象了嗎？還是可以放 Phase 2？

**Surface race conditions and reversals early** — these change the data model, so they
are Discovery questions, not implementation details:
- 兩個人同時搶最後一個名額會怎樣？
- 取消 / 退款流程是什麼？
- 資料刪除是軟刪除還是硬刪除？有沒有稽核需求？

## When the user wants to skip Discovery

Ask exactly three, then start:

1. 核心使用者是誰，成功長什麼樣？（一句話）
2. P0 要證明的那一件事是什麼？
3. 有沒有硬性限制？（技術、法規、期限 — 有/沒有 + 一句話）

If they answer all three, that is enough to write a P0 plan. Do not ask for more.

## Exit criteria

Leave Discovery when:

- The Outcome is one sentence.
- v1 scope is bounded, with at least one thing explicitly excluded.
- No open constraint would force a rewrite if answered the other way.

Unanswered questions that do *not* meet that bar go into the plan's **Open questions**
section. They are not blockers.
