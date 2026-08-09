# README Template

## Full template (8 sections)

````markdown
# Project Name

> One sentence describing the project.

[![npm version](https://img.shields.io/npm/v/PACKAGE.svg)](https://www.npmjs.com/package/PACKAGE)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

What this project is, what problem it solves, and who it's for. 2–4 sentences.

## Features

- Core capability 1
- Core capability 2
- Core capability 3

## Demo

- Live demo: https://example.com
- ![Screenshot](docs/screenshot.png)

## Getting Started

### Prerequisites

- Node.js 18 or newer
- PostgreSQL 15 (or: a Supabase project)

### Installation

```bash
git clone https://github.com/owner/repo.git
cd repo
npm install
```

### Environment Variables

Copy `.env.example` to `.env` and fill in:

| Variable | Description | Required |
| --- | --- | --- |
| `DATABASE_URL` | Postgres connection string | Yes |
| `OPENAI_API_KEY` | Model provider key | Yes |

### Development

```bash
npm run dev
```

Open http://localhost:3000.

## Usage

The shortest path to real output — one concrete example, not an exhaustive tour.

```bash
npm run generate -- --input ./sample.md
```

## Documentation

- [Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Database](docs/database.md)
- [Deployment](docs/deployment.md)
- [Troubleshooting](docs/troubleshooting.md)

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the development setup and PR process.

## License

[MIT](LICENSE)
````

## Minimum viable template

For small, internal, or early-stage projects:

````markdown
# Project Name

> One sentence describing the project.

## Overview

## Features

## Getting Started

## Usage

## License
````

## Conventions

- **Title + one-liner**: the blockquote line under the H1 is the elevator pitch; keep it under ~15 words.
- **Badges**: max 3–4, directly under the title. Version, downloads, license, CI. Skip if not published.
- **Demo**: only if there's something visual. A GIF beats a screenshot; a live URL beats both. Store media in `docs/`.
- **Code blocks**: always language-tagged (` ```bash `, ` ```ts `). Every command must be runnable as written.
- **Env vars**: a table if there are more than two; otherwise point at `.env.example`.
- **Tables** for anything enumerable (env vars, CLI commands, supported targets) — they scan faster than bullets.
