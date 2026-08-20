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

- Without this thing, how do they solve it today?
- How many times a week does this happen? (Frequency decides whether automation is worth it.)
- The last time this problem bit them, what did it cost?

### User — who is v1 for?

- Who are the first users? Specific down to "which role at which company".
- What tools do they use today? Are we replacing them or plugging into them?
- How many roles are there? If more than two, which single one does v1 serve?

### Outcome — what must work?

- If only one thing could work, what is that thing?
- What action, once a user completes it, tells you the idea holds up?
- How is it measured? (A number, not an adjective.)

### Scope — what's in v1?

- If it ships in a week and you can build only three things, which three?
- Which features do you "know you'll eventually need" but v1 can go without?
- Is there anything the design should leave room for but not implement yet?

### Constraint — what boxes us in?

- Any technology, platform, or cloud that is off the table?
- Does it have to integrate with an existing system? Which one?
- Any regulatory, audit, or data-residency requirements?
- Any hard deadline?

### Technical (only when it changes architecture)

- Expected scale? (Decides whether queue / cache / sharding matter now.)
- Any real-time requirement? (Chat, notifications, state sync → WebSocket vs polling.)
- Which external services are involved? Payments, notifications, third-party APIs?

## Questioning technique

The difference between a useful question and an interview question:

**Use a concrete scenario, not a category.**
- ❌ Do you need notifications?
- ✅ After Ming signs up successfully, where does he see the confirmation? Email? SMS? In-app?

**Anchor with an analogy the user already knows.**
- ✅ Is this more like Meetup (open sign-up) or Discord (invite-only)?

**Offer options instead of an open field.** (This is what `AskUserQuestion` is for.)
- ✅ There are three payment timings: A. pay in full at sign-up  B. deposit up front  C. pay afterwards — which one?

**Expose hidden complexity behind a "simple" word.**
- ✅ "Online payment" covers: multiple payment methods, refunds, revenue splits, invoices, reconciliation — how far does v1 go?

**Challenge an assumption in the same breath as asking.**
- ✅ You mentioned insurance, but that usually needs a contract with an insurer plus compliance work. Do you have a partner already, or can it go to Phase 2?

**Surface race conditions and reversals early** — these change the data model, so they
are Discovery questions, not implementation details:
- What happens when two people grab the last spot at the same time?
- What is the cancellation / refund flow?
- Is deletion soft or hard? Is there an audit requirement?

## When the user wants to skip Discovery

Ask exactly three, then start:

1. Who is the core user, and what does success look like? (One sentence.)
2. What is the one thing P0 must prove?
3. Any hard constraints? (Tech, regulation, deadline — yes/no plus one sentence.)

If they answer all three, that is enough to write a P0 plan. Do not ask for more.

## Exit criteria

Leave Discovery when:

- The Outcome is one sentence.
- v1 scope is bounded, with at least one thing explicitly excluded.
- No open constraint would force a rewrite if answered the other way.

Unanswered questions that do *not* meet that bar go into the plan's **Open questions**
section. They are not blockers.
