---
name: disk-audit
description: Audit a macOS disk for reclaimable space — scan caches, dev-tool stores, build artifacts, node_modules, Docker, local AI models, emulator images, and large files, then report a tiered cleanup list (safe / confirm first / personal data) with sizes and commands. Use when the user says the disk is full, is low on storage, asks what can be deleted or cleaned up, or runs /disk-audit. Read-only; never deletes without explicit confirmation.
---

# Disk Audit

Find what is eating disk space on macOS and produce a prioritized, tiered cleanup list. The audit itself is **read-only**.

## Workflow

1. **Scan** — Run the bundled script and save its output to the scratchpad (it can take a few minutes on a large home directory):

   ```bash
   bash <skill-dir>/scripts/disk-audit.sh [project-dir ...] > <scratchpad>/disk-audit.txt 2>&1
   ```

   With no arguments it scans whichever of `~/Workspace ~/Projects ~/code ~/dev ~/src` exist. If the home-directory listing shows other folders holding code, pass them explicitly. Use a 600000 ms timeout.

2. **Drill down** — For any entry over ~1 GB whose contents are not obvious (an app's `Application Support` folder, a project folder, a big `Containers` entry), run one more level of `du -sh <dir>/* | sort -rh | head`. Batch independent drill-downs into one response. Stop once each large item can be classified.

3. **Classify** — Put every significant item into a tier using [references/cleanup-tiers.md](./references/cleanup-tiers.md), which also gives the cleanup command and caveats for each known location.

4. **Report** — Reply in the user's language:
   - Disk status: total, used %, free (use the `/System/Volumes/Data` row)
   - 🟢 **Safe, regenerates automatically** — table: item · size · command
   - 🟡 **Confirm still needed** — table: item · size · note
   - 🔴 **Personal data, user decides** — bullets
   - Estimated reclaimable space for 🟢 alone and for 🟢 plus the biggest 🟡 items
   - A recommended first step, and an offer to run the cleanup

   Sort by size inside each tier and skip items under ~100 MB unless there are many of them.

5. **Clean (only on request)** — Delete nothing until the user explicitly picks items or tiers. Then run the commands, prefer tool-native cleanup (`npm cache clean`, `flutter clean`, `docker system prune`, `ollama rm`) over `rm -rf`, and finish with `df -h /System/Volumes/Data` to report what was freed.

## Rules

- Never delete during the audit, not even items in the 🟢 tier.
- If `~/.Trash`, `~/Library/Mail` or similar show as empty or error, the terminal probably lacks Full Disk Access — say so rather than reporting 0 B.
- `docker system prune -a --volumes` also removes images and volumes of stopped containers; mention this before running it.
- Treat project source, mail stores, photos, documents and cloud-drive folders as 🔴 no matter how large they are.
