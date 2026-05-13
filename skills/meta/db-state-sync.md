# DB State Sync

**Trigger:** Salvar estado, registrar decisão, add-decision, set-phase, resumir sessão, buscar decisão, osforge-db, estado do projeto, blocker, retomar sessão, where did I leave off.

---

## Purpose

Gerencia o estado de projetos no banco SQLite local do OSForge (`~/.osforge/osforge.db`). Usa `osforge-db` CLI para salvar progresso de fases, registrar decisões arquiteturais, adicionar/resolver blockers e retomar sessões com contexto preciso.

---

## Commands

### Resume Session
```bash
# Get minimal context to resume (~50 tokens)
osforge-db resume

# Output:
# Phase: implementation
# Last: Completed auth API routes
# Next: Frontend login form
# Blockers: None
```

### Save Progress
```bash
# Set current phase
osforge-db set-phase --phase "implementation" --note "Auth API complete"

# Add decision
osforge-db add-decision \
  --title "Use Supabase Auth" \
  --context "Need OAuth + RLS" \
  --decision "Supabase over NextAuth" \
  --consequences "Vendor dependency"
```

### Manage Blockers
```bash
# Add blocker
osforge-db add-blocker --title "API design unclear" --severity high

# Resolve blocker
osforge-db resolve-blocker --id 1 --resolution "Discussed with team"
```

### Search Decisions
```bash
# Full-text search across projects
osforge-db search "authentication"

# Search in current project only
osforge-db search "authentication" --scope local
```

---

## Database Schema

```sql
-- Phases
CREATE TABLE phases (
  id INTEGER PRIMARY KEY,
  project_id TEXT NOT NULL,
  name TEXT NOT NULL,
  note TEXT,
  started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  completed_at DATETIME
);

-- Decisions
CREATE TABLE decisions (
  id INTEGER PRIMARY KEY,
  project_id TEXT NOT NULL,
  title TEXT NOT NULL,
  context TEXT,
  decision TEXT NOT NULL,
  consequences TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Blockers
CREATE TABLE blockers (
  id INTEGER PRIMARY KEY,
  project_id TEXT NOT NULL,
  title TEXT NOT NULL,
  severity TEXT CHECK(severity IN ('low', 'medium', 'high')),
  resolution TEXT,
  resolved_at DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- FTS5 for semantic search
CREATE VIRTUAL TABLE decisions_fts USING fts5(
  title, context, decision, consequences
);
```

---

## Scope Options

| Scope | Database | Use Case |
|-------|----------|----------|
| **global** | `~/.osforge/osforge.db` | Cross-project search |
| **local** | `.osforge/project.db` | Project-specific state |

```bash
# Use local scope
osforge-db add-decision --scope local ...

# Search globally
osforge-db search "prisma" --scope global
```

---

## Integration with Session

At session start:
```bash
osforge-db resume
# Returns minimal context for continuation
```

At checkpoint:
```bash
osforge-db set-phase --phase "review" --note "Implementation complete, starting review"
```

At decision point:
```bash
osforge-db add-decision --title "..." --decision "..."
```

---

## Benefits

- **~50 tokens** to resume vs reading full conversation
- **Cross-project learning** via FTS5 search
- **Audit trail** of architectural decisions
- **Blocker tracking** for async collaboration
