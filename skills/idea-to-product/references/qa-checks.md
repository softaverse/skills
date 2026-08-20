# Review gates

Read during the Review phase, before handing a plan over to Build.

## Drive the review — don't ask "any thoughts?"

Three targeted questions, then iterate:

1. Is the Outcome right? — "This P0 is meant to prove [X]. Correct?"
2. Is v1 too big? — Name the item you would cut first, and let the user push back.
3. Any objection to the tech stack?

Anything the user doesn't object to is agreed. Move on.

## Artifact gates

The plan is not ready to build from until all of these pass:

- [ ] **One-liner** — product, user, problem, in one sentence
- [ ] **Outcome** — the single thing P0 must prove, with a number attached
- [ ] **Challenge verdict recorded** — which existing tool was considered, why it doesn't fit
- [ ] **Roles** — who v1 serves, and which roles are explicitly deferred
- [ ] **Prioritised features** — every item tagged P0/P1/P2/P3
- [ ] **1–2 core flows** written out step by step, with exceptions
- [ ] **Data sketch** — entities and relationships, enough to write the schema
- [ ] **Tech choices** — each names a specific library/service and a reason
- [ ] **External dependencies** — third-party services listed
- [ ] **Out of scope** — with a reason per item
- [ ] **Open questions** — and none of them blocks P0
- [ ] **Risks** — with mitigations, not just names

## Red flags — send it back

| Symptom | What it means |
|---|---|
| P0 contains auth, billing, admin, or CI | Scaffolding disguised as validation |
| Every template section is filled | Placeholder padding — cut the empty ones |
| A feature says "good UX" or "easy to use" | Not a requirement; delete or make it specific |
| No item in "out of scope" | Scope was never actually bounded |
| Estimates are all round numbers with no basis | Nobody thought about sequencing |
| The document is longer than the P0 build | Wrong output mode — drop a level |

## Final gate

> Could an engineer who wasn't in this conversation start P0 tomorrow
> without asking a follow-up question?

If no, the plan isn't done. If yes, stop planning and build.
