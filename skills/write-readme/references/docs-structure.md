# Splitting Content Into `docs/`

## Default layout

```
README.md          ← entry point only
docs/
├── architecture.md
├── api.md
├── database.md
├── deployment.md
└── troubleshooting.md
```

Create only the files the project actually needs. An empty stub is worse than no link.

## Where each topic goes

| Content | Destination |
| --- | --- |
| System design, data flow, module boundaries, diagrams | `docs/architecture.md` |
| Directory/file layout explanation | `docs/architecture.md` (or omit — the repo tree already shows it) |
| Endpoint reference, request/response shapes, auth | `docs/api.md` |
| Schema, migrations, seeding, ERD | `docs/database.md` |
| Hosting, CI/CD, build config, production env vars | `docs/deployment.md` |
| Common errors and fixes, FAQ | `docs/troubleshooting.md` |
| Full CLI option reference, advanced recipes | `docs/usage.md` |
| Version history | `CHANGELOG.md` (repo root) |
| Contribution process detail | `CONTRIBUTING.md` (repo root) |

## Extraction procedure

1. Identify README sections that exceed ~15 lines or explain internals rather than usage.
2. Move each into its `docs/` file **verbatim first**, then edit for standalone readability — add a title and a one-line intro, since the section no longer has README context around it.
3. Replace the README section with a link under **Documentation**.
4. Fix relative links: a link that worked from README root (`docs/foo.md`, `src/x.ts`) becomes `./foo.md` / `../src/x.ts` inside `docs/`.
5. Give each `docs/` file a back-link to the README when it's part of a reading path.

## Keep in the README anyway

- Env vars needed just to boot the dev server (production-only config goes to `docs/deployment.md`)
- A single-sentence "how it works" summary, even when a full architecture doc exists
- The one usage example that proves the project works

## When a docs site exists

If the project has a documentation website (Docusaurus, Mintlify, Nextra), the Documentation section is a single link to it. Don't maintain both `docs/*.md` and a site with overlapping content.
