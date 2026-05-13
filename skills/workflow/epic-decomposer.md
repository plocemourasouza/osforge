# Epic Decomposer

**Trigger:** épicos, stories, decompor, breakdown

---

## Purpose

Decompõe specs, PRDs ou requisitos em épicos e stories implementáveis. Cada story com ACs testáveis, tasks com file paths, dependências mapeadas.

---

## Epic Structure

```markdown
# Epic: [Epic Name]

## Overview
[Brief description of what this epic delivers]

## Business Value
[Why this matters to users/business]

## Success Criteria
- [Measurable outcome 1]
- [Measurable outcome 2]

## Stories
1. [Story 1 Title]
2. [Story 2 Title]
3. [Story 3 Title]

## Dependencies
- [External dependency]
- [Other epic dependency]

## Risks
- [Risk and mitigation]
```

---

## Story Structure

```markdown
# Story: [Story Title]

## Epic
[Parent epic reference]

## Description
As a [user type],
I want [goal],
So that [benefit].

## Acceptance Criteria

### AC1: [Scenario]
- GIVEN [precondition]
- WHEN [action]
- THEN [expected result]

### AC2: [Scenario]
- GIVEN [precondition]
- WHEN [action]
- THEN [expected result]

## Tasks

| # | Task | File(s) | Complexity |
|---|------|---------|------------|
| 1 | [task description] | `path/to/file.ts` | S |
| 2 | [task description] | `path/to/file.ts` | M |

## Dependencies
- Requires: [Story X] to be complete
- Blocks: [Story Y]

## Notes
- [Implementation consideration]
- [Edge case to handle]
```

---

## Decomposition Rules

### Right-Sized Stories
```
Too Big: "Implement user authentication"
Right: "User can log in with email/password"
Right: "User can reset password via email"
Right: "User session persists across browser refresh"
```

### INVEST Criteria
- **I**ndependent — Can be developed separately
- **N**egotiable — Details can be discussed
- **V**aluable — Delivers user value
- **E**stimable — Can estimate effort
- **S**mall — Fits in a sprint
- **T**estable — Has clear acceptance criteria

### Dependency Mapping
```
Story A (no deps) ──┐
                    ├──▶ Story C
Story B (no deps) ──┘
                         │
                         ▼
                    Story D
```

---

## Complexity Estimation

| Size | Description | Typical Scope |
|------|-------------|---------------|
| S | Trivial | 1-2 files, straightforward |
| M | Moderate | 3-5 files, some complexity |
| L | Large | 6+ files, significant complexity |
| XL | Epic-level | Should be broken down further |

---

## Output Structure

```
docs/specs/stories/{feature}/
├── index.md           # Epic overview + story list
├── story-01-login.md
├── story-02-password-reset.md
└── story-03-session.md
```

---

## Story Status Tracking

```yaml
# In each story file
---
story: story-01-login
epic: user-authentication
status: todo | in_progress | review | done
assignee: null
started: null
completed: null
---
```

---

## Process

### 1. Identify Epics
```
- Group related functionality
- Each epic delivers cohesive value
- 3-7 stories per epic typically
```

### 2. Write Stories
```
- Start with user-facing stories
- Add technical stories only if necessary
- Each story independently deployable (ideally)
```

### 3. Map Dependencies
```
- Identify blockers
- Optimize parallel work
- Flag critical path
```

### 4. Estimate & Prioritize
```
- Size each story
- Prioritize by value/effort ratio
- Identify MVP subset
```
