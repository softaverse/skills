# ENGINEERING mode — Technical Spec

For non-trivial architecture or a real API surface. Not needed when the build is a
straightforward CRUD layer on an existing stack — in that case the Feature List's data
sketch is enough.

Delete sections that don't apply.

```markdown
# [System/Feature] — Technical Spec

**Author**: · **Date**: · **Status**: Draft / In review / Accepted

## 1. Overview
What is being designed and why. Link the PRD or Feature List it implements.

## 2. Goals, non-goals, constraints
- Goals: what this design must achieve
- Non-goals: what it deliberately does not solve
- Constraints: must use [existing DB/framework], must stay compatible with [what]

## 3. Architecture
High-level components and data flow (text or ASCII is fine).

For each component: responsibilities, inputs/outputs, dependencies.

## 4. Data model
### [Entity]
| field | type | constraints | notes |
|---|---|---|---|
| id | UUID | PK | |

Relationships. Then the indexing strategy, justified by the queries that need it:

| table | index | type | driven by |
|---|---|---|---|
| users | email | UNIQUE | login lookup |

Migration path: how this schema evolves without a rewrite.

## 5. Key design decisions
### [Decision title]
- Background: why a decision is needed here
- Options: A, B, C
- Chosen: B
- Rationale: ...
- Trade-off accepted: we give up X to get Y
- Reversal cost: how expensive is it to switch later

Record these even when the choice feels obvious — the reversal cost is the part
future-you will want.

## 6. Security
Authn/authz approach, input validation strategy, data protection, secrets handling.

## 7. Testing
- Unit: business logic
- Integration: API contracts
- E2E: the P0 happy path, at minimum
- Load: only if there is a stated scale target

## 8. Deployment
Feature flags for risky changes, migration steps, and a rollback plan with reversible
steps. Blue/green or canary where the risk justifies it.

## 9. Observability
Structured logs with request IDs, key metrics, alert thresholds, SLOs for critical
endpoints. Scope this to P2/P3 unless an outage during P0 would be costly.
```

---

## API Requirements

Use when the API *is* the product.

```markdown
# [API] — Requirements

## Overview
What it does, who calls it, interaction model (REST / GraphQL / gRPC).

## Auth
Mechanism (API key / OAuth2 / JWT), permission model, rate limiting.

## Endpoints

### `GET /api/v1/[resources]`
| param | type | required | description |
|---|---|---|---|
| page | int | no | default 1 |
| limit | int | no | default 20, max 100 |

Response `200`:
    { "data": [...], "pagination": { "page": 1, "limit": 20, "total": 150 } }

### `POST /api/v1/[resources]`
Body, validation rules per field, `201` response, error codes (400/401/409/422).

## Error format
    {
      "error": {
        "code": "VALIDATION_ERROR",
        "message": "human-readable",
        "details": [...]
      }
    }

## Versioning
URL path / header, and the deprecation policy.
```

---

## Decision Log

A standalone log when decisions accumulate across the project.

```markdown
## [Decision]
**Date**: · **Status**: Proposed / Accepted / Superseded by [X]

**Background** — what forced the decision
**Options** — A / B / C, each with pros, cons, effort (S/M/L)
**Decision** — chosen option
**Rationale** — why this one
**Consequences** — new constraints this introduces
```
