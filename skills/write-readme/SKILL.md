---
name: write-readme
description: Write or restructure a project README using the 8-section structure common to high-star GitHub projects (Overview, Features, Demo, Getting Started, Usage, Documentation, Contributing, License), and move Architecture / API / Database / Deployment / Troubleshooting into docs/. Use when the user asks to create, rewrite, review, or clean up a README, says their README is too long or unstructured, or is preparing a project for open source or launch.
model: sonnet
---

# Write README

A README is the project's **entry point**, not its full technical documentation. It answers five questions and then hands off:

```
README.md
├── What is this?        → Overview
├── What can it do?      → Features
├── How do I install it? → Getting Started
├── How do I use it?     → Usage
└── Where are the docs?  → Documentation → docs/
```

Everything deeper — architecture, API, database, deployment, troubleshooting — lives in `docs/`, not the README.

## The 8 Sections

Use these, in this order, for a normal AI MVP / SaaS / web app:

1. **Overview** — what it is, what problem it solves, who it's for
2. **Features** — 3–6 core capabilities as bullets
3. **Demo** — live URL, screenshot, or video (skip if there's no UI)
4. **Getting Started** — Prerequisites → Installation → Environment Variables → Development
5. **Usage** — the basic path to actually using it
6. **Documentation** — links into `docs/` or a docs site
7. **Contributing** — how to participate (open source)
8. **License** — required for open source

Minimum viable README: **Overview → Features → Getting Started → Usage → License**.

## Do Not Put In README

Architecture, Project Structure, API reference, Database schema, Deployment, Troubleshooting, Roadmap. These are `docs/` files by default. Only inline one if the project is tiny and the section is a few lines.

## Core Workflow

1. **Read the project** — `package.json`, entry points, existing README, `.env.example`, scripts
2. **Choose scope** — full 8 sections, or minimum viable if it's a small/internal project
3. **Draft README.md** from the template
4. **Extract overflow** — move anything long or deep into `docs/*.md` and link it from Documentation
5. **Verify** — every command runs, every link resolves, no placeholder text left

## Reference Routing

- **[references/readme-template.md](./references/readme-template.md)** — Read this for the copy-paste README skeleton, the minimum-viable variant, and badge/demo conventions.
- **[references/section-guide.md](./references/section-guide.md)** — Read this for what belongs in each section, how long it should be, and the frequency table of sections across high-star projects.
- **[references/docs-structure.md](./references/docs-structure.md)** — Read this when splitting content out of the README into `docs/`: which file each topic goes to and how to link back.
- **[references/review-checklist.md](./references/review-checklist.md)** — Read this when auditing or trimming an existing README rather than writing a new one.

## Quality Checks

- ✓ Title, one-line description, and Overview answer "what is this" within the first screen
- ✓ A new user can go from clone to running from Getting Started alone
- ✓ No Architecture / API / Database / Deployment sections inline
- ✓ Every `docs/` link in Documentation points to a file that exists
- ✓ All code blocks are language-tagged and copy-pasteable
