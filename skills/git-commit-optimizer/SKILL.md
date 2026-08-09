---
name: git-commit-optimizer
description: >
  Optimize git commits for clarity, atomicity, and conventional commit standards.
  Trigger this skill whenever the user wants to: write or improve a commit message,
  stage and commit changes, split a large diff into logical commits, squash or reword
  commits, review commit history for quality, or set up commit hooks/linting.
  Also trigger when the user says "commit my changes", "help me write a commit",
  "clean up my commits", "interactive rebase", or asks about commitizen, husky,
  conventional commits, or semantic versioning. Use this skill even if the request
  seems simple — a single commit message is still worth optimizing.
---

# Git Commit Optimizer

A skill for writing great commits: atomic, descriptive, and following Conventional Commits.

---

## Core Principles

1. **Atomic commits** — one logical change per commit; never bundle unrelated changes.
2. **Conventional Commits** — `<type>(<scope>): <subject>` format (see below).
3. **Imperative mood** — "Add feature" not "Added feature" or "Adding feature".
4. **72-char subject line** — hard limit; detail goes in the body.
5. **Why, not what** — the diff shows *what* changed; the message explains *why*.

---

## Conventional Commit Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Types

| Type       | When to use                                              |
|------------|----------------------------------------------------------|
| `feat`     | New feature visible to users                             |
| `fix`      | Bug fix                                                  |
| `refactor` | Code restructure, no behavior change                     |
| `perf`     | Performance improvement                                  |
| `test`     | Adding or updating tests                                 |
| `docs`     | Documentation only                                       |
| `style`    | Formatting, whitespace (no logic change)                 |
| `chore`    | Build scripts, deps, config, tooling                     |
| `ci`       | CI/CD pipeline changes                                   |
| `revert`   | Reverting a previous commit                              |
| `build`    | Changes that affect the build system or external deps    |

### Breaking Changes
Append `!` after type/scope **or** add `BREAKING CHANGE:` footer:
```
feat(api)!: rename endpoint /users to /accounts

BREAKING CHANGE: clients must update their base URL.
```

### Scope
Lowercase noun describing the changed area: `auth`, `ui`, `db`, `parser`, `cli`, etc.
Omit scope when the change is truly cross-cutting.

---

## Workflow

### 1. Inspect the Working Tree

```bash
git status
git diff --stat          # overview of changed files
git diff                 # full diff (unstaged)
git diff --cached        # staged diff
```

Read the diff carefully before writing anything. Understand *what* changed and *why*.

### 2. Group Changes into Logical Units

If `git diff --stat` shows many unrelated files, split into multiple commits:

```bash
# Stage only related files
git add src/auth/login.ts src/auth/logout.ts
git commit -m "feat(auth): add session expiry logic"

git add tests/auth.test.ts
git commit -m "test(auth): cover session expiry edge cases"
```

Use `git add -p` (patch mode) to stage individual hunks within a file:
```bash
git add -p src/api.ts   # interactively pick hunks
```

### 3. Write the Commit Message

**Template:**
```
<type>(<scope>): <imperative subject, max 72 chars>

Why this change is needed (1-3 sentences). What problem does it solve?
What would happen without it?

Refs: #<issue-number>
Co-authored-by: Name <email>    (if pair programming)
```

**Good examples:**
```
fix(auth): prevent token refresh race condition

Concurrent requests could each trigger a refresh, invalidating the
first new token before it was used. Added a mutex so only one refresh
runs at a time.

Closes #412
```

```
feat(dashboard): add date range filter to analytics view

Users need to compare metrics across custom periods, not just fixed
30/90-day windows.
```

```
chore(deps): upgrade axios from 1.4 to 1.7

Fixes a SSRF vulnerability (CVE-2024-XXXX). No API changes required.
```

**Bad examples (and why):**
```
fix bug              ← no type, no scope, not descriptive
updated stuff        ← vague, past tense
WIP                  ← never commit WIP to shared branches
feat: Added the new login page and also fixed the signup bug and updated deps
                     ← three unrelated changes; split this
```

### 4. Commit

```bash
git commit -m "feat(scope): subject" -m "Body paragraph here."

# Or open editor for multi-line messages:
git commit
```

For a series of commits, check the log afterwards:
```bash
git log --oneline -10
```

---

## Fixing Commits

### Amend the last commit (not yet pushed)
```bash
git commit --amend                  # opens editor
git commit --amend -m "new message" # inline
git commit --amend --no-edit        # keep message, update files
```

### Interactive rebase (last N commits)
```bash
git rebase -i HEAD~N
```
Commands in the editor:
- `reword` (r) — edit message only
- `squash` (s) — merge into previous commit, combine messages
- `fixup` (f) — merge into previous, discard this message
- `edit` (e) — pause to amend files/message
- `drop` (d) — delete commit

**Safety rule**: only rebase commits that haven't been pushed to a shared branch.

### Squash a feature branch before merge
```bash
# From the feature branch:
git rebase -i main
# Mark all but the first as `squash` or `fixup`
```

---

## Commit Quality Checklist

Before committing, verify:

- [ ] `git diff --cached` reviewed — no debug logs, commented-out code, or `TODO: remove`
- [ ] Subject ≤ 72 characters
- [ ] Type is correct (not everything is `fix` or `chore`)
- [ ] Scope is meaningful and consistent with repo conventions
- [ ] Imperative mood in subject
- [ ] Body explains *why* (if non-trivial)
- [ ] Issue/ticket reference included (if applicable)
- [ ] No unrelated files staged
- [ ] Tests pass (`npm test`, `pytest`, etc.) before committing

---

## Automating Commit Quality

### commitlint + husky (Node.js projects)

```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional husky
npx husky init
echo "npx --no -- commitlint --edit \$1" > .husky/commit-msg
```

`commitlint.config.js`:
```js
module.exports = { extends: ['@commitlint/config-conventional'] };
```

### commitizen (interactive commit prompt)

```bash
npm install --save-dev commitizen cz-conventional-changelog
npx commitizen init cz-conventional-changelog --save-dev --save-exact
# Then use: git cz  (instead of git commit)
```

### pre-commit hooks (Python / polyglot)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.2.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
```

```bash
pip install pre-commit
pre-commit install --hook-type commit-msg
```

---

## Generating Commit Messages from Diff

When asked to generate a commit message, follow this process:

1. Run `git diff --cached` (or `git diff` if nothing staged).
2. Identify the primary intent of the change.
3. Choose the correct type and scope.
4. Draft subject in imperative mood.
5. Add body if the change is non-trivial or the *why* isn't obvious.
6. Output the full commit message in a code block so the user can copy or pipe it.

```bash
# User can apply directly:
git commit -F- <<'EOF'
feat(parser): support multiline string literals

The old parser would throw on strings containing newlines. Updated the
tokenizer to handle escaped newlines and raw string delimiters.

Closes #88
EOF
```

---

## Reference

- Conventional Commits spec: https://www.conventionalcommits.org
- Angular commit guidelines (origin of the convention): https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit
- `git rebase` docs: `man git-rebase`