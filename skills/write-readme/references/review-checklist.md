# README Review Checklist

Use when auditing or trimming an existing README instead of writing a new one.

## 1. Structure

- [ ] H1 project name, then a one-line description
- [ ] Sections appear in order: Overview → Features → Demo → Getting Started → Usage → Documentation → Contributing → License
- [ ] No section is present that the project doesn't need (an empty Contributing section on a private repo is noise)
- [ ] No duplicated content between sections

## 2. Overflow to move out

Flag any of these that appear inline and move them to `docs/` (see `docs-structure.md`):

- [ ] Architecture / system design
- [ ] Project structure tree beyond ~10 lines
- [ ] API endpoint reference
- [ ] Database schema
- [ ] Deployment / CI config
- [ ] Troubleshooting / FAQ
- [ ] Any single section longer than ~15 lines that isn't Getting Started or Usage

## 3. Correctness

- [ ] Every command runs as written on a clean clone
- [ ] Package name, install command, and repo URL match `package.json` / the actual remote
- [ ] Prerequisites list real versions, not "latest"
- [ ] Env var names match `.env.example` and the code
- [ ] Every internal link resolves to a file that exists
- [ ] Images and demo URLs load

## 4. Content quality

- [ ] The first screen answers "what is this and why would I use it"
- [ ] Features are capabilities, not marketing adjectives
- [ ] Usage shows at least one concrete input → output
- [ ] No `TODO`, `Coming soon`, `Lorem ipsum`, or template placeholders
- [ ] No stale references to renamed/removed commands or files

## 5. Formatting

- [ ] All code blocks language-tagged
- [ ] Tables used for enumerable data (env vars, commands, options)
- [ ] Consistent heading levels (no jump from `##` to `####`)
- [ ] Badges limited to 3–4 and all resolving

## Output when reviewing

Report as: what to delete, what to move (with destination file), what to add, what's broken. Apply changes only after the user confirms scope, unless they asked for a rewrite outright.
