---
name: youtube-production
description: >
  Run the production workflow for a YouTube episode built with hf-studio (HyperFrames)
  animations — Stage A plans it (brief → outline → line-numbered script → storyboard that
  reuses the channel's existing animations), Stage B measures the user's edited voice track,
  retimes the storyboard and builds the animations, Stage C prepares the final edit for DaVinci Resolve. Use when the user
  wants to plan, script, or storyboard a YouTube video, says an episode is recorded or
  edited, or asks to continue an episode (EP<n>). Not for building a single animation
  (use hf-studio / hyperframes directly) or editing a finished video.
---

# YouTube Production

One episode, three stages. Each stage ends with a hard stop: **the user must say ok
before the next stage starts.** An ok unlocks only the next step, never everything after it.

| Stage | Input from the user | Output | Reference |
|---|---|---|---|
| **A — Plan** | topic, audience, core point, what is built, the result | outline, script, storyboard, animation & asset lists | `references/stage-a-planning.md` |
| **B — Retime & animate** | the voice track the user already edited (fillers, pauses, retakes cut) + screen recordings | transcript, storyboard timing measured from the voice, then animations in hf-studio | not written yet |
| **C — Assemble** | the rendered animations (the storyboard timing is final) | DaVinci timeline, captions, chapters, upload package | not written yet |

Stages B and C are not available yet: after Stage A, stop and tell the user so.

## Where things live

Everything for an episode lives in hf-studio, next to the animations it will produce:

```
<hf-studio>/compositions/
  DESIGN.md                ← channel style, shared by every episode
  EP<n>-<slug>/
    brief.md  outline.md  script.md
    storyboard.json        ← single source of truth; never hand-edit the derived lists
    animations.md  assets.md   ← generated from storyboard.json by scripts/storyboard.py
    DESIGN.md              ← only if this episode deviates from the channel style
```

`<hf-studio>` defaults to `~/Workspace/hyperframes/hf-studio`; the scripts accept
`--studio <path>` or `HF_STUDIO`. If it isn't there, ask once.

hf-studio's own `CLAUDE.md` governs how animations are built (its three gates, the
composition contract, render-safe rules). Never restate or override it here — when a stage
touches compositions, read that file.

## Which stage are we in

Infer it from the episode folder before asking:

| Folder state | Stage |
|---|---|
| no folder, or only `brief.md` / `outline.md` | A |
| `storyboard.json` exists, no voice track given | A is done — confirm, then wait for the edited voice |
| user hands over the edited voice track | B |
| `storyboard.json` has measured `timing.dur` and the animations are rendered | C |

Do not downgrade: if the user arrives with a finished script, convert it (A3, no rewording)
and go straight to the storyboard.

## Rules that hold in every stage

- The animation library is the point. Prefer kit components (`compositions/kit/`: generic,
  length set by the storyboard, themeable), then the channel's own compositions, then library
  ones, and any of them over new work — every reuse keeps episodes looking alike and saves a
  build. A piece that will recur is planned as a new kit component. Explain every `new`.
- Footage first: about 60–70% of the running time is the real demo / screen, 20–30%
  templated graphics, 5–10% custom animation (`storyboard.py check` measures it).
- `storyboard.json` is the only place a decision is recorded. Edit it, then regenerate
  the lists; never edit `animations.md` / `assets.md` by hand.
- Segment and line ids are permanent once Stage B starts (renders and timelines are named
  after them). Add new ids instead of renumbering.
- The storyboard owns time: Stage A estimates each segment's length, Stage B replaces it with
  the measured one, and animations follow it — never the other way round.
- Delivery is 1920×1080 at 60 fps. hf-studio compositions are 1280×720; they are rendered
  at 4K (exact 3×) and scaled down in DaVinci.
- Write documents in the user's language; keep ids, JSON keys, and file names in English.

## References

- `references/stage-a-planning.md` — Stage A workflow, checkpoints, writing and storyboarding rules
- `references/storyboard-schema.md` — `storyboard.json` fields and validation rules
- `references/scripts.md` — usage and output of every script in `scripts/`
