# MVP mode — Feature List

For a clear, small-to-medium build. Delete any section you have nothing concrete to say
about. A short list of decisions beats a long list of placeholders.

```markdown
# [Project] — Feature List

## One-liner
[Product] lets [user] [core action], so that [outcome].

## Outcome to validate
The one thing that must work for this to be worth shipping: [one sentence].
Measured by: [one number].

## Users
- Primary (v1): [who — specific]
- Deferred: [roles explicitly not served in v1]

## Features

### [Group, e.g. Booking]
| # | Feature | Level | Notes |
|---|---------|-------|-------|
| 1 | Pick a time slot | P0 | The validation path — must work end to end |
| 2 | Confirmation email | P0 | Transactional only, no templating UI |
| 3 | Cancel / reschedule | P1 | |
| 4 | Google Calendar sync | P2 | |

Levels: **P0 Validate** · **P1 Make it work** · **P2 Make it good** · **P3 Scale**

## Explicitly out of scope
| Item | Why |
|---|---|
| Multi-tenant | One clinic in v1; tenancy is a Phase 2 rewrite risk, noted below |
| Payments | Cash on site for v1 |

## Reserved but not built
Designed for, deliberately unimplemented (so v1 doesn't paint us into a corner):
- [e.g. i18n structure in place, zh-TW only shipped]

## Data sketch
Core entities and how they relate — enough for someone to create the schema.
- `Booking` → `Slot` (many-to-one), `Slot` → `Practitioner` (many-to-one)

## Tech
| Layer | Choice | Why |
|---|---|---|
| | | |

Existing stack wins unless there is a stated reason to deviate.

## Open questions
- [ ] [Only things that don't block P0]
```

---

## User Stories variant

Use instead of the feature table when the team works in sprints.

```markdown
### [Short title]
**As a** [role], **I want** [action], **so that** [benefit].

**Acceptance criteria**
- Given [precondition], when [action], then [result]
- On [error condition], [expected handling]

**Level**: P0 · **Estimate**: S/M/L · **Depends on**: [list]
```

Rules:
- The "so that" clause carries the why — if you can't write it, the story may not belong in v1.
- Acceptance criteria must be verifiable by someone who didn't write them.
- Too big? Split along the user flow, never along the technical stack
  (no "backend story" + "frontend story" for one user-visible thing).
