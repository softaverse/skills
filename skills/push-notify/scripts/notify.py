"""Push to the Scheduler App. Standard library only — copy this function into your script.

Inside a scheduled job the scheduler injects NOTIFY_URL / NOTIFY_TOKEN / NOTIFY_TOPIC.
Anywhere else, set PUSH_URL / PUSH_TOKEN in the environment (never hard-code them).
"""
import json
import os
import urllib.request


def notify(body: str, title: str | None = None, priority: str = "default", topic: str | None = None) -> dict:
    """priority: low (stored, no alert) / default / high (urgent channel)."""
    url = os.environ.get("NOTIFY_URL") or os.environ["PUSH_URL"]
    token = os.environ.get("NOTIFY_TOKEN") or os.environ["PUSH_TOKEN"]
    topic = topic or os.environ.get("NOTIFY_TOPIC") or "default"
    req = urllib.request.Request(
        f"{url.rstrip('/')}/api/messages",
        data=json.dumps({"topic": topic, "body": body, "title": title, "priority": priority}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as res:  # raises HTTPError on 4xx/5xx
        return json.load(res)


if __name__ == "__main__":
    notify("hello from notify.py", title="Python")
