// Push to the Scheduler App. Node 18+, no dependencies — copy this function into your script.
//
// Inside a scheduled job the scheduler injects NOTIFY_URL / NOTIFY_TOKEN / NOTIFY_TOPIC.
// Anywhere else, set PUSH_URL / PUSH_TOKEN in the environment (never hard-code them).

export async function notify(body, { title, priority = "default", topic } = {}) {
  const url = (process.env.NOTIFY_URL ?? process.env.PUSH_URL)?.replace(/\/$/, "");
  const token = process.env.NOTIFY_TOKEN ?? process.env.PUSH_TOKEN;
  if (!url || !token) throw new Error("PUSH_URL / PUSH_TOKEN not set");
  const res = await fetch(`${url}/api/messages`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ topic: topic ?? process.env.NOTIFY_TOPIC ?? "default", title, body, priority }),
    signal: AbortSignal.timeout(10_000),
  });
  if (!res.ok) throw new Error(`notify failed: ${res.status} ${await res.text()}`);
  return res.json();
}

if (import.meta.url === `file://${process.argv[1]}`) {
  await notify("hello from notify.mjs", { title: "Node" });
}
