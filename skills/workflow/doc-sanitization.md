# Doc Sanitization

**Trigger:** /clean-docs, docs accumulating, docs >30 days old

---

## Purpose

Clean up, consolidate, and organize project documentation. Removes obsolete specs, merges duplicates, enforces lifecycle rules.

---

## Document Categories

### Permanent Docs (Always Maintain)
```
README.md
tasks/todo.md
tasks/lessons.md
docs/architecture.md
docs/features.md
CHANGELOG.md (if exists)
```

### Temporary Docs (Consolidate/Remove After 30 Days)
```
specs/*.md
plans/*.md
notes/*.md
.osforge/designs/*.md
```

---

## Process

### 1. Inventory
```bash
# Find all markdown files
find . -name "*.md" -type f | grep -v node_modules | grep -v .git

# Check ages
find . -name "*.md" -mtime +30 -type f | grep -v node_modules
```

### 2. Analyze
For each document:
- Is it still relevant?
- Is it a duplicate?
- Should it be merged?
- Should it be archived?

### 3. Propose
```markdown
## Sanitization Proposal

### Keep (no changes)
- README.md — Active, current
- docs/architecture.md — Reference doc

### Archive
- specs/user-auth.md — Feature shipped 45 days ago
- plans/q1-roadmap.md — Quarter ended

### Merge
- notes/api-ideas.md + notes/api-design.md → docs/api-design.md

### Delete
- specs/abandoned-feature.md — Never implemented, no longer planned

### Update
- README.md — Outdated installation instructions
```

### 4. Confirm
**NEVER delete without approval.**

```
Please confirm:
- [A] Archive: [list]
- [M] Merge: [list]
- [D] Delete: [list]

Type 'CONFIRM' to proceed or specify changes.
```

### 5. Execute
```bash
# Archive
mkdir -p .osforge/archive/$(date +%Y-%m)
mv specs/old-feature.md .osforge/archive/$(date +%Y-%m)/

# Merge
cat notes/file1.md notes/file2.md > docs/merged.md
rm notes/file1.md notes/file2.md

# Delete (only after explicit confirmation)
rm specs/abandoned.md
```

### 6. Report
```markdown
## Sanitization Report

**Date:** 2024-01-15
**Files processed:** 23

### Actions Taken
- Archived: 5 files → .osforge/archive/2024-01/
- Merged: 2 files → docs/api-design.md
- Deleted: 1 file (abandoned-feature.md)
- Updated: 1 file (README.md)

### Remaining
- 15 active documents
- Next review: 2024-02-15
```

---

## Lifecycle Rules

| Document Type | Max Age | Action After |
|---------------|---------|--------------|
| Feature spec (shipped) | 30 days | Archive |
| Feature spec (abandoned) | 14 days | Delete (with confirmation) |
| Meeting notes | 30 days | Archive or delete |
| Design docs | 60 days | Archive |
| ADRs | Never | Keep forever |
| Lessons learned | Never | Keep forever |

---

## Archive Structure

```
.osforge/archive/
├── 2024-01/
│   ├── user-auth-spec.md
│   └── q4-roadmap.md
├── 2024-02/
│   └── payment-design.md
```

---

## Quality Checks

### For Permanent Docs
- [ ] README has current setup instructions
- [ ] Architecture doc reflects actual system
- [ ] Features doc lists actual features
- [ ] No broken internal links

### For Temporary Docs
- [ ] Specs have status (draft/approved/shipped)
- [ ] Plans have dates
- [ ] Notes have context

---

## Automation Suggestion

Add to monthly maintenance:
```bash
# In package.json scripts
"docs:audit": "find . -name '*.md' -mtime +30 -type f | grep -v node_modules | grep -v .git | grep -v archive"
```
