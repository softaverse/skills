---
name: route-skill-references
description: Refactors existing Skills into a lean SKILL.md plus topic-specific reference files for progressive disclosure. Use when simplifying a bloated Skill, splitting examples or lookup material into references, adding a reference routing map, or reorganizing Skill content so only relevant files are loaded on demand.
---

# Route Skill References

Use this skill to turn an existing Skill into a concise entry point that routes to detailed files only when needed.

## Core Rule

`SKILL.md` should contain discovery metadata, the essential workflow, and a routing map. Detailed examples, syntax, source links, long checklists, lookup material, and reusable scripts should live in `references/` and `scripts/` and be read/executed only when the task needs them.

## Reference Routing

- Routing map pattern: read `references/routing-template.md` when adding or revising the links from `SKILL.md` to reference files.
- Rewrite checklist: read `references/rewrite-checklist.md` before editing a skill with several sections, duplicated examples, or unclear routing.
- Scripts best practices: read `references/scripts-best-practices.md` when adding reusable shell scripts to the `scripts/` directory (for deterministic operations that run without context cost).
- Script scaffold: read `references/script-template.md` when writing a new script file.
- Reference index: update `references/README.md` only when adding, removing, or renaming reference files.

Do not read every reference by default. Pick the file that matches the current refactor decision.

## Workflow

1. Inspect the current Skill structure: `SKILL.md`, existing `references/`, `scripts/`, and assets.
2. Identify content categories: trigger metadata, required workflow, routing decisions, examples, source links, lookup material, and deterministic operations.
3. Keep only the trigger, purpose, workflow, and routing decisions in `SKILL.md`.
4. Move detailed material into one-hop reference files under `references/`, split by task/topic rather than by arbitrary size.
5. Extract deterministic, repetitive operations into modular shell scripts under `scripts/`; each script takes parameters and produces structured output.
6. Add or update a routing map that says when each reference should be read or each script should be executed.
7. Add an explicit fallback for uncovered topics: use the official or upstream docs, and keep external-source instructions narrow.
8. Remove duplicate content so a rule, example, source list, or script lives in one place.

## Output Shape

- `SKILL.md`: frontmatter, concise task instructions, reference routing, fallback rule, and quality checks.
- `references/README.md`: short index of available reference files.
- `references/*.md`: detailed topic-specific material, one topic per file.
- `scripts/*.sh`: modular shell scripts for deterministic operations (executed via bash, code never enters context).

## Quality Checks

- The `description` says both what the skill does and when to use it.
- `SKILL.md` is short enough to load comfortably and does not inline all detailed reference content.
- Each reference has one obvious purpose and is linked directly from `SKILL.md`.
- The agent can decide which single reference to open for a specific task.
- Missing local coverage has a clear official-docs fallback.
- (If using scripts) Each script in `scripts/` has one responsibility, accepts parameters, and produces structured output.
- (If using scripts) All scripts are documented in a reference file with usage, output format, and platform notes.
