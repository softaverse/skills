# Push to the Scheduler App from a shell script — source this file or paste the function.
#
# Inside a scheduled job the scheduler injects NOTIFY_URL / NOTIFY_TOKEN / NOTIFY_TOPIC.
# Anywhere else, set PUSH_URL / PUSH_TOKEN in the environment (never hard-code them).
#
# Usage: notify "body" ["title"] [low|default|high]
# Note: plain-text endpoint; keep the title free of newlines.

notify() {
  curl -fsS -o /dev/null --max-time 10 \
    -H "Authorization: Bearer ${NOTIFY_TOKEN:-$PUSH_TOKEN}" \
    -H "Title: ${2:-}" -H "Priority: ${3:-default}" \
    --data-binary "$1" \
    "${NOTIFY_URL:-${PUSH_URL%/}}/t/${NOTIFY_TOPIC:-default}"
}
