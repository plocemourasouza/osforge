---
name: system-diagrams
description: "Verified technical diagrams (leading word: **receipt**) — architecture, workflow, sequence, data-flow, lifecycle — delivered as self-contained interactive artifacts through Archify's validate → deliver loop. Use when: defining the structure of a new project, module, or integration; a spec, ADR, design doc, or runbook needs its architecture, request path, data pipeline, or state machine made explicit; comparing an architecture before and after a change; the user asks to visualize, map, or diagram a system. Keywords: architecture diagram, system map, data flow, sequence diagram, state machine, lifecycle, workflow diagram, ADR diagram, visualize the system, Archify. Do NOT use for: presenting a whole plan or spec as a narrative page (visual-planner), interactive approval of a plan (osforge-canvas), a 3-node sketch inside a chat reply (inline Mermaid is fine), UI mockups or screens (ui-design-intelligence)."
model: sonnet
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
metadata:
  version: "1.0.0"
  inspired_by: tt-a1i/archify (SKILL.md)
  source: tt-a1i/archify
  license_note: "Discipline layer over the Archify skill (MIT); the engine is installed pinned by deploy.sh, not vendored"
  requires_binary: node >= 18 + ~/.claude/skills/archify (deploy.sh --with-archify)
---

# System Diagrams (receipt)

**Iron Law:** `A DIAGRAM EXISTS ONLY WHEN deliver RETURNS 9/9 CHECKS AND A SHA-256 — A DRAWING WITHOUT A RECEIPT IS AN OPINION`

OSForge already demands facts before an irreversible action (GateGuard) and evidence before "done"
(`verification-before-completion`). This skill applies the same rule to the picture of a system:
the diagram is authored as typed JSON, validated by a deterministic engine, and delivered with a
**receipt**. Mermaid in a Markdown file is a sketch; a `deliver` receipt is a fact.

The engine is **Archify** (`~/.claude/skills/archify`, installed pinned by `deploy.sh`). This skill
decides *when* a diagram is due, *which type*, *where* it lives, and *what counts as accepted*.
Authoring details (schemas, geometry repairs, brands, viewer features) belong to
`~/.claude/skills/archify/SKILL.md` — read it when you author; do not duplicate it here.

## When NOT to use

- The whole plan/spec needs a narrative, scroll-through page → `visual-planner` (it may embed or
  link the HTML this skill delivers; it does not redraw it)
- The user must approve a plan interactively with structured feedback → `osforge-canvas`
- A tiny illustration inside a chat answer (≤ 4 nodes, no artifact) → inline Mermaid, say it is
  unverified
- Screens, components, UI states → `frontend-design`, `ui-design-intelligence`
- The engine is missing (`doctor` fails) and the user cannot run `./deploy.sh --with-archify` →
  fallback in step 5

## Process

### 1. Decide whether a diagram is due — and which type

A diagram is **due** (not optional) at these points of the OSForge flow:

| Moment | Type(s) | Lives at |
|---|---|---|
| `/spec-design` (Phase 2) | `architecture` for components; `sequence` or `dataflow` for the feature's main path | `.specs/features/<feature>/diagrams/` |
| ADR (`architecture`, `arch-builder`) with a topology change | `architecture`; `compare` base vs head when the ADR replaces something | `.specs/architecture/` next to the ADR |
| Technical Design Doc | `architecture` + `sequence` for the critical request | wherever the TDD lives, `diagrams/` beside it |
| Runbook / CI / deployment procedure | `workflow`; `lifecycle` for status transitions | beside the runbook |
| New project or module bootstrap ("define the structure") | `architecture` (8–12 primary nodes, one main path) | `.specs/architecture/system-overview.*` |

Pick the type from the question the reader must answer: *what exists and how it connects* →
`architecture`; *who calls whom, in what order* → `sequence`; *where data goes and who consumes
it* → `dataflow`; *which steps, gates, and lanes* → `workflow`; *which states and transitions* →
`lifecycle`. When ambiguous, run
`node ~/.claude/skills/archify/bin/archify.mjs guide "<scenario>" --json` and use its
`useWhen`/`avoidWhen`; do not guess.

**Done when:** the type is named, the target path is named, and the source document that the
diagram derives from is identified (spec, ADR, TDD, runbook — the diagram is never the source of
truth).

### 2. Author the source JSON from facts, not from imagination

Create `<target>/<slug>.<type>.json`. Follow the Archify fast authoring path: read **one** matching
schema in `~/.claude/skills/archify/schemas/`, `common.schema.json`, and **one** matching example
in `~/.claude/skills/archify/examples/` — for field shape only. Then:

- Nodes come from the source document and, when the code exists, from the repository (Grep the
  entry points; a component that does not exist in the spec or the code does not go on the map).
- One clear main path, short side branches, sparse labels, at most 12 primary nodes,
  `meta.quality_profile: "showcase"`.
- Use OSForge vocabulary: the same names as `CONTEXT.md`, the spec, and the Prisma schema. A
  diagram that renames things creates a second glossary.
- Set `brand` only for real products with a built-in ID (`node bin/archify.mjs brands --json`;
  the default stack is covered: `next-js`, `supabase`, `prisma`, `postgresql`, `stripe`, `vercel`,
  `cloudflare`, `claude`, `github`, `docker`, `redis`). Never infer a brand from a role.
- Start with automatic routes and labels; add `via`/`labelAt`/sides only when a diagnostic asks.

**Done when:** every node and relationship can be pointed at a line in the source document or a
file in the repository, and the JSON is written to its target path.

### 3. Validate → repair until the diagnostics reach zero

```bash
node ~/.claude/skills/archify/bin/archify.mjs validate <type> <slug>.<type>.json --quality showcase --json
```

Each diagnostic names a `subject`, `evidence`, and `supportedFixes` — change **only** the diagnosed
subject, one geometry control per repair, and rerun. Keep going while the error count reaches a new
minimum; if two consecutive rounds do not improve it, stop and report the unresolved diagnostics
truthfully. Never delete a meaningful relationship label to pass geometry — move it.

**Done when:** `validate` reports `ok: true` with 0 composition errors and 0 warnings under
`showcase` (a receipt with only 4 artifact checks is basic validation, not acceptance).

### 4. Deliver, record the receipt, link it from the source document

```bash
node ~/.claude/skills/archify/bin/archify.mjs deliver <type> <slug>.<type>.json <slug>.html --quality showcase --json
```

A non-zero exit is never success. From the JSON receipt, record in the source document (design.md,
the ADR, the TDD, the runbook) a **Diagrams** entry:

```markdown
## Diagrams
- [System overview](diagrams/system-overview.html) — `architecture`, Archify v2.16.0,
  spec `diagrams/system-overview.architecture.json` sha256 `2611…8d60`, artifact sha256 `614b…47dd`, 9/9 checks
```

Commit the `.json` always; commit the `.html` unless the project ignores `**/diagrams/*.html`
(it is reproducible from the JSON with `deliver`). Present the result through the normal channel
(`osforge-canvas` when a checkpoint is open; otherwise the path). Do not start `preview` unless the
user asks for a live authoring loop.

**Done when:** the HTML exists at the target path, the receipt line is in the source document, and
the JSON is versioned.

### 5. Fallback when the engine is unavailable

If `node ~/.claude/skills/archify/bin/archify.mjs doctor` fails or the directory is missing: say so
in one line, point to `./deploy.sh --with-archify`, and write the diagram as **Mermaid inside the
source document**, labelled `<!-- unverified: Archify unavailable -->`. Add a task
(`osforge-db add-task`) to replace it with a delivered artifact. Never present the Mermaid as an
accepted diagram.

**Done when:** the reader can tell, from the document alone, that the diagram is unverified and
what would make it verified.

## Anti-patterns

| WRONG | RIGHT |
|---|---|
| "Here is the architecture" + a Mermaid block in `design.md` | Typed JSON → `validate` → `deliver` → receipt line in `design.md` |
| Drawing components the spec never mentions "for completeness" | Every node traceable to the spec or the code |
| 25 nodes, every integration, all labels | 8–12 primary nodes, one main path, detail in cards |
| Deleting a label to silence a collision diagnostic | Move the label (`labelDy`/`labelAt`); labels are semantic data |
| `brand: "database"` because the node is a database | `brand` only for a real product with a built-in ID; otherwise omit |
| Claiming success on a non-zero `deliver` or after `validate` alone | `deliver` receipt: 9/9 checks, SHA-256 of spec and artifact |
| Re-drawing the architecture inside `visual-planner` | `visual-planner` links/embeds the delivered HTML |
| Reading `renderers/` or geometry source before the first candidate | Schema + one example, write the candidate, let diagnostics drive |

## References  (progressive disclosure)

- `~/.claude/skills/archify/SKILL.md` — authoring contract, geometry repairs, viewer features
  (read when authoring; installed by `deploy.sh`, not part of this repo)
- `references/pipeline-hooks.md` — the exact step each OSForge command/skill runs to call this
  skill, and the receipt block format
- `docs/ANALISE-ARCHIFY.md` (repo) — why the engine is Archify and what was deliberately left out
