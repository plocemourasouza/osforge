# Code Review

**Trigger:** code review, review code, review PR

---

## Review Dimensions

### 1. Correctness
- Does the code do what it's supposed to?
- Are edge cases handled?
- Are error conditions handled?
- Does it match the acceptance criteria?

### 2. Security
- Input validation present?
- Auth/authz checks in place?
- No sensitive data exposed?
- No injection vulnerabilities?

### 3. Performance
- No N+1 queries?
- No unnecessary re-renders?
- Large data sets handled efficiently?
- No memory leaks?

### 4. Maintainability
- Code is readable?
- Functions are focused (SRP)?
- No code duplication?
- Clear naming?

### 5. Testing
- Tests cover happy path?
- Tests cover edge cases?
- Tests cover error cases?
- Tests are readable?

### 6. Style
- Follows project conventions?
- Consistent formatting?
- No debug code?
- No commented-out code?

---

## OSForge Stack Checklist

### TypeScript
- [ ] Strict mode compliant
- [ ] No `any` types
- [ ] No `@ts-ignore` without justification
- [ ] Named exports (no `export default`)

### Next.js
- [ ] Server Components by default
- [ ] `"use client"` only when necessary
- [ ] Server Actions for mutations
- [ ] Proper error boundaries

### Prisma
- [ ] `select` specified (not selecting *)
- [ ] No N+1 (using `include` properly)
- [ ] Migrations reviewed

### Supabase
- [ ] RLS policies in place
- [ ] Using `getUser()` not `getSession()`
- [ ] Auth checks in Server Actions

### UI (shadcn)
- [ ] Using existing components
- [ ] Consistent with design system
- [ ] Accessible (keyboard, screen reader)
- [ ] Responsive

---

## Review Process

### 1. Understand Context
```
- Read the PR description
- Check linked issues/specs
- Understand the goal
```

### 2. Big Picture Review
```
- Is the approach sound?
- Are there architectural concerns?
- Is the scope appropriate?
```

### 3. Detailed Review
```
- Go file by file
- Check logic correctness
- Look for edge cases
- Verify tests
```

### 4. Provide Feedback
```
- Be specific
- Explain why
- Suggest alternatives
- Distinguish blocking vs nice-to-have
```

---

## Comment Format

### Blocking (Must Fix)
```markdown
**[Blocking]** Missing auth check

This endpoint can be called by any user, but it modifies data belonging to a specific user. Need to verify the current user matches.

```typescript
// Add at the start of the function
if (session.user.id !== userId) {
  throw new Error('Unauthorized')
}
```
```

### Important (Should Fix)
```markdown
**[Important]** N+1 query

This will make a separate query for each user. Consider using `include` to fetch in one query.

```typescript
const orders = await prisma.order.findMany({
  include: { user: true }
})
```
```

### Suggestion (Optional)
```markdown
**[Suggestion]** Could simplify with early return

Optional, but this might be clearer:

```typescript
if (!user) return null

return processUser(user)
```
```

### Question
```markdown
**[Question]** Why is this check needed?

I'm not sure I understand this condition. Could you explain the scenario where `items` would be undefined at this point?
```

### Praise
```markdown
Nice approach to the caching here! The invalidation logic is really clean.
```

---

## Response to Review

When receiving feedback:

1. **Don't be defensive**
2. **Ask for clarification** if unclear
3. **Fix blocking issues** first
4. **Discuss** disagreements professionally
5. **Thank** the reviewer

See: `~/.claude/skills/workflow/receiving-review.md`

---

## Common Issues

### Security
```typescript
// BAD: No auth
export async function deleteUser(id: string) {
  await prisma.user.delete({ where: { id } })
}

// GOOD: With auth
export async function deleteUser(id: string) {
  const session = await auth()
  if (!session) throw new Error('Unauthorized')
  if (session.user.id !== id && session.user.role !== 'admin') {
    throw new Error('Forbidden')
  }
  await prisma.user.delete({ where: { id } })
}
```

### Performance
```typescript
// BAD: N+1
const users = await prisma.user.findMany()
for (const user of users) {
  const orders = await prisma.order.findMany({ where: { userId: user.id } })
}

// GOOD: Single query
const users = await prisma.user.findMany({
  include: { orders: true }
})
```

### Maintainability
```typescript
// BAD: Magic numbers
if (score > 85) { ... }

// GOOD: Named constant
const PASSING_SCORE = 85
if (score > PASSING_SCORE) { ... }
```

---

## Approval Criteria

Approve when:
- [ ] No blocking issues
- [ ] Code is correct
- [ ] Tests pass
- [ ] Security reviewed
- [ ] Maintainable
