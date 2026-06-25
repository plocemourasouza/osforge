---
name: osforge-evolve
description: |
  Use when: evolve, /evolve, osforge evolve, analyze observations, propose skills, pattern clustering, instinct, promote instinct, continuous learning, close the learning loop, capture session patterns, add-observation, list-instincts, promote-instinct, configuration evolution
---

# OSForge Evolve — Instinct Architecture

Closes the learning loop in OSForge: captures session events as `observations`
in the SQLite database, clusters them by trigger normalization, and proposes concrete diffs in
`skills/` or `rules/` for human approval.

**Principles:** no daemon, no LLM in the clustering, pure stdlib, human-in-the-loop.

---

## Full Flow

```
work session
      │
      ▼
  add-observation            (manual or via the observe-capture.py hook)
      │
      ▼ (on-demand)
  osforge-db evolve          (clusters + proposes diffs)
      │
      ▼ (human reviews)
  edit skills/ or rules/     (manual curation)
      │
      ▼ (confidence ≥ 0.8)
  promote-instinct           (raises scope project → global)
      │
      ▼
  ./deploy.sh                (propagates to ~/.claude/ and ~/.cursor/)
```

---

## Subcommands

### `osforge-db add-observation <project> <trigger_text> [--context=<ctx>] [--tool=<tool>]`

Records a session observation for later clustering.

```bash
osforge-db add-observation my-proj "when writing tests prefer TDD" \
  --context="it got easier with red-green" --tool=Bash
```

- `project` — project slug (e.g., `osforge`, `api-prod`)
- `trigger_text` — descriptive phrase of the observed pattern (e.g., "when adding components run shadcn install")
- `--context` — free-form context or justification
- `--tool` — the tool that generated the observation (e.g., `Bash`, `Edit`, `Write`)

### `osforge-db evolve [--project=<slug>] [--min-count=2]`

Clusters observations by trigger normalization and proposes candidates.

```bash
osforge-db evolve --project=my-proj
osforge-db evolve --min-count=3   # tighter cluster
```

**Output:** a suggested unified diff per cluster, classified as SKILL / COMMAND / AGENT.

Classification rules:
| Criterion | Type |
|----------|------|
| cluster ≥ 3 AND conf ≥ 0.75 | AGENT |
| conf ≥ 0.70 | COMMAND |
| default | SKILL |

The human reviews the diff, edits the actual file in `skills/` or `rules/`, and only then commits.

### `osforge-db list-instincts [--project=<slug>] [--scope=project|global]`

Lists registered instincts, with optional filters.

```bash
osforge-db list-instincts
osforge-db list-instincts --scope=global
osforge-db list-instincts --project=osforge
```

### `osforge-db promote-instinct <instinct_id> [--scope=global]`

Raises an instinct's scope from `project` to `global` (requires confidence ≥ 0.8).

```bash
osforge-db promote-instinct 3
```

`global` instincts are candidates to enter `claude-code/SKILLS.md` or `rules/` via
human curation and `./deploy.sh`.

---

## Data Schema

### `observations` table
| Field | Type | Description |
|-------|------|-----------|
| `id` | INTEGER PK | autoincrement |
| `project` | TEXT | project slug (default `''` = global) |
| `trigger_text` | TEXT | pattern phrase (e.g., "when writing tests prefer TDD") |
| `context` | TEXT | free-form context |
| `tool` | TEXT | generating tool |
| `created_at` | TEXT | UTC ISO8601 |

### `instincts` table
| Field | Type | Description |
|-------|------|-----------|
| `id` | INTEGER PK | autoincrement |
| `trigger` | TEXT | normalized canonical trigger |
| `guidance` | TEXT | concrete guidance |
| `confidence` | REAL 0–1 | estimated confidence |
| `domain` | TEXT | thematic domain |
| `scope` | TEXT | `project` or `global` |
| `project` | TEXT | slug of the originating project |
| `seen_count` | INTEGER | number of observations that produced the instinct |
| `created_at` / `updated_at` | TEXT | UTC ISO8601 |

---

## Hook Integration (observe-capture.py)

The `hooks/observe-capture.py` file is a lightweight `PostToolUse` hook that records observations
automatically. To enable it, add to `hooks-claude-code.json`:

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit|Write|Bash",
      "hooks": [
        {
          "type": "command",
          "command": "python3 ~/.claude/hooks/observe-capture.py"
        }
      ]
    }
  ]
}
```

**Important:** the hook is silent by design (always exit 0) and does not block the main
flow even if the write fails.

---

## Best Practices

- Capture observations at the end of productive sessions, not in real time
- Prefer descriptive triggers: "when X do Y" instead of generic tags
- Use `--min-count=3` for large projects with many observations
- Review the diff suggested by `evolve` — it is a starting point, not a finished recipe
- Only promote instincts to `global` after validation across multiple projects
- Do not edit the `instincts` table directly; use the subcommands

---

## References

- `skills/evolve/references/clustering.md` — detailed normalization heuristic
- `scripts/osforge-db.py` — full implementation (Python stdlib, zero deps)
- `docs/DECISIONS.md` ADR-001 — mandatory deploy flow via `./deploy.sh`
