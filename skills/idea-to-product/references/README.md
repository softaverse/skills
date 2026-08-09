# References — idea-to-product

**Maintainer-facing index. Not a runtime reference — `SKILL.md` decides what to read and when.**

| File | Phase | Contents |
|---|---|---|
| `challenge.md` | Challenge | Build-vs-buy ladder, the five cuts, worked kill/keep examples |
| `discovery.md` | Discovery | Repo-inference map, question banks by axis, questioning technique |
| `feature-list.md` | Output: MVP | Feature list template, user stories variant |
| `prd.md` | Output: COMPLEX | PRD template |
| `technical-spec.md` | Output: ENGINEERING | Tech spec, API requirements, decision log |
| `build-plan.md` | Output: BUILD | Build plan template, sequencing, level exit gates |
| `qa-checks.md` | Review | Review questions, artifact gates, red flags |

## Invariants

- `SKILL.md` holds everything that must fire **at decision time** — intent detection,
  the Challenge questions, the "don't ask what won't change the plan" rule, the P0–P3
  ladder, guardrails. Behaviour never moves into `references/`: there is no trigger that
  makes the model read a file it hasn't decided it needs.
- `references/` holds only what is looked up **after** a decision — templates, question
  banks, worked examples.
- One hop only: `SKILL.md` → one reference. References do not chain.
- Each rule lives in exactly one file.
- This README is not routed from `SKILL.md`. Update it when files are added, removed,
  or renamed.
