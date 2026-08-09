# Rewrite Checklist

- Identify the real user task the skill should solve.
- Remove duplicate explanations from `SKILL.md`.
- Keep the body short and action-oriented.
- Move detailed examples into `references/`.
- Move reusable operations into `scripts/` (for deterministic, parameterized tasks).
- Split references by topic, not by file size alone.
- Keep references one level deep from `SKILL.md`.
- Each script should have one responsibility and accept parameters.
- Document all scripts in `references/scripts.md` with usage and output format.
- Add a fallback rule for missing usage.
- Verify the skill no longer shows every reference at once.
- Test all scripts locally on macOS and Linux before deploying.
