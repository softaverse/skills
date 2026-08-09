# Challenge — should this be built at all?

Read when the input is in **Idea** or **Problem** state. The goal is to kill bad builds
cheaply and shrink good ones, in one short exchange — not to talk the user out of things.

## The build-vs-buy ladder

Walk down. Stop at the first rung that satisfies the outcome.

| Rung | Question | If yes |
|---|---|---|
| 0 | Does the outcome happen already, just manually? | Is manual actually fine at this volume? |
| 1 | Is there an off-the-shelf product for this? | Name it, name what it misses |
| 2 | Can existing tools be glued? (Zapier, Make, Sheets + Apps Script) | Propose the glue, estimate hours |
| 3 | Is it a script, not a product? (cron + shell/Python) | Write the script instead |
| 4 | Is it a thin layer on someone's API? | Build the layer, not the platform |
| 5 | Genuinely needs a product | Proceed to Discovery |

Most "我想做一個 SaaS" requests stop at rung 1–3.

## The five cuts

Apply to any idea that survives the ladder:

1. **Cut the users.** One user type in v1. Multi-role is a Phase 2 decision.
2. **Cut the platforms.** One platform. Not web + iOS + Android.
3. **Cut the persistence.** Does v1 need a database, or does a JSON file / localStorage prove it?
4. **Cut the accounts.** Does v1 need login, or can it work anonymously / single-tenant?
5. **Cut the automation.** Can a human do the hard step manually for the first 10 users?

If the idea still holds after all five, it is probably real.

## Stating the verdict

Five lines maximum. Format:

```
現成方案：<tool>，覆蓋 ~X%
缺口：<the specific thing it can't do>
判斷：<build / don't build / build a thin layer>
如果要做，P0 只需要：<one sentence>
```

Never hedge into a question. Give the verdict, then let the user override.

## Worked examples

### Kill — 線上預約 SaaS

> 「我要做一個線上預約 SaaS，讓客戶選時段、自動寄確認信。」

- Rung 1 hit: Calendly, Cal.com, SimplyBook cover this outright.
- Verdict: don't build. Recommend Cal.com (self-hostable if data residency matters).
- Reopen only if the real requirement is something Calendly structurally cannot do —
  multi-practitioner resource conflicts, health-record linkage, offline operation,
  local payment rails.

### Shrink — 診所預約系統

> 「我想做一個給診所使用的線上預約系統，要能對接健保、多醫師排班。」

- Rung 1 misses: 健保 integration is not in any off-the-shelf booking tool.
- But: 排班 + 提醒 is solved. Only the 健保 layer is novel.
- Verdict: build the thin layer. P0 = 健保 資料對接 proven against one clinic's real data.
  Scheduling UI in P0 is a stock component, not the risk.

### Keep, and skip Challenge — 滑鼠放大器

> 「我想做 Mac 滑鼠放大器，快捷鍵放大。」

- Scope is already concrete → this is **MVP state**, not Idea state.
- Challenge does not run. Go straight to Plan/Build.
- Cheap sanity check only: macOS 內建 Accessibility Zoom 是否已足夠？One line, then move on.

### Descope — 內部工具 with a dashboard

> 「做一個內部工具，讓團隊看到每天的訂單狀況，要有 dashboard 跟權限管理。」

- Rung 2 hit for the dashboard: Metabase / Retool over the existing DB, zero code.
- Permissions: the DB already has users. Don't rebuild authz.
- Verdict: Metabase, one afternoon. Revisit only when a custom write-action is needed.

## When to stop challenging

Once per idea. If the user has heard the verdict and still wants to build it, that is
their call — record the reason in the plan's Decision Log and move on. Repeating the
challenge is being annoying, not being rigorous.
