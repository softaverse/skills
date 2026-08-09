# Softaverse

[![npm version](https://img.shields.io/npm/v/softaverse.svg)](https://www.npmjs.com/package/softaverse)
[![npm downloads](https://img.shields.io/npm/dm/softaverse.svg)](https://www.npmjs.com/package/softaverse)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Install AI agent skills into Claude Code, Codex, Cursor, Windsurf, GitHub Copilot, and more.

![Softaverse CLI demo](docs/demo.gif)

## Quickstart

List available skills:

```bash
npx softaverse list
```

Install a skill:

```bash
npx softaverse add extract-design-system
```

Install a skill into specific tools:

```bash
npx softaverse add extract-design-system --target claude-code codex cursor
```

## Features

- Install skills into multiple AI coding tools.
- Use interactive prompts or scriptable flags.
- Support both skill-directory and rule-file based tools.
- Run without global installation through `npx`.

## Requirements

- Node.js 18 or newer.

## Installation

Install the CLI globally if you plan to use it often:

```bash
npm install -g softaverse
```

## Usage

Install a skill interactively:

```bash
softaverse add extract-design-system
```

Choose skills and targets interactively:

```bash
softaverse add skills
```

Install without prompts:

```bash
softaverse add extract-design-system --target claude-code codex cursor
```

List available skills:

```bash
softaverse list
```

List supported targets:

```bash
softaverse targets
```

Remove an installed skill:

```bash
softaverse remove extract-design-system
```

Every command can also be run through `npx`:

```bash
npx softaverse list
npx softaverse targets
npx softaverse add extract-design-system --target claude-code codex
```

## Skills

| Skill | Use it for |
| --- | --- |
| [`web-design`](skills/web-design/SKILL.md) | Designing modern websites with stronger visual direction and layout decisions. |
| [`extract-design-system`](skills/extract-design-system/SKILL.md) | Extracting design tokens and reusable components from a website URL or local HTML file. |
| [`code-reviewer`](skills/code-reviewer/SKILL.md) | Reviews recently written or modified code; focuses on changed files and detects bugs, security, and performance issues. |
| [`explain-code`](skills/explain-code/SKILL.md) | Explains code with visual diagrams and everyday analogies; great for teaching and onboarding. |
| [`obsidian-formatter`](skills/obsidian-formatter/SKILL.md) | Formats Markdown for correct display in Obsidian (tables, code blocks, headings, diagrams). |
| [`draw-mermaid-diagrams-for-obsidian`](skills/draw-mermaid-diagrams-for-obsidian/SKILL.md) | Create Mermaid diagrams tailored for Obsidian notes. |
| [`idea-to-product`](skills/idea-to-product/SKILL.md) | Turn product ideas into concise, actionable plans and implementation roadmaps. |
| [`optimize-images`](skills/optimize-images/SKILL.md) | Convert and compress PNG/JPG to WebP and update source references; includes scripts and workflow. |
| [`write-readme`](skills/write-readme/SKILL.md) | Write or restructure a README into the 8-section entry-point structure and move deep docs into `docs/`. |
| [`route-skill-references`](skills/route-skill-references/SKILL.md) | Refactor Skills into a lean SKILL.md with topic-specific reference files for progressive disclosure. |

## Supported targets

| Tool | Target key | Installed to |
| --- | --- | --- |
| Claude Code | `claude-code` | `.claude/skills/<skill>/` |
| Codex | `codex` | `.codex/skills/<skill>/` |
| Antigravity | `antigravity` | `.agents/skills/<skill>/` |
| Cursor | `cursor` | `.cursor/rules/<skill>.mdc` |
| Windsurf | `windsurf` | `.windsurf/rules/<skill>.md` |
| GitHub Copilot | `github-copilot` | `.github/copilot-instructions.md` |
| Cline | `cline` | `.clinerules/<skill>.md` |
| Roo Code | `roo-code` | `.roo/rules/<skill>.md` |
| Gemini CLI | `gemini-cli` | `GEMINI.md` |

## License

[MIT](LICENSE)
