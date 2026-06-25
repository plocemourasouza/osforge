# Delegation Brief Template

> Workers (sub-agents, Task tools) **do not have access to the conversation with the user**.
> The brief is the only context the worker receives. An incomplete brief produces incomplete
> output — garbage in, garbage out. Fill in all fields before dispatching.

---

## Canonical Template

```markdown
## Objective
<!-- 1-3 sentences: what to do and why it matters now. -->

## Skills to Load
<!-- Exact paths the worker must read BEFORE implementing.
     Example: `skills/stack/prisma.md`, `skills/security-best-practices.md` -->
- 

## File Scope
**May read/edit:**
- 

**Out of scope (do not touch):**
- 

## Essential Context
<!-- Decisions already made, constraints, project patterns the worker must
     respect. Include: relevant stack, conventions, architectural decisions,
     why alternative approaches were discarded. -->

## Done Criterion
<!-- Verifiable: command to run + expected result.
     The worker may NOT report done without running this command and seeing this result. -->
**Command:** `<command>`
**Expected result:** <what should appear>

## Output Format
<!-- What to report back: commit hash? summarized diff? list of findings?
     Be explicit — the worker will not guess. -->

## Parallel-with / Depends-on
<!-- IDs of sibling tasks running in parallel (shared-file warning)
     or tasks that must complete before this worker starts. -->
- Parallel-with: (none | task-X)
- Depends-on: (none | task-Y complete)
```

---

## Complete Example

```markdown
## Objective
Create endpoint `POST /api/products` with Zod validation and persistence via Prisma.
Validation must run before any write to the database to ensure that
invalid data never reaches storage.

## Skills to Load
- `skills/stack/prisma.md` — schema patterns and transaction handling
- `skills/api-patterns.md` — Route Handler structure and error handling
- `skills/security-best-practices.md` — "Zod validation on ALL external input" section

## File Scope
**May read/edit:**
- `app/api/products/route.ts` (create if it does not exist)
- `lib/validations/product.ts` (create if it does not exist)
- `prisma/schema.prisma` (read only — do not change)
- `types/product.ts` (read only — use the existing types)

**Out of scope (do not touch):**
- Any other file in `app/api/`
- Prisma migrations — schema is already approved
- Existing E2E tests

## Essential Context
- Stack: Next.js App Router, TypeScript strict, Prisma 5, Bun
- Error convention: `{ error: string, code: string }` with the correct HTTP status
- Authentication: `lib/auth/session.ts` already exists — import `getSession()` and
  return 401 if the session is null (do not implement auth from scratch)
- The `Product` model in the schema has required fields: `name`, `price`, `tenantId`
- `tenantId` must come from the session, NEVER from the request body

## Done Criterion
**Command:** `bun test app/api/products/route.test.ts`
**Expected result:** all tests passing, 0 failures

(If the test file does not exist, create it before implementing — TDD mandatory.)

## Output Format
Report:
1. Hash of the commit with the implementation
2. Test summary: `N passed, 0 failed`
3. If there is a non-obvious design decision, list it in 1-2 bullets

## Parallel-with / Depends-on
- Parallel-with: task-frontend-product-form (distinct files — no conflict)
- Depends-on: task-schema-product complete (migration must already be applied)
```

---

## Model Selection

| Model | Use when |
|--------|-------------|
| `haiku` | Mechanical tasks: format output, generate simple boilerplate, search docs |
| `sonnet` | Standard implementation: CRUD, components, refactoring, unit tests |
| `opus` / `fable` | High complexity: schema migrations with cross-tenant impact, distributed system design, concurrency, architectural decisions with non-obvious trade-offs |

**Quick rule:** when a model's judgment error can cost hours of
rollback (migrations, design of public API contracts, RLS changes),
use opus/fable. For everything else, sonnet is enough.
