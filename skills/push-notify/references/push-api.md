# Push API

Base URL is `$PUSH_URL`; every call except `/api/health` needs `Authorization: Bearer $PUSH_TOKEN`. UTF-8 throughout.

## Endpoints (same effect — pick whichever is convenient)

### `POST /t/{topic}` — plain text (shell, curl)

| Where | Name | Required | Notes |
|---|---|---|---|
| path | `topic` | ✓ | 1–80 chars |
| body | — | ✓ | Plain text; trimmed; must not be empty. Use `--data-binary` to keep newlines (`-d` strips them). |
| header / query | `Title` / `?title=` | | Title; UTF-8 OK |
| header / query | `Priority` / `?priority=` | | `low` / `default` / `high`; unknown → `default` |

Query params win over headers.

### `POST /api/messages` — JSON (programs)

```json
{ "topic": "stock", "body": "**TSMC** below 1000", "title": "⚠️ Price alert", "priority": "high" }
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `topic` | string | ✓ | 1–80 chars; the app groups messages by topic |
| `body` | string | ✓ | ≥ 1 char, Markdown |
| `title` | string \| null | | Defaults to `topic` |
| `priority` | `low` \| `default` \| `high` | | Invalid value → `422` |

## Priority

| Value | Phone | In app | Use for |
|---|---|---|---|
| `low` | **no notification** | stored | routine logs to read later |
| `default` | normal notification | stored | most cases |
| `high` | urgent channel (loud) | red left bar | errors, alerts, needs action now |

## Responses

- `201` → `{id, topic, title, body, priority, run_id, created_at}` (`created_at` is UTC ISO 8601; `run_id` is null for API calls).
- `401` → missing/wrong token. Check `PUSH_TOKEN`.
- `422` → empty body, topic too long, bad priority, bad JSON. Read `detail`, fix, **do not retry**.
- `5xx` / timeout → retry 1–2 times.

The message is saved before delivery; a phone that is offline does not make the API fail.

## Body formatting

The app renders `body` as Markdown; the phone's notification shade shows raw text (you will see `**`).

- Supported: headings, `**bold**`, `*italic*`, `~~strike~~`, `` `code` ``, fenced code blocks (horizontally scrollable — use for aligned tables), lists, `>` quotes, `---`, links / bare URLs.
- Differences from standard Markdown: a **single newline is a line break**; `_x_` is not italic (`snake_case` is safe); `*` surrounded by spaces is literal (`5 * 3`).
- Not supported: pipe tables, images, HTML. Put tables in a code block.

Length: the app collapses cards over ~6 lines; the phone notification truncates at 1500 chars with `…`. Put the key point in the first line; for long reports push a summary plus a link.

## Other endpoints

| Method | Path | Notes |
|---|---|---|
| GET | `/api/health` | No token; `{"status":"ok"}` |
| GET | `/api/messages?topic=&before_id=&limit=` | Newest first; `limit` 1–200 (default 50); paginate with the last `id` as `before_id` |
| DELETE | `/api/messages/{id}` | `204` |
| GET | `/api/topics` | Topics with message counts |
| GET | `/api/status` | Host disk/memory/load, running jobs, last-24h run stats |

## Rules of thumb

- No rate limit, but every `default`/`high` message alerts the phone. Batch many results into one message, or use `low`.
- Topic names: short words (`stock`, `備份`, `ci`). The app shows one button per topic, so don't invent a new topic per message.
- The token can also create and run jobs on the server — keep it out of code, logs, commits, and command output.
