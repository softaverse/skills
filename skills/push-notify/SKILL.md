---
name: push-notify
description: Send push notifications to the user's own phone through their self-hosted Scheduler server (Expo/FCM Android app) — create a scheduled script on the server that pushes results, add a notify() call to any other program (local scripts, other servers, GitHub Actions), or send one message right now. Use when the user wants something pushed / notified to their phone — 「推播到手機」「通知我」「排程跑完推給我」「每天早上推…」「股價跌破就通知」「CI 失敗通知我」「notify me when…」— or mentions the Scheduler app, NOTIFY_TOKEN, or PUSH_TOKEN. Not for LINE messages, email, or desktop notifications.
---

# Push Notify

Push messages to the user's phone through their Scheduler server (FastAPI + APScheduler in Docker on EC2, delivered to an Android app). Reply to the user in their language.

## Configuration — always from the local environment

| Variable | Meaning |
|---|---|
| `PUSH_URL` | Server base URL |
| `PUSH_TOKEN` | API token |
| `PUSH_SSH_HOST` | SSH host for the server — only needed for scenario A |

**Never** hard-code the URL or token in files, look the token up on the server, print it, or pass it on a command line where it would be echoed. Check presence without revealing values:

```bash
for v in PUSH_URL PUSH_TOKEN; do [ -n "${(P)v}" ] && echo "$v: set" || echo "$v: MISSING"; done   # zsh
```

If either is missing, stop and tell the user to add them to `~/.zshrc` (`export PUSH_URL=…`, `export PUSH_TOKEN=…`) and open a new shell — Claude Code's Bash tool reads the shell profile on each call. Then verify with `curl -fsS "$PUSH_URL/api/health"`.

## Pick the scenario

| Scenario | Signal | Go to |
|---|---|---|
| **A. New scheduled push** | "every day / every hour / when X happens, push to me" — runs on the server | [A](#a-new-scheduled-push) |
| **B. Push from another program** | existing local script, another server, CI, IoT | [B](#b-push-from-another-program) |
| **C. Push one message now** | "push me a test", "notify me when this long task finishes" | [C](#c-push-one-message-now) |

Read [references/push-api.md](references/push-api.md) for fields, priorities, errors, and Markdown limits. For scenario A also read [references/jobs-api.md](references/jobs-api.md).

## Decide: print, or call the API?

- **Just send the result to the phone** → the script `print()`s / `console.log()`s; job `notify: on_output`. No API code needed.
- **Push only when a condition holds, send several messages, or set title/priority per message** → copy `notify()` from `scripts/`; job `notify: on_failure` (otherwise stdout is pushed again).

Priority: `low` = stored, no alert (routine logs); `default` = most things; `high` = needs action now. Don't make routine output `high`.

## A. New scheduled push

1. **Clarify** only what you can't default: what to check, when (→ cron), and the condition for pushing. Defaults: timeout 600 s, topic = short English or Chinese word, priority `default`.
2. **Write the script** locally in the scratchpad under `<name>/` (`main.py` or `index.mjs`). Prefer the standard library; if you need packages, add `requirements.txt` or `package.json`. Exit non-zero on real errors so the scheduler sends the `❌` failure push. Run it locally once if it doesn't need the server environment.
3. **Show the user** the script, the cron (with plain-language meaning), notify mode, topic, and priority. Wait for approval before touching the server.
4. **Upload** (needs `PUSH_SSH_HOST`; if missing, ask the user for it). Scripts live in `~/scripts` on the host, mounted at `/scripts` in container `scheduler`; compose project is `~/scheduler-server/server`. Never overwrite an existing folder without checking it first (`ssh "$PUSH_SSH_HOST" ls ~/scripts`).

   ```bash
   rsync -av --exclude .venv --exclude node_modules <scratchpad>/<name>/ "$PUSH_SSH_HOST":scripts/<name>/
   # Python packages
   ssh "$PUSH_SSH_HOST" 'cd ~/scheduler-server/server && docker compose exec -w /scripts/<name> scheduler sh -c "uv venv .venv && uv pip install -p .venv -r requirements.txt"'
   # Node packages
   ssh "$PUSH_SSH_HOST" 'cd ~/scheduler-server/server && docker compose exec -w /scripts/<name> scheduler npm install'
   ```

5. **Confirm the server sees it**: `GET /api/scripts` should list `<name>/main.py`.
6. **Create the job** with a JSON body (write it to a scratchpad file to avoid quoting problems):

   ```bash
   curl -fsS -H "Authorization: Bearer $PUSH_TOKEN" -H "Content-Type: application/json" \
     --data-binary @<scratchpad>/job.json "$PUSH_URL/api/jobs"
   ```

   `{"name":"台股收盤","cron":"30 13 * * 1-5","script":"stock/main.py","notify":"on_output","topic":"stock"}`
   `409` = name taken (offer to PATCH the existing job instead); `422` = read `detail`.
7. **Test run**: `POST /api/jobs/{id}/run`, then poll `GET /api/jobs/{id}/runs` until it finishes, and show status, exit code, and stdout/stderr. Ask the user whether the push arrived.
8. **Report**: job name, schedule in plain words, next run time, and how to change it (app → 排程, or PATCH).

To change an existing job, `GET /api/jobs` to find it, then `PATCH /api/jobs/{id}` with only the changed fields. To change its script, re-upload and run once.

## B. Push from another program

1. Copy the matching client from `scripts/` into the program — [notify.py](scripts/notify.py) (stdlib), [notify.mjs](scripts/notify.mjs) (Node 18+), [notify.sh](scripts/notify.sh) (curl). They read `NOTIFY_*` inside scheduled jobs and fall back to `PUSH_URL` / `PUSH_TOKEN` elsewhere.
2. Put the URL and token in that environment's secrets, never in code. Tell the user exactly where to set them (e.g. GitHub → Settings → Secrets → `PUSH_URL`, `PUSH_TOKEN`).
3. Don't let a failed push crash the main program unless the user wants that: wrap the call and log the error.
4. GitHub Actions step:

   ```yaml
   - name: Notify
     if: always()
     env:
       PUSH_URL: ${{ secrets.PUSH_URL }}
       PUSH_TOKEN: ${{ secrets.PUSH_TOKEN }}
     run: |
       curl -fsS -H "Authorization: Bearer $PUSH_TOKEN" \
         -H "Title: ${{ github.repository }} ${{ job.status }}" \
         -d "${{ github.workflow }} #${{ github.run_number }}" \
         "$PUSH_URL/t/ci"
   ```

## C. Push one message now

```bash
bash <skill-dir>/scripts/push.sh -t "標題" [-p low|default|high] [-T topic] "內文"
long-command 2>&1 | tail -20 | bash <skill-dir>/scripts/push.sh -t "Build finished" -T build
```

Topic defaults to `default`. For "notify me when X finishes", chain it after the task: `task; bash push.sh -t "Done (exit $?)" "…"`.

## Checklist

- [ ] `PUSH_URL` / `PUSH_TOKEN` read from env; nothing secret written to files or output
- [ ] print vs. API chosen, and the notify mode matches (no double pushes)
- [ ] Priority fits; first line of the body carries the point (the phone truncates at 1500 chars and shows raw Markdown)
- [ ] Script exits non-zero on real errors
- [ ] Scenario A: user approved before upload; test run done and its result shown
