# Jobs API and the scheduler runtime

All calls need `Authorization: Bearer $PUSH_TOKEN` against `$PUSH_URL`.

## Endpoints

| Method | Path | Notes |
|---|---|---|
| GET | `/api/scripts` | Runnable scripts the server can see, as paths relative to the scripts dir (e.g. `stock/main.py`) |
| GET | `/api/jobs` | All jobs |
| POST | `/api/jobs` | Create (`201`) |
| GET / PATCH / DELETE | `/api/jobs/{id}` | PATCH accepts any subset of fields |
| POST | `/api/jobs/{id}/run` | Run now |
| GET | `/api/jobs/{id}/runs` | Run history |
| GET | `/api/runs/{id}` | One run: status, duration, exit code, stdout, stderr |

## Job fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `name` | string 1–80 | required | Must be unique (`409` otherwise) |
| `cron` | string | required | 5 fields: `min hour dom mon dow`; server timezone (default `Asia/Taipei`) |
| `script` | string | | Path relative to the scripts dir, as listed by `/api/scripts` |
| `args` | string | | Shell-split and appended to the script |
| `command` | string | | Arbitrary shell; only when the server has `ALLOW_COMMANDS=true` — prefer `script` |
| `timeout` | int seconds 1–86400 | `600` | |
| `notify` | `on_output` \| `always` \| `on_failure` \| `never` | `on_output` | See below |
| `topic` | string ≤ 80 | job name | Becomes `NOTIFY_TOPIC` for the script |
| `priority` | `low` \| `default` \| `high` | `default` | Priority of the auto-pushed stdout |
| `enabled` | bool | `true` | |

Exactly one of `script` / `command`. `422` means a bad cron, a missing script, or both/neither set — read `detail`.

Cron day-of-week: `0` and `7` are Sunday, `1-5` is Mon–Fri (the server converts to names, so standard cron meaning holds). Examples: `0 8 * * *` daily 08:00, `30 13 * * 1-5` weekdays 13:30, `*/15 * * * *` every 15 min.

## Notify mode vs. calling the API yourself

| `notify` | Scheduler pushes stdout | Script also calls the push API? |
|---|---|---|
| `on_output` | when stdout is non-empty | no — would duplicate |
| `always` | every run | no — would duplicate |
| `on_failure` | only on failure / timeout | **yes, use this** |
| `never` | never (not even failures) | possible, but failures go silent |

Except `never`, a non-zero exit or timeout always sends a `high` message titled `❌ <job name> 失敗`. So scripts should exit non-zero on real errors instead of swallowing them.

## Runtime inside the container

- Python 3.12 and Node 22; timezone `Asia/Taipei`, so `datetime.now()` / `new Date()` are Taiwan time.
- Environment injected per run: `NOTIFY_URL` (internal `http://127.0.0.1:8000`), `NOTIFY_TOKEN`, `NOTIFY_TOPIC`.
- Working directory is the script's folder.
- Interpreter by suffix: `.py` (uses a `.venv`/`venv` in the script's folder or a parent inside the scripts dir, else system python), `.js`/`.mjs`/`.cjs` (node), `.sh` (bash).
- Dependencies must be installed inside the container (see SKILL.md, scenario A). The listing skips `node_modules`, `.venv`, `venv`, `__pycache__`, `.git`, `data`, and dot-folders; it goes 3 levels deep.
