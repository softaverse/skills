---
name: obsidian-excalidraw
description: Turn requirements, processes, system architecture, data models, interactions, state changes, plans or any structured idea into a hand-drawn Excalidraw diagram inside Obsidian (.excalidraw.md) — flowcharts, swimlanes, layered architecture, sequence diagrams, state machines, ER diagrams, trees/mind maps, timelines, tables — with automatic layout, a real Excalidraw render to check the result, and safe edits that preserve whatever the user drew themselves. Use it whenever the user wants something visualised in Obsidian/Excalidraw, wants a new .excalidraw.md drawing, or wants an existing Excalidraw drawing extended, corrected or restyled — including casual asks like「畫成圖」「畫到 excalidraw」「把這個流程／架構畫出來」「補一張圖」「圖上改成…」. Not for Mermaid code blocks in plain markdown notes (use draw-mermaid-diagrams-for-obsidian for that).
---

# Obsidian Excalidraw

Turn what the user describes into a clear diagram in an Obsidian Excalidraw file. You decide **what** to
draw (the structure); bundled scripts handle **how** (layout, bindings, file format, safe write-back).
Don't hand-edit the compressed JSON — one wrong binding or a stale write silently corrupts the user's drawing.

Scripts: `<skill-dir>/scripts/` (Node; `<skill-dir>` = the folder holding this SKILL.md). First run only:
`cd <skill-dir> && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install`.
Keep work files (spec, candidate, preview PNG) in your scratchpad, never inside the vault — Obsidian would index them.

## 1. Understand before drawing

Read the request (and any linked notes/code) and extract:
- **things** — actors, systems, steps, entities, states, milestones (become nodes)
- **relationships** — sequence, calls, data flow, ownership, transitions (become edges, with labels where the
  relationship isn't obvious: conditions 是/否, protocols, amounts, cardinality)
- **groupings** — who does a step (lanes), which tier a component is in (layers), bounded contexts (groups)
- **the question the diagram answers** — "what happens when X fails?", "who talks to whom?", "what are the
  options?" — this decides the diagram type and what to leave out.

Then pick the type — `references/diagram-types.md` has the decision table and conventions for each:

| The content is… | Draw a |
|---|---|
| steps with decisions/loops | `flow` (flowchart) |
| steps split across roles or systems | `swimlane` |
| components by tier / deployment | `layers` (or `flow` with `groups` for free-form) |
| time-ordered calls between parties | `sequence` |
| statuses and transitions | `state` |
| entities and relations | `er` |
| hierarchy / breakdown | `tree` / `mindmap` |
| dates, phases, roadmap | `timeline` |
| numbers, comparisons, options | `table` |

Several views of one topic (e.g. architecture + the main sequence + a numeric example) are often clearer than
one crowded diagram — put each in its own frame. If a key fact is genuinely missing (who approves? sync or
async?), ask, or draw it with a `warning` note instead of inventing it. Keep node text short (≤ ~3 lines);
details go in a `note` box.

## 2. Workflow

1. **Inspect** (existing file) — `node scripts/inspect.js "<file>" --texts` (`--grep` / `--region y0,y1` for
   big drawings). Note the `hash`, free space, frames, and the drawing's own conventions (colors, fonts).
   If it reports **changes since last write**, those are the user's own edits: keep them, follow their lead
   (e.g. they renamed frames → name new ones the same way), never re-create what they deleted, and mention it.
   New file: skip this; the spec gets `"create": true`.

2. **Write a spec** (JSON, in the scratchpad) — full format in `references/spec-format.md`. Usually one
   `diagram` item per view, with nodes/edges; positions are computed for you:
   ```json
   { "expectHash": "<hash>",            // or "create": true for a new file
     "origin": "below",                  // existing file: start under current content
     "frame": { "name": "登入流程" },     // one frame per view; its name is the title
     "add": [
       { "diagram": "flow", "direction": "TB",
         "nodes": [ {"id":"s","text":"開始","style":"start"},
                    {"id":"chk","text":"帳密正確？","style":"decision"},
                    {"id":"ok","text":"登入成功","style":"success"} ],
         "edges": [ {"from":"s","to":"chk"}, {"from":"chk","to":"ok","label":"是"} ] },
       { "text": "說明\n• 連續失敗 5 次鎖定 15 分鐘", "x": 0, "y": 700, "w": 600, "h": 80, "style": "note" } ] }
   ```
   Use semantic styles (`process decision start end actor system service external datastore queue ui entity
   state milestone note warning success …`, see `references/style-guide.md`) — but if the drawing already has
   its own color scheme, match it. Manual boxes/arrows/tables, `edit`, `delete` and `shift` are there for
   annotations and changes to existing content.

3. **Apply** to a candidate copy (the real file is untouched):
   `node scripts/apply.js "<file>" spec.json --out <scratch>/cand.excalidraw.md`
   Fix every `OVERFLOW` / `OVERLAP` warning and re-apply. Text queries that match 0 or several elements stop
   with the candidates listed — narrow them with `within` or a longer string.

4. **Preview** with Excalidraw's own renderer and look at it:
   `node scripts/preview.js <scratch>/cand.excalidraw.md --out <scratch>/prev.png --frame "<frame name>"`
   (or `--changes <cand>.changes.json`, `--region x,y,w,h`, `--all`). Check: reads left→right / top→bottom,
   no crossing or overlapping arrows where avoidable, labels legible, nothing clipped, numbers add up, fits the
   existing content. Iterate: change `direction`, reorder nodes, split a crowded view, `edgeRoute: "orthogonal"`,
   adjust `nodesep`/`ranksep`. Two or three rounds is normal.

5. **Commit** — `node scripts/commit.js <scratch>/cand.excalidraw.md` re-checks the hash (or that a new file
   still doesn't exist), backs up, writes, verifies, snapshots. **REFUSED** means the user edited the file
   meanwhile: go back to step 1 on the new content; don't force it.

6. **Report**: what you drew and why that diagram type, assumptions or open questions (also visible as notes
   in the drawing when they matter), anything of the user's you preserved, and the `restore:` command.

## 3. Things that go wrong

- **Crowded diagram** → split into several frames, or move detail into notes. More than ~15 nodes in one
  flow is usually too many.
- **Back-edges (loops) overlap forward edges** in `flow` → give them a label, try `"edgeRoute": "orthogonal"`,
  or the other `direction`.
- **Same text in several places** → `"within": {"y": [y0, y1]}` on the query; `inspect.js --grep` shows all matches.
- **Growing a section pushes into the next** → `shift` everything below first, then add.
- **Moving/resizing a box** via `edit` re-attaches its arrows automatically; a raw script must call `Scene.reroute`.
- **Something the spec can't express** → small Node script on `scripts/lib.js` (see
  `references/element-schema.md`), writing a candidate + `.changes.json`, then preview and commit as usual.
- **Preview can't start** → it uses installed Google Chrome; else `npx playwright install chromium` in the skill folder.

Backups: `~/.cache/obsidian-excalidraw/backups/` (each commit prints its `restore:` command).
