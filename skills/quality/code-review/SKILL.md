---
name: code-review
description: "Structured code review with a checklist adapted to the OSForge stack. Use when: code review, review code, review PR, CR. Integrates adversarial-review and edge-case-hunter automatically. Keywords: code review, review code, review PR, CR, pull request, diff, changes, review changes."
model: sonnet
context: fork
agent: general-purpose
allowed-tools: Read, Bash, Glob, Grep
metadata:
  version: '1.1'
---

## Review context
!`git log --oneline -10 2>/dev/null || echo "Git not available or not initialized"`
!`git diff --stat HEAD 2>/dev/null | tail -5 || echo "Diff not available"`

# Code Review

## Role
A rigorous but constructive technical reviewer. Focus on correctness, security,
performance and maintainability. Respects project-context.md.

## Inputs
- **diff or changes** — Code to review (identify automatically)
- **story file** (optional) — If it exists, verify ACs against the implementation
- **project-context.md** — Codebase rules (load if it exists)

## Execution

### 1. Identify Scope
- Identify modified files and the type of change
- Load the story file if referenced
- Load project-context.md

### 2. Structured Checklist

**Functionality:**
- [ ] All story ACs satisfied? (if a story exists)
- [ ] Business logic correct for the happy path?
- [ ] Error states handled appropriately?
- [ ] Loading states implemented? (for UI changes)

**TypeScript:**
- [ ] Correct and specific types (no `any`)?
- [ ] Strict mode respected?
- [ ] Interfaces/types exported when necessary?
- [ ] Zod schemas for external inputs?

**Next.js Patterns:**
- [ ] Server vs Client Components correct?
- [ ] Server Actions vs API Routes per the project's pattern?
- [ ] Metadata/SEO configured (for pages)?
- [ ] Error boundaries and loading states?

**Database/Supabase:**
- [ ] Prisma queries efficient (no N+1)?
- [ ] RLS policies covering new data?
- [ ] Migrations reversible?
- [ ] Indexes for frequent queries?

**Security:**
- [ ] Inputs validated with Zod?
- [ ] Auth verified on endpoints?
- [ ] No sensitive data exposed on the client?
- [ ] CORS and rate limiting if applicable?
- [ ] LGPD compliance (personal data)?

**Quality:**
- [ ] No console.log or debug code?
- [ ] Imports organized?
- [ ] Naming conventions followed?
- [ ] No duplicated code?
- [ ] Tests for happy path + edge cases?

### 3. Deep Analysis
- Invoke `edge-case-hunter` on the diff (if changes > 20 lines)
- Identify patterns that diverge from project-context

**Concrete examples of edge cases to look for:**
- **Null/undefined**: `user.profile.name` when `profile` may be `null`; `findUnique` return not checked before accessing fields
- **Empty strings**: `""` passing a validation that only checks `!== null`; search/filter with empty input returning everything
- **Race conditions**: two simultaneous requests creating a "unique" record without a constraint in the database; `read-modify-write` without a transaction (e.g., decrementing balance/inventory)
- **Empty arrays**: `items[0]` without checking length; `reduce` without an initial value on an empty array
- **Numeric limits**: pagination with `page=0` or negative; monetary values with float instead of Decimal

### 4. Verdict

```markdown
## Code Review: {identification}

**Verdict:** APPROVED | CHANGES_REQUESTED
**Files reviewed:** {N}
**Findings:** {N}

### Issues (must be resolved)
1. {issue with location and suggestion}

### Suggestions (recommended)
1. {suggestion}

### Positives
1. {something that turned out well}
```

If CHANGES_REQUESTED: list each issue with a suggested fix.
If APPROVED: may include optional suggestions to improve.


## Gotchas

- **Approving without verifying the story ACs**: if there is an associated story, ALWAYS verify each AC against the code. Many PRs pass technical review but silently fail the business acceptance criteria.
- **Focusing only on style issues**: code style review (imports, naming) is Low priority. Security issues, incorrect business logic and N+1 queries are High priority. Don't invest 80% of the review in formatting problems.
- **Not invoking edge-case-hunter**: for diffs >20 lines, edge-case-hunter is mandatory — it finds cases that manual review routinely misses (null values, empty strings, concurrency, pagination limits).
- **APPROVED with "optional suggestions" that are critical**: if an issue is critical for security or correctness, it must be CHANGES_REQUESTED, not APPROVED with a note. The distinction matters for the PR workflow.
- **Not checking the impact of schema changes**: every change in `prisma/schema.prisma` requires verification of: (1) the generated migration, (2) impacted RLS policies, (3) queries that may break with the new schema.
- **Ignoring `bun tsc --noEmit`**: always mention whether the type-check passes. TypeScript errors silenced with `@ts-ignore` or `any` are red flags that must appear in the review report.
