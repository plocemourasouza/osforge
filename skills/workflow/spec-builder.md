# Spec Builder (Collaborative)

**Trigger:** spec, especificar, definir feature, tech spec

---

## Purpose

Facilitação colaborativa de especificação técnica. Produz tech-spec com acceptance criteria testáveis, tasks ordenadas por dependência, e riscos.

**Princípio:** Não gera — FACILITA com o usuário.

---

## Process

### 1. Context Gathering
```
- What problem are we solving?
- Who is the user?
- What does success look like?
- What are the constraints?
```

### 2. Requirements Elicitation
```
- Functional requirements (must have)
- Non-functional requirements (performance, security)
- Out of scope (explicitly)
- Assumptions
```

### 3. Acceptance Criteria
Each requirement gets testable ACs:
```
GIVEN [precondition]
WHEN [action]
THEN [expected result]
```

### 4. Task Breakdown
```
- Tasks ordered by dependency
- Each task has file paths
- Estimated complexity (S/M/L)
- Blockers identified
```

### 5. Risks
```
- Technical risks
- Integration risks
- Timeline risks
- Mitigation strategies
```

---

## Output Format

```markdown
# Tech Spec: [Feature Name]

## Status
- Author: [name]
- Created: [date]
- Status: Draft | In Review | Approved

## Problem Statement
[Clear description of the problem]

## Solution Overview
[High-level approach]

## Requirements

### Functional
- [ ] FR1: [requirement]
- [ ] FR2: [requirement]

### Non-Functional
- [ ] NFR1: Performance - [requirement]
- [ ] NFR2: Security - [requirement]

## Out of Scope
- [What we're NOT doing]

## Acceptance Criteria

### AC1: [Scenario Name]
- GIVEN [precondition]
- WHEN [action]
- THEN [expected result]

## Technical Design
[Architecture decisions, data flow, component structure]

## Tasks

| # | Task | Files | Complexity | Depends On |
|---|------|-------|------------|------------|
| 1 | Setup database schema | `prisma/schema.prisma` | M | - |
| 2 | Create API endpoint | `app/api/feature/route.ts` | M | 1 |
| 3 | Build UI component | `components/feature.tsx` | L | 2 |

## Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [risk] | High | Medium | [strategy] |

## Open Questions
- [ ] [Question needing answer before implementation]
```

---

## Checkpoint

Before moving to implementation:

```
[A] Approve — Ready to implement
[E] Edit — Needs changes (specify)
[S] Simplify — Scope too large, reduce
```

---

## Stack Awareness

Respects `project-context.md` for:
- Tech stack constraints
- Existing patterns
- Naming conventions
- File structure

---

## Output Location

```
docs/specs/{feature}.md
```

With frontmatter:
```yaml
---
feature: feature-name
status: draft
created: 2024-01-15
author: user
---
```
