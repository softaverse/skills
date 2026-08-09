# Section Guide

## Frequency across high-star projects

Observed across projects like `obra/superpowers`, `shadcn/ui`, and Next.js.

| Section | Frequency | Rule |
| --- | --- | --- |
| Project name | ✅ Always | Required |
| One-line description | ✅ Always | Required |
| Demo / Screenshot | ✅ Common | Include if the project has a UI |
| Features | ✅ Common | Recommended |
| Installation / Quick Start | ✅ Always | Required |
| Usage | ✅ Common | Recommended |
| Documentation | ✅ Common | Required for mid/large projects — link to `docs/` |
| Contributing | ✅ Common | Recommended for open source |
| License | ✅ Always | Required for open source |
| Tech Stack | △ Sometimes | Optional |
| Architecture | △ Sometimes | Prefer `docs/architecture.md` |
| Project Structure | △ Sometimes | Prefer `docs/` |
| Environment Variables | △ Sometimes | Only if setup needs them |
| API | △ Sometimes | Prefer `docs/api.md` |
| Deployment | △ Sometimes | Prefer `docs/deployment.md` |
| Troubleshooting | △ Sometimes | Prefer `docs/troubleshooting.md` |
| Roadmap | △ Sometimes | Project-dependent |

The pattern: **shadcn/ui** keeps the README to product intro → Documentation → Contributing → License, pushing all usage detail to a docs site. **superpowers** keeps Quickstart, How it works, Installation, Contributing, and spreads detail across `docs/` and per-skill `SKILL.md` files.

## What goes in each section

### Overview
What it is, what problem it solves, who it's for. Concrete over aspirational — "converts PNG/JPG to WebP and rewrites source references" beats "a powerful image toolkit". 2–4 sentences. A "How it works" paragraph or a small diagram can live here if it's genuinely short.

### Features
3–6 bullets, each one capability in one line. Not a changelog, not a roadmap, not implementation detail. If you need more than 6, the extras belong in docs.

### Demo
Live URL, GIF, screenshot, or video — in that order of preference. Omit the section entirely for libraries and CLIs with no visual output (a terminal GIF still counts as visual).

### Getting Started
The one section that must be complete and correct. Four subsections:

- **Prerequisites** — runtimes, versions, external services, accounts
- **Installation** — clone/install commands, verbatim
- **Environment Variables** — required keys and where to get them; table form if more than two
- **Development** — the command that starts it, plus the URL/output to expect

Test it against a clean clone mentally: could someone with none of your local state follow this?

### Usage
One concrete example of real use, not an API dump. Show input and output. Multiple commands are fine if the project is a CLI; deep option references go to docs.

### Documentation
A link list into `docs/` or a documentation site. This is the hand-off point that keeps the README short — it exists precisely so Architecture/API/Database/Deployment don't get inlined.

### Contributing
Short. Development setup pointer, PR process, code style/commit convention. Link `CONTRIBUTING.md` if it exists rather than duplicating it.

### License
One line linking `LICENSE`.
