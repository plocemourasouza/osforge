---
name: osforge-canvas
description: >
  Local generative UI for interactive review of plans, specs, and breakdowns in
  the browser, with native structured feedback. DEFAULT CHANNEL for presenting
  any spec or plan: the server is started automatically by a SessionStart
  hook — don't wait for the user to ask. Use when: presenting a plan, spec,
  or breakdown (default), approval checkpoints in STANDARD/COMPLEX triage,
  or the user asks "open in canvas", "show in the browser", "I want to review
  interactively", "I need to approve before implementing", "canvas".
  Keywords: canvas, interactive review, approve plan, spec, structured feedback,
  checkpoint, approve, interactive review, open canvas. Do NOT use for: quick
  text responses that don't require a round-trip; one-shot presentable document
  without feedback collection → use visual-planner; the user explicitly asked
  for "text only" / "in the terminal".
version: 1.1.0
metadata:
  category: "planning"
  position: "interactive-review-layer"
allowed-tools: Read, Write, Bash
---

# OSForge Canvas

Local generative UI, Thesys C1 style. Claude emits a structured JSON artifact,
the Bun server renders the interactive UI in the browser, and feedback returns via file
for Claude's next turn.

## Decision table

| Situation | Tool |
|---|---|
| Quick response / status / question | text in the terminal |
| **Any presentation of a plan, spec, or breakdown** (default — no request needed) | **CANVAS** |
| Standalone presentable document with no feedback round-trip (explicit request) | `visual-planner` HTML |
| User asked for "text only" / "in the terminal" | text in the terminal |

When emitting to the canvas, also include a short summary (5-10 lines) in the terminal —
the canvas is the full document, the terminal is the TL;DR.

## Operational workflow

### 1. Server health check (usually already running)

The server is started automatically by the SessionStart hook
(`hooks/canvas-autostart.sh`) with the **global** data dir `~/.osforge/canvas/`.
Confirm and capture the real data dir:

```bash
curl -sf http://localhost:4242/api/health
# → {"ok":true,...,"dir":"<DATA_DIR>"}  ← ALWAYS use this dir for artifacts/feedback
```

If it returns an error (hook didn't run / bun missing): start it manually in the background:

```bash
bun ~/.claude/canvas/server.ts --dir="$HOME/.osforge/canvas" &
# fallback if not deployed: bun <osforge-repo>/scripts/canvas/server.ts --dir="$HOME/.osforge/canvas" &
```

Default port: `4242`. Override via `CANVAS_PORT=<port>` before the command.
Re-check health after starting.

### 2. Write the artifact

Write `<DATA_DIR>/artifacts/<slug>.json` (DATA_DIR comes from health — global by
default) following the schema in `skills/osforge-canvas/references/schema.md`.

Quick rules:
- `$schema`: `"osforge-canvas/v1"` (literal)
- `id`: unique kebab-case — same value as the file name without `.json`.
  **Prefix with the project slug** (e.g. `myapp-auth-refactor-plan`) — the
  data dir is shared across all projects on the machine
- `revision`: starts at `1`, increments on each overwrite
- `createdAt`: ISO 8601, do not change on revisions
- `blocks`: array of up to 8 types (`heading`, `markdown`, `cards`, `table`,
  `checklist`, `form`, `decision`, `mermaid`) — all with a unique kebab-case `id`
- `accent`: choose by domain (see the table in the "Accent color" section)

**Pseudo-streaming:** for long artifacts, write the file early with initial
blocks and overwrite as it completes. The viewer detects changes via SSE and
reloads without a manual refresh.

### 3. Present to the user

Print the URL and ask for review:

```
Artifact ready. Open it to review:
http://localhost:4242/?a=<slug>

When you're done, submit the feedback in the browser — I'll read it next.
```

### 4. Next turn — read feedback before continuing

**Every time the user sends any message after an active artifact**, read
`<DATA_DIR>/feedback/<slug>.json` before any other action.

Mandatory checks:
- Does the file exist? If not: feedback not yet submitted — notify the user.
- `feedback.revision === artifact.revision`? If lower: feedback is stale (the user
  reviewed a previous version) — notify and reconcile before acting.
- Act on `responses` per block: `checklist` → checked items; `form` → filled
  values; `decision` → action (`approve` / `edit` / `reject`) + comment.

**Requested revisions:** overwrite the same `artifacts/<slug>.json` file,
incrementing `revision`. The viewer reloads via SSE automatically.

## Accent color

| Domain | Accent | Hex |
|---|---|---|
| General engineering, product | `vermillion` (default) | `#D94F30` |
| Data, infra, backend | `teal` | `#2A7B9B` |
| Consumer, UX, front-end | `coral` | `#E06B56` |
| DevTools, CLI, OSS | `forest` | `#2D8B55` |
| Fintech, analytics, BI | `amber` | `#D4A843` |

## Schema reference

`skills/osforge-canvas/references/schema.md` — source of truth for all block
types, required fields, feedback format, and ID rules.

## v2 backlog (deferred)

- Interactive charts (`chart` block type)
- Block-level streaming via SSE (send blocks as they are generated)
- `UserPromptSubmit` hook to automatically inject feedback into the context
- Standalone compiled binary for deploy without Bun installed
