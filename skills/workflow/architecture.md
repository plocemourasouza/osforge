# Architecture Builder (ADR)

**Trigger:** architecture, technical decisions, ADR, schema changes

---

## Purpose

Facilitation of architectural decisions with ADRs (Architecture Decision Records). Stack-aware — optimizes for Next.js/Prisma/Supabase.

**Principle:** FACILITATES the decision — does not decide on its own.

---

## When to Use

- Schema changes affecting multiple models
- New integration patterns
- Technology selection
- Data flow redesign
- Performance architecture changes
- Security model changes

---

## ADR Format

```markdown
# ADR-[number]: [Title]

## Status
Proposed | Accepted | Deprecated | Superseded by ADR-XX

## Date
[YYYY-MM-DD]

## Context
[What is the issue? Why do we need to decide?]

## Decision Drivers
- [Driver 1: e.g., performance requirement]
- [Driver 2: e.g., team familiarity]
- [Driver 3: e.g., cost constraint]

## Options Considered

### Option 1: [Name]
**Description:** [How it works]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Effort:** [S/M/L]

### Option 2: [Name]
[Same structure]

### Option 3: [Name]
[Same structure]

## Decision
[Which option and WHY]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Trade-off 1]
- [Trade-off 2]

### Risks
- [Risk 1 and mitigation]

## Implementation Notes
- [Migration path if needed]
- [Affected files/systems]
- [Rollback strategy]
```

---

## Stack-Specific Guidance

### Prisma Migrations
```
1. Review generated SQL before applying
2. Additive changes only in production
3. Two-phase drops (deprecate → remove)
4. Test with production data copy
```

### Supabase RLS
```
1. Enable RLS on all multi-tenant tables
2. Separate policies per operation
3. Test with multiple user roles
4. Document policy logic
```

### Next.js Patterns
```
1. Server Components by default
2. Route Handlers for API
3. Server Actions for mutations
4. Middleware for auth/redirects
```

---

## Process

### 1. Problem Framing
```
- What architectural decision do we need to make?
- What constraints exist?
- What are the quality attributes that matter?
```

### 2. Options Generation
```
- At least 2-3 viable options
- Include "do nothing" if applicable
- Consider unconventional approaches
```

### 3. Evaluation
```
- Score options against decision drivers
- Identify trade-offs explicitly
- Consider long-term implications
```

### 4. Decision
```
- Choose option with clear justification
- Document dissenting views if any
- Identify implementation steps
```

---

## Output Location

```
docs/specs/arch-decisions-{feature}.md
```

Or in central location:
```
docs/architecture/decisions/
├── ADR-001-database-selection.md
├── ADR-002-auth-strategy.md
└── ADR-003-caching-layer.md
```

---

## Migration Path Template (Prisma)

```markdown
## Migration Plan

### Phase 1: Preparation
- [ ] Backup production database
- [ ] Test migration on staging
- [ ] Prepare rollback script

### Phase 2: Additive Changes
- [ ] Add new columns/tables (nullable or with defaults)
- [ ] Deploy code that writes to both old and new
- [ ] Verify data integrity

### Phase 3: Data Migration
- [ ] Backfill existing data
- [ ] Verify migration completeness
- [ ] Monitor for issues

### Phase 4: Cutover
- [ ] Switch reads to new structure
- [ ] Remove writes to old structure
- [ ] Mark old columns as deprecated

### Phase 5: Cleanup (next release)
- [ ] Remove deprecated columns
- [ ] Clean up old code paths
```
