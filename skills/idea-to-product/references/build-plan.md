# BUILD mode — Build Plan and implementation guidance

Read when the plan is agreed and code starts. The build plan is short — it exists to keep
P0 honest, not to document the project.

## Build plan template

```markdown
# [Project] — Build Plan

## P0 — Validate
**Proves**: [the one thing]
**Done when**: [a real person can do X and the result is Y]

- [ ] [task]
- [ ] [task]

Deliberately skipped in P0: auth, billing, analytics, admin, Docker, CI/CD, i18n
(unless one of these *is* the thing being validated).

## P1 — Make it work
**Done when**: [someone can use it daily without a workaround]
- [ ] Real persistence
- [ ] The unhappy paths that actually occur
- [ ] [task]

## P2 — Make it good
- [ ] UX pass on the core flow
- [ ] Error handling and empty/loading states
- [ ] Tests on business logic and the P0 path

## P3 — Scale
- [ ] Performance targets
- [ ] Monitoring and alerts
- [ ] CI/CD, automation

## Decision points needing the user
- [ ] [thing to ask before building it, not after]
```

## Sequencing

**Greenfield** — build the thinnest vertical slice first, not the layers:

1. One route/screen that exercises the core flow end to end, hardcoded data is fine
2. Replace the hardcoded data with a real schema, once the flow proved worth persisting
3. Widen to the remaining P0 steps
4. Only then: project scaffolding hardening, configs, CI

Building schema → API → frontend in that order means nothing is testable until the end.
That is how P0 turns into three weeks.

**Existing codebase** — the repo's conventions outrank everything here:

1. Read the neighbouring modules and match their structure, naming, and error handling
2. Follow `CLAUDE.md` / `AGENTS.md` if present
3. Extend existing abstractions before introducing new ones
4. Do not restructure the project as a side effect of adding a feature

## Principles

- **Check in after each level.** Do not go dark and deliver everything at the end.
- **Stop at real decision points and ask.** An assumption baked into P1 is expensive.
- **Production-grade code, demo-grade scope.** Cut features, not quality.
- Comment the *why* behind business rules; the *what* is already in the code.
- Prefer small deployable units. Feature-flag anything risky.

## Level exit gates

Do not start the next level until the current one is user-visible:

| Level | Gate |
|---|---|
| P0 → P1 | A real user completed the core flow at least once |
| P1 → P2 | Someone used it for real work without a manual workaround |
| P2 → P3 | Quality complaints stopped; growth is the next constraint |

If P0 fails its gate, the answer is usually to change the idea, not to start P1.
