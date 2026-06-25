---
name: artifact-chain
description: >
  Always-on rule that guarantees traceability between planning artifacts
  and respect for project-context.md as the project's constitution.
type: always-on
version: 1.0.0
---

# Rule: Artifact Chain

## Traceability

- Every spec must reference project-context.md (if it exists).
- Every story must reference the spec or epic that originated it.
- Every code review must reference the story being reviewed.
- Every architecture decision must be documented as an ADR.
- Frontmatter with `depends_on: []` in artifacts that depend on others.

## Project Context as Constitution

- If `project-context.md` exists in the project, it is the source of truth for:
  - Stack and versions
  - Naming conventions
  - Code patterns
  - Security rules
  - Forbidden anti-patterns
- Any skill or agent MUST load project-context.md before generating
  code or making technical decisions.
- If a decision conflicts with project-context.md, HALT and ask the
  user which one prevails.
- If project-context.md does not exist in an existing project: suggest generating it
  via `skills/context/project-context-generator` before significant work.

## Language

- Communication with the dev: reply in the user's language (ADR-011)
- All repository content and artifacts: English (ADR-011)
- Code: always in English (variables, functions, comments, commits)
- Conventional Commits in English: `feat:`, `fix:`, `refactor:`, etc.
