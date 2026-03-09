---
name: doc-sanitization
description: Clean up, consolidate, and organize project documentation. Removes obsolete specs, merges duplicates, enforces lifecycle rules. Use when triggered by /clean-docs command, when docs accumulate over 5 files in specs/ or plans/, when documents are older than 30 days, or when the user mentions organizing, cleaning, or reviewing documentation.
---

# Documentation Sanitization

Triggers: `/clean-docs`, "limpar docs", "organizar documentação", or automatically every 10 interactions.

## Permanent Documents (always maintain)
- `README.md` — Project overview, setup, run instructions
- `tasks/todo.md` — Active tasks and immediate backlog
- `tasks/lessons.md` — Learnings, avoided errors, project rules
- `docs/architecture.md` — Architectural decisions and rationale
- `docs/features.md` — Consolidated feature documentation

## Temporary Documents (consolidate or remove after 30 days)
- `specs/*.md` — Feature specifications during development
- `plans/*.md` — Implementation plans during execution
- `notes/*.md` — Work notes, drafts, investigations

## Sanitization Process

### Step 1: Inventory
```bash
find . -name "*.md" -path "*/docs/*" -o -path "*/specs/*" -o -path "*/plans/*" -o -path "*/notes/*" -o -path "*/tasks/*" | sort
```
List all docs organized by category with last modified date.

### Step 2: Analyze
For each document evaluate:
- Last modified date (>30 days = candidate for removal)
- Current relevance (feature delivered? plan executed?)
- Overlap with other documents
- Consolidation potential

### Step 3: Propose
Present structured proposal:
- **KEEP**: Documents to maintain as-is
- **CONSOLIDATE**: Documents to merge (specify target)
- **REMOVE**: Documents to delete (specify reason)
- **REORGANIZE**: Structural improvements

### Step 4: Confirm
**NEVER remove or alter documentation without explicit user approval.**

### Step 5: Execute
After approval:
1. Consolidate relevant content before removing sources
2. Update cross-references
3. Extract important decisions → `docs/architecture.md`
4. Extract learnings → `tasks/lessons.md`

### Step 6: Report
Summary: documents removed, consolidated, and final structure.

## Decision Rules

| Condition | Action |
|-----------|--------|
| Permanent doc | Keep, update if stale |
| Feature delivered >30 days | Consolidate → `docs/features.md`, then remove |
| Plan executed | Extract decisions → `docs/architecture.md`, then remove |
| Notes with learnings | Move to `tasks/lessons.md`, then remove |
| Duplicated content | Merge into single source |
| Empty/placeholder only | Remove |
| Uncertain | **Ask user** |

## Urgency Indicators
- More than 5 files in `specs/` or `plans/`
- Documents >60 days without modification
- `tasks/todo.md` with >50 items including completed ones
- Difficulty locating relevant information
