#!/usr/bin/env bash
# Send one push notification to the Scheduler App.
#
#   push.sh "body"                      # topic "default", priority default
#   push.sh -t "Title" -p high -T ci "body"
#   some-command | push.sh -t "Output"  # body from stdin when no body argument
#
# Reads PUSH_URL and PUSH_TOKEN from the environment. Never pass the token as an argument.
set -euo pipefail

usage() { sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }

TITLE="" PRIORITY="default" TOPIC="default"
while getopts "t:p:T:h" opt; do
  case "$opt" in
    t) TITLE="$OPTARG" ;;
    p) PRIORITY="$OPTARG" ;;
    T) TOPIC="$OPTARG" ;;
    h) usage 0 ;;
    *) usage 2 ;;
  esac
done
shift $((OPTIND - 1))

: "${PUSH_URL:?PUSH_URL is not set (e.g. export PUSH_URL=https://push.example.com)}"
: "${PUSH_TOKEN:?PUSH_TOKEN is not set}"

case "$PRIORITY" in low|default|high) ;; *) echo "priority must be low|default|high" >&2; exit 2 ;; esac

if [[ $# -gt 0 ]]; then BODY="$*"; else BODY="$(cat)"; fi
if [[ -z "${BODY//[[:space:]]/}" ]]; then echo "body is empty" >&2; exit 2; fi

# JSON endpoint so title/topic with any characters are safe; python3 only for encoding.
PAYLOAD=$(TOPIC="$TOPIC" TITLE="$TITLE" PRIORITY="$PRIORITY" BODY="$BODY" python3 -c '
import json, os
print(json.dumps({"topic": os.environ["TOPIC"], "body": os.environ["BODY"],
                  "title": os.environ["TITLE"] or None, "priority": os.environ["PRIORITY"]}))')

RESP=$(mktemp)
trap 'rm -f "$RESP"' EXIT

HTTP_CODE=$(curl -sS -o "$RESP" -w '%{http_code}' --max-time 10 \
  -H "Authorization: Bearer $PUSH_TOKEN" -H "Content-Type: application/json" \
  --data-binary "$PAYLOAD" "${PUSH_URL%/}/api/messages") || { echo "network error" >&2; exit 1; }

if [[ "$HTTP_CODE" == "201" ]]; then
  echo "sent (topic=$TOPIC, priority=$PRIORITY)"
else
  echo "push failed: HTTP $HTTP_CODE $(cat "$RESP")" >&2
  exit 1
fi
