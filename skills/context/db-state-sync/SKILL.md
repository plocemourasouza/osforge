---
name: db-state-sync
description: "Manages project state in OSForge's local SQLite database (~/.osforge/osforge.db). Use when: saving phase progress, recording an architectural decision, adding/resolving a blocker, tracking tasks, viewing the cross-project board, resuming a previous session, searching past decisions. Keywords: save state, record decision, add-decision, set-phase, add-task, set-task, list-tasks, board, resume session, search decision, osforge-db, project state."
model: haiku
allowed-tools: Bash
metadata:
  author: osforge
  version: '1.1'
---

## Database available
!`osforge-db stats 2>/dev/null || echo "database not initialized — run: osforge-db init"`

# DB State Sync

## Role

Interface between the orchestrator and OSForge's local SQLite database.
Runs queries via the `osforge-db` CLI without token overhead — every state
read returns only what is needed.

---

## Database

Default location: `~/.osforge/osforge.db` (global, cross-project)
Local location: `.osforge/osforge.db` (per project, via `--scope=local`)

`osforge-db` uses Python's built-in `sqlite3` — zero external dependencies.

---

## Commands by situation

### INTAKE — resume session

```bash
# Returns current phase + resume point (compact shell injection, ~50 tokens)
osforge-db resume <slug>

# Returns complete state (all phases, blockers, recent decisions)
osforge-db status <slug>

# List all active projects
osforge-db list-projects
```

**Shell injection in SKILL.md** (use inside any planning skill):
```
!`osforge-db resume PROJECT_SLUG`
```

### TRACK — update progress

```bash
# Create/update project
osforge-db upsert-project <slug> "<description>" <triage> <status>

# Change a phase's status
osforge-db set-phase <slug> "<phase name>" in-progress skills/planning/spec-builder
osforge-db set-phase <slug> "<phase name>" complete skills/planning/spec-builder docs/specs/feature.md

# Save resume point (end session)
osforge-db set-resume <slug> "<where you stopped and the exact next step>"
```

### DECISIONS — record and search

```bash
# Record decision
osforge-db add-decision <slug> "<decision>" --category=arch
osforge-db add-decision <slug> "<decision>" --category=product
osforge-db add-decision <slug> "<decision>" --category=ux
osforge-db add-decision <slug> "<decision>" --category=data
osforge-db add-decision <slug> "<decision>" --category=security

# List recent decisions
osforge-db list-decisions <slug> --category=arch --limit=10

# Cross-project FTS5 search (returns semantically related decisions)
osforge-db search "Prisma RLS multi-tenant"
osforge-db search "OAuth authentication" --project=<slug>
```

### TASKS — track tasks + cross-project board

```bash
# Create task (initial status: pending). All flags optional.
osforge-db add-task <slug> "<title>"
osforge-db add-task <slug> "<title>" --phase="<phase name>" --wave=1 --depends=1,2 --priority=p0
# → prints the id of the created task (e.g.: "Task #5 created")
# --phase resolves by name (the phase must exist; create it with set-phase first)
# --depends is a CSV of task ids (free text, not validated against FK)
# --priority: p0 (critical) | p1 (default) | p2

# Update a task's status
osforge-db set-task <slug> <task_id> in-progress
osforge-db set-task <slug> <task_id> done
# valid statuses: pending | in-progress | done | blocked | cancelled

# List a project's tasks (compact)
osforge-db list-tasks <slug>
osforge-db list-tasks <slug> --status=in-progress
# format: [id] status priority wave:N title (deps: ...)

# Cross-project board: tasks from all projects grouped by status
osforge-db board                 # default: only projects with status=active
osforge-db board --status=all    # includes archived/inactive projects
# group order: in-progress → blocked → pending → done (only the last 3)
# projects with no tasks appear as "<slug>: no tasks"
```

### BLOCKERS — track impediments

```bash
# Add blocker
osforge-db add-blocker <slug> "<description>" --waiting="<what it is waiting on>"

# List active blockers
osforge-db list-blockers <slug>

# Resolve blocker
osforge-db resolve-blocker <slug> <id>
```

### MIGRATION — import existing status.yaml

```bash
# Migrates .osforge/status.yaml into the database
osforge-db import-yaml .osforge/status.yaml <slug>
```

---

## Decision categories

| Category | When to use |
|---|---|
| `arch` | Architecture and stack decisions (default) |
| `product` | Product, scope, priority decisions |
| `ux` | Interface and experience decisions |
| `data` | Schema, migrations, data decisions |
| `security` | Security, auth, LGPD decisions |

---

## Integration with the orchestrator

The orchestrator uses `osforge-db` at two moments:

**INTAKE** — when starting a session:
```bash
# Check whether there is work in progress
osforge-db list-projects --status=active

# Load the current project's state
osforge-db status <slug>
```

**TRACK** — when completing each phase:
```bash
osforge-db set-phase <slug> "<phase>" complete <skill-path> <artifact-path>
osforge-db add-decision <slug> "<decision made in this phase>"
osforge-db set-resume <slug> "Next: <phase> via <skill>"
```

---

## Gotchas

- **Project slug**: use consistent kebab-case. The slug is the primary key for everything — `linkme-tur`, `essent-billing`, `rede-essent-portal`. Never change it after creating.
- **FTS5 and hyphens**: the search already sanitizes hyphens automatically. No need to escape.
- **Global vs local database**: for projects with sensitive data (Essent, Rede Essent Jus), use `--scope=local` — the database stays in the project and can be `.gitignore`d. The global database holds only non-sensitive state and decisions.
- **set-resume is mandatory when ending**: without an updated `set-resume`, the next session won't know where you stopped. Treat it like a git commit — always run it before closing the editor.
- **import-yaml is idempotent**: it can be run multiple times on the same project without duplicating phases (uses `ON CONFLICT DO NOTHING`).
