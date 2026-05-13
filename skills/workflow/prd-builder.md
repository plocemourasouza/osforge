# PRD Builder (Collaborative)

**Trigger:** prd, requisitos, requirements, product requirements

---

## Purpose

Facilitação colaborativa de Product Requirements Document. Para projetos com ambiguidade significativa (nível COMPLEX).

**Princípio:** Guia o usuário seção por seção com checkpoints.

---

## Process

### Phase 1: Problem Definition
```
- What problem are we solving?
- Who has this problem? (personas)
- How do they solve it today?
- What's the cost of not solving it?
- Evidence of the problem (data, quotes, observations)
```

### Phase 2: Users & Personas
```
- Primary persona (who benefits most)
- Secondary personas
- Anti-personas (who is this NOT for)
- User journey today vs. desired
```

### Phase 3: Functional Requirements
```
- Core features (must have for MVP)
- Nice-to-have features (v2)
- User stories with acceptance criteria
```

### Phase 4: Non-Functional Requirements
```
- Performance (response times, load)
- Security (auth, data protection)
- Scalability (expected growth)
- Accessibility (WCAG level)
- Compliance (GDPR, LGPD, etc.)
```

### Phase 5: Success Metrics
```
- Primary metric (North Star)
- Secondary metrics
- Baseline values
- Target values
- Measurement method
- Review timeline
```

### Phase 6: Scope & Timeline
```
- MVP scope (smallest viable experiment)
- Phase 2 scope
- Future considerations
- Dependencies
- Constraints
```

---

## Output Format

```markdown
# PRD: [Product/Feature Name]

## Metadata
- Author: [name]
- Created: [date]
- Status: Draft | Review | Approved
- Stakeholders: [list]

## Executive Summary
[2-3 sentences: problem, solution, expected impact]

## Problem Statement

### The Problem
[Clear description]

### Evidence
- [Data point 1]
- [User quote]
- [Observation]

### Current Solutions
[How users solve this today]

### Cost of Inaction
[What happens if we don't solve this]

## Target Users

### Primary Persona
- **Name:** [Persona name]
- **Role:** [Job/context]
- **Goals:** [What they want to achieve]
- **Pain Points:** [Current frustrations]

### Secondary Personas
[Brief descriptions]

### Anti-Personas
[Who this is NOT for]

## Requirements

### Functional Requirements (MVP)
| ID | Requirement | Priority | User Story |
|----|-------------|----------|------------|
| FR1 | [requirement] | Must | As a [user], I want [goal] so that [benefit] |

### Non-Functional Requirements
| ID | Category | Requirement |
|----|----------|-------------|
| NFR1 | Performance | Page load < 2s |
| NFR2 | Security | All data encrypted at rest |

## Success Metrics

| Metric | Baseline | Target | Timeline |
|--------|----------|--------|----------|
| [Primary metric] | [current] | [goal] | [when] |

## Scope

### In Scope (MVP)
- [Feature 1]
- [Feature 2]

### Out of Scope
- [Not doing 1]
- [Not doing 2]

### Future Considerations
- [Phase 2 idea]

## Dependencies
- [Dependency 1]
- [Dependency 2]

## Open Questions
- [ ] [Question 1]
- [ ] [Question 2]

## Appendix
[Mockups, research data, competitive analysis]
```

---

## Checkpoints

After each phase:
```
[C] Continue — Phase complete, move to next
[R] Revisit — Need to clarify something
[P] Pause — Need external input before continuing
```

---

## Output Location

```
docs/prd/{feature}.md
```

With frontmatter:
```yaml
---
type: prd
feature: feature-name
status: draft
created: 2024-01-15
stakeholders: [user, pm]
---
```
