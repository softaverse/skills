# Softaverse Skills

[![Install via skills.sh](https://img.shields.io/badge/skills.sh-install-green)](https://skills.sh/softaverse/skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This repository contains [Agent Skills](https://agentskills.io/home) for everyday
development work — code review, documentation, design extraction, and skill authoring.
They are plain Markdown, so they work with Claude Code, Cursor, Codex, and every other
agent that reads `SKILL.md`.

> [!NOTE]
> This repository is under active development.

## Installation

```bash
npx skills add softaverse/skills
```

From the `npx skills add` command, you can select the specific skills from this repo to
install, and choose which agents to install them into.

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
with any repository, this one included. It needs Node.js 18 or newer; the skills
themselves have no runtime.

## Available Skills

<!-- BEGIN SKILLS -->
- **Code and review**
  - [**Code Reviewer**](./skills/code-reviewer) — review recently changed code for bugs, security, and performance issues.
  - [**Explain Code**](./skills/explain-code) — explain code with visual diagrams and everyday analogies, for teaching and onboarding.
  - [**Explain Concept**](./skills/explain-concept) — explain a technology as an evolution story: the problem it solves, what changed, a minimal example, and whether you need it.
  - [**Git Commit Optimizer**](./skills/git-commit-optimizer) — write conventional commits, split large diffs, and clean up commit history.
- **Design and assets**
  - [**Extract Design System**](./skills/extract-design-system) — pull design tokens and reusable components out of a website URL or local HTML file.
  - [**Optimize Images**](./skills/optimize-images) — convert and compress PNG/JPG to WebP and update source references.
- **Documentation and notes**
  - [**Write README**](./skills/write-readme) — restructure a README into the 8-section entry-point layout and move deep docs into `docs/`.
  - [**Obsidian Formatter**](./skills/obsidian-formatter) — format Markdown so tables, code blocks, and headings render correctly in Obsidian.
  - [**Draw Mermaid Diagrams for Obsidian**](./skills/draw-mermaid-diagrams-for-obsidian) — create Mermaid diagrams tailored for Obsidian notes.
- **Planning and skill authoring**
  - [**Idea to Product**](./skills/idea-to-product) — turn product ideas into concise, actionable plans and implementation roadmaps.
  - [**Route Skill References**](./skills/route-skill-references) — refactor a bloated skill into a lean `SKILL.md` plus on-demand reference files.
- **System maintenance**
  - [**Disk Audit**](./skills/disk-audit) — scan a macOS disk for reclaimable space and report a tiered cleanup list with commands.
- **Video production**
  - [**YouTube Production**](./skills/youtube-production) — plan a YouTube episode from brief to a line-numbered script and a storyboard that reuses your HyperFrames animation library (Stage A; voice retiming and DaVinci assembly in progress).
<!-- END SKILLS -->

## Using these skills locally

This repository ignores `.claude/skills/`, so install into it like any other consumer:

```bash
npx skills add . -a claude-code
```

## Support

If you need help or encounter issues with these skills, search for existing issues or open
a new one in the [GitHub Issue Tracker](https://github.com/softaverse/skills/issues).

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

Before opening a pull request, confirm the skill is discoverable and add it to the list
above:

```bash
npx skills add . --list
```

A skill missing required frontmatter is reported as skipped rather than listed.

You can also help by [reporting bugs or inaccuracies](https://github.com/softaverse/skills/issues)
in the skill Markdown files, or by filing a feature request for a new skill.

## Previous CLI

Versions up to `softaverse@1.0.1` shipped a dedicated `npx softaverse` CLI. It has been
retired in favour of `npx skills`, which does the same job across many more agents and is
maintained by a wider community. Existing installs keep working; there is nothing to
migrate beyond switching the install command.

## License

You are free to copy, modify, and distribute these skills under the terms of the MIT
license. See the [LICENSE](LICENSE) file for details.
