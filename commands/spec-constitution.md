---
description: Creates or updates the project constitution — principles, conventions, and governance that guide all technical decisions. Use when starting a new project or when you need to formalize team rules. Triggers: "project constitution", "create constitution", "define principles", "governance".
---

## Required context
Read before executing:
- `README.md` (if it exists) — project overview
- `.specs/memory/constitution.md` (if it exists) — previous version to update
- `package.json` — current stack

## Phase: Pre-project — Constitution

## Expected output
`.specs/memory/constitution.md`

## Process

1. **Check existence**: If `.specs/memory/constitution.md` exists, load it and identify the current version.

2. **Collect values** for the following elements:
   - Project name and core purpose
   - Development principles (maximum 7, minimum 3)
   - Mandatory technical stack
   - Quality standards (tests, code review, deploy)
   - Naming and structure conventions
   - Criteria for accepting or rejecting architectural changes

3. **Version**: If it's a new constitution → v1.0.0. If it's an update:
   - Principle change → MAJOR (v2.0.0)
   - New principle added → MINOR (v1.1.0)
   - Clarification or fix → PATCH (v1.0.1)

4. **Create** `.specs/memory/` (if it doesn't exist) and save the file:

```markdown
# Project Constitution: [NAME]
**Version:** [x.y.z] | **Ratified:** [YYYY-MM-DD] | **Last changed:** [YYYY-MM-DD]

## Purpose
[A single sentence defining what this project does and for whom]

## Principles
1. **[Name]**: [Description — how to apply it, what it implies]
2. **[Name]**: [Description]
...

## Mandatory Stack
[List with pinned versions]

## Quality Standards
- Minimum test coverage: [%]
- Code review: [who reviews, criteria]
- Deploy: [process, branches]

## Conventions
[Naming, folder structure, commit patterns]

## Criteria for Architectural Changes
[What justifies changing the architecture vs. adapting within it]
```

5. **Confirm** with the user: version created/updated, file path, next steps.

## Notes
- Do not ask for each field individually — use existing context and inference from the README/package.json
- If the user provided input, use it directly without re-confirming each item
- The constitution is referenced by the `/spec-specify` and `/spec-design` commands
