---
name: tdd-workflow
description: Enforces Test-Driven Development (RED-GREEN-REFACTOR) workflow. Use when implementing any feature, bugfix, or behavior change. Ensures tests are written before implementation code, watches them fail, then writes minimal code to pass. Triggers on tasks involving new features, bug fixes, refactoring, or when the user mentions TDD, tests first, or red-green-refactor.
---

# Test-Driven Development (TDD)

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

## When NOT to Use TDD

TDD applies to behavior and logic. Skip it (without guilt) for:
- **UI prototypes / throwaway spikes** — exploratory code meant to be deleted; testing it first wastes the exploration
- **Pure styling changes** — CSS/Tailwind tweaks, spacing, colors, typography with zero logic
- **Static content** — copy changes, markdown, layout-only markup
- **Config files** — next.config, biome.json, tsconfig
- **Generated code** — Prisma Client, shadcn components

If the change has any conditional logic, data transformation, or user-facing behavior — TDD applies. When in doubt, it applies.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before the test? **Delete it. Start over.**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

## RED-GREEN-REFACTOR Cycle

### 1. RED — Write the Failing Test
- Write ONE test for the smallest behavior increment
- Run it. Confirm it **fails for the expected reason**
- If it passes without implementation → test is wrong, fix the test

### 2. GREEN — Make It Pass
- Write the **minimum** code to make the test pass
- No future-proofing, no "while I'm here" additions
- Run the test. Confirm it passes.

### 3. REFACTOR — Clean Up
- Improve code quality while keeping tests green
- Extract functions, rename variables, remove duplication
- Run tests after each change. Still green? Continue.

### 4. COMMIT
- Commit after each complete RED-GREEN-REFACTOR cycle
- Message format: `test: add test for X` → `feat: implement X`

## Cycle Size Guide

| Too Big | Right Size | Too Small |
|---------|-----------|-----------|
| "User authentication system" | "Login returns JWT on valid credentials" | "Function exists" |
| "CRUD for entity" | "Create returns 201 with new entity" | "Variable is defined" |
| "Payment flow" | "Charge fails with invalid card number" | "Function is callable" |

## Exceptions (Ask Before Skipping)

- Throwaway prototypes explicitly labeled as such
- Generated code (Prisma Client, shadcn components)
- Configuration files (next.config, biome.json)
- Pure UI styling changes with no logic

If thinking "skip TDD just this once" → **Stop. That's rationalization. Follow the process.**

## Stack-Specific Patterns

### Vitest (Unit/Integration)
```typescript
// Write test FIRST
describe('PaymentService', () => {
  it('should reject expired cards', async () => {
    const result = await service.charge({ cardExp: '01/20', amount: 100 })
    expect(result.success).toBe(false)
    expect(result.error).toBe('CARD_EXPIRED')
  })
})
// Then implement PaymentService.charge()
```

### Playwright (E2E)
```typescript
// Write the user journey test FIRST
test('user can complete checkout', async ({ page }) => {
  await page.goto('/cart')
  await page.getByRole('button', { name: 'Checkout' }).click()
  await expect(page.getByText('Order confirmed')).toBeVisible()
})
// Then implement the checkout flow
```

### Server Actions
```typescript
// Write test FIRST for the action behavior
it('should validate input and return errors', async () => {
  const result = await createUser({}, new FormData())
  expect(result.success).toBe(false)
  expect(result.errors).toBeDefined()
})
```
