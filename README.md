# Softaverse Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A curated collection of agent skills for Claude Code, Cursor, Codex, and every other
agent that reads `SKILL.md`.

## Quickstart

```bash
npx skills add softaverse/skills
```

Pick the skills you want from the interactive list and choose which agents to install
them into. No global install, no account, nothing to configure.

```bash
# See what's in here without installing
npx skills add softaverse/skills --list

# Install one skill into Claude Code and Cursor
npx skills add softaverse/skills --skill extract-design-system -a claude-code -a cursor

# Install everything, everywhere
npx skills add softaverse/skills --all

# Update later
npx skills update
```

`skills` is the [open agent skills CLI](https://github.com/vercel-labs/skills) — it works
with any repository, this one included.

## Skills

| Skill | Use it for |
| --- | --- |
| [`extract-design-system`](skills/extract-design-system/SKILL.md) | Extracting design tokens and reusable components from a website URL or local HTML file. |
| [`code-reviewer`](skills/code-reviewer/SKILL.md) | Reviewing recently changed code for bugs, security, and performance issues. |
| [`explain-code`](skills/explain-code/SKILL.md) | Explaining code with visual diagrams and everyday analogies; great for teaching and onboarding. |
| [`write-readme`](skills/write-readme/SKILL.md) | Restructuring a README into the 8-section entry-point layout and moving deep docs into `docs/`. |
| [`git-commit-optimizer`](skills/git-commit-optimizer/SKILL.md) | Writing conventional commits, splitting large diffs, and cleaning up commit history. |
| [`idea-to-product`](skills/idea-to-product/SKILL.md) | Turning product ideas into concise, actionable plans and implementation roadmaps. |
| [`optimize-images`](skills/optimize-images/SKILL.md) | Converting and compressing PNG/JPG to WebP and updating source references. |
| [`obsidian-formatter`](skills/obsidian-formatter/SKILL.md) | Formatting Markdown for correct display in Obsidian (tables, code blocks, headings). |
| [`draw-mermaid-diagrams-for-obsidian`](skills/draw-mermaid-diagrams-for-obsidian/SKILL.md) | Creating Mermaid diagrams tailored for Obsidian notes. |
| [`route-skill-references`](skills/route-skill-references/SKILL.md) | Refactoring a bloated skill into a lean `SKILL.md` plus on-demand reference files. |

## Requirements

- Node.js 18 or newer (only to run `npx skills`; the skills themselves are plain Markdown).

## Contributing

Each skill is one directory under `skills/`:

```
skills/my-skill/
  SKILL.md          # frontmatter (name + description) and the instructions
  references/       # optional, loaded only when SKILL.md routes to it
  scripts/          # optional
```

The `name` in the frontmatter must match the directory name, and `description` should say
both *what* the skill does and *when* to use it — that sentence is the only thing an agent
sees before deciding to load the skill.

Before opening a pull request, confirm the skill is discoverable and add it to the table
above:

```bash
npx skills add . --list
```

A skill missing required frontmatter is reported as skipped rather than listed.

## Using these skills locally

This repository ignores `.claude/skills/`, so install into it like any other consumer:

```bash
npx skills add . -a claude-code
```

## Previous CLI

Versions up to `softaverse@1.0.1` shipped a dedicated `npx softaverse` CLI. It has been
retired in favour of `npx skills`, which does the same job across many more agents and is
maintained by a wider community. Existing installs keep working; there is nothing to
migrate beyond switching the install command.

## License

[MIT](LICENSE)
