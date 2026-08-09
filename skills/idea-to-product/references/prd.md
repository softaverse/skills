# COMPLEX mode — PRD

Only for multi-role systems, real stakeholder alignment, or builds over ~4 weeks.
If a Feature List can carry the decisions, use that instead.

**Delete every section you have nothing concrete to say about.** A PRD with placeholder
sections is worse than no PRD — it hides which decisions are actually made.

```markdown
# [Project] — PRD

**Author**: · **Date**: · **Status**: Draft / In review / Accepted

## 1. One-liner
[Product] is a [form] that lets [users] [core action].

## 2. Background
The pain, how it's handled today, and what changed to make this worth doing now.
Include the Challenge verdict: what existing tool was considered and why it doesn't fit.

## 3. Outcome & metrics
| Goal | Metric | Target |
|---|---|---|
| | | |

### Non-goals
What we are explicitly not pursuing. This section prevents more scope creep than any other.

## 4. Roles
### [Role]
- Who they are, what they're trying to accomplish, how often they show up
- What they can and cannot do

Mark which roles are **v1** and which are deferred.

## 5. Core flows
Write out the 1–2 flows that matter. Steps, then exceptions.

    Step 1: opens [page] → sees [what]
    Step 2: clicks [action] → [system does what]
    Step 3: sees [result]

Exceptions:
- If [X] → [handling]
- If [Y] fails → [recovery]

## 6. Functional requirements

**FR-001: [title]**
- Description: specific enough to build from — which page, which control, what result
- Level: P0 / P1 / P2 / P3
- Acceptance: Given [state], when [action], then [result]
- Edge cases: [list]

No filler. Never write "needs a good user experience".

## 7. Non-functional requirements
Only the ones with a real number attached.
- Performance: page load < Xs (p95), API < Xms (p99)
- Security: auth method, encryption at rest/in transit, compliance regime
- Scale: expected concurrent users, data growth per month

Anything you can't put a number on probably belongs in P2/P3, not here.

## 8. Data model
### [Entity]
| field | type | constraints | notes |
|---|---|---|---|
| id | UUID | PK | |

Relationships, and the indexes the core flows require.

## 9. Architecture
| Layer | Choice | Why |
|---|---|---|

External services, with the alternative you rejected and the reason.

## 10. Scope
- **v1 (P0)**: [list]
- **Deferred**: [item] — [why]
- **Reserved, not built**: [designed-for but unimplemented]

## 11. Roadmap
| Level | Focus | Estimate | Deliverable |
|---|---|---|---|
| P0 Validate | The single core flow, end to end | | Something a real user can try |
| P1 Make it work | Real data, unhappy paths | | Usable daily |
| P2 Make it good | UX, errors, tests | | Won't embarrass you |
| P3 Scale | Perf, monitoring, CI/CD | | Survives growth |

Estimates should be realistic, not aspirational.

## 12. Risks
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|

## 13. Open questions
- [ ] [Non-blocking only — blockers get resolved before this document ships]
```

## Quality bar

- A new engineer reads it and starts on P0 without a follow-up question.
- Every feature says which page, which control, what result.
- Every tech recommendation names a specific library or service.
- Every deferred item says why it was deferred.
