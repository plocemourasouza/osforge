---
description: Phase 2 — Creates the technical design: architecture, data model, API contracts, and technical decisions with documented trade-offs. Use after /spec-specify. Triggers: "design", "feature architecture", "data model", "API contracts", "/spec-design [feature]".
---

## Required context
Read before executing:
- `.specs/features/[feature]/spec.md` — requirements and acceptance criteria
- `.specs/memory/constitution.md` — project architecture standards
- `schema.prisma` (if it exists) — current data model
- `.specs/codebase/ARCHITECTURE.md` (if it exists) — current architecture

## Phase: Phase 2 — Design

## Expected output
`.specs/features/[feature-name]/design.md`

## Process

1. **Load spec.md**: Read the functional requirements and acceptance criteria to guide the design decisions.

2. **Analyze the current schema**: If `schema.prisma` exists, check the data model before proposing changes. Consult the Supabase MCP to verify the real state if available.

3. **Create `design.md`**:

```markdown
# Design: [Feature Name]
**Feature:** [feature-name] | **Date:** [YYYY-MM-DD] | **Status:** Draft
**Reference:** [spec.md]

## Architecture

### Data Flow
[Text or Mermaid diagram showing how data flows]

### Components Involved
- **[Component/module]**: [responsibility in this feature]
- Server Actions: [which actions and in which file]
- API Routes: [only if external integration — justify why it isn't a Server Action]
- React Components: [Server vs Client — justify each Client Component]

## Data Model

### Schema Changes
```prisma
// New tables or fields required
model [Name] {
  id        String   @id @default(cuid())
  // ...
}
```

### Required Migrations
- [Describe each migration in natural language]

### RLS Policies (if Supabase)
- [Table]: [SELECT/INSERT/UPDATE/DELETE] for [role] when [condition]

## Contracts

### Server Actions
```typescript
// src/actions/[feature].actions.ts
export async function [actionName](input: [InputType]): Promise<[ReturnType]>
```

### TypeScript Types
```typescript
// src/types/[feature].types.ts
type [Name] = {
  // ...
}
```

## Technical Decisions

### Decision 1: [Title]
- **Context:** [Why this decision was necessary]
- **Options considered:**
  - A: [description] — Pros: [...] Cons: [...]
  - B: [description] — Pros: [...] Cons: [...]
- **Decision:** [Which option and why]
- **Consequences:** [What this decision implies for the future]

## Impact on Existing Features
- [Affected feature/component]: [how it is impacted, whether it requires changes]
- No impact: [areas checked and confirmed unaffected]

## Constitution Check
- [ ] Design respects [architectural principle from the constitution]
- [ ] No undocumented exception to the defined standards
```

4. **Confirm**: Present the design. For decisions with significant trade-offs, present the options explicitly and wait for confirmation before recording the decision in the file. Suggest next step: `/spec-tasks [feature-name]`.

## Rules
- Every decision with non-trivial alternatives must be documented as an ADR (Architecture Decision Record)
- Server Actions are the default; API Routes require explicit justification
- RLS is mandatory for tables with multi-tenant data
- Do not implement code in this phase — only contracts and types
