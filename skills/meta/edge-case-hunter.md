# Edge Case Hunter

**Trigger:** "edge cases", "boundary conditions", "what can go wrong?", or invoked automatically by code-review and adversarial-review.

---

## Purpose

Exhaustive hunt for edge cases through systematic path enumeration. Method-driven, not attitude-driven (orthogonal to adversarial-review).

**Reports ONLY paths without adequate handling.**

---

## Categories

### 1. Null/Undefined
```typescript
// Check for:
- Optional parameters
- Database query results
- API response fields
- Array element access
- Object property access
```

### 2. Empty Values
```typescript
// Check for:
- Empty strings ""
- Empty arrays []
- Empty objects {}
- Zero values 0
- Whitespace-only strings "   "
```

### 3. Boundary Values
```typescript
// Check for:
- Min/max integers
- Array length limits
- String length limits
- Date boundaries (year 9999, 1970)
- Negative numbers where positive expected
```

### 4. Concurrent Access
```typescript
// Check for:
- Race conditions
- Double-click submit
- Parallel requests
- Stale data
- Optimistic update conflicts
```

### 5. Timing Issues
```typescript
// Check for:
- Request timeouts
- Session expiration mid-action
- Token refresh during request
- Slow network conditions
- Clock skew
```

### 6. Encoding Problems
```typescript
// Check for:
- Unicode characters
- Emoji in text fields
- RTL text
- Special characters (<>&"')
- Non-ASCII filenames
```

### 7. Overflow
```typescript
// Check for:
- Integer overflow
- Array size limits
- String length limits
- File size limits
- Pagination beyond data
```

### 8. Auth Bypass
```typescript
// Check for:
- Direct object access
- Missing ownership check
- Role escalation
- Session fixation
- Token reuse after logout
```

### 9. State Transitions
```typescript
// Check for:
- Invalid state transitions
- Partial state updates
- State corruption
- Undo/redo edge cases
- Back button behavior
```

---

## Enumeration Process

```
For each function/endpoint:

1. List all parameters
   └── For each parameter, enumerate edge cases

2. List all return paths
   └── For each path, check handling

3. List all external calls
   └── For each call, enumerate failure modes

4. List all state mutations
   └── For each mutation, check consistency
```

---

## Output Format

```markdown
## Edge Cases: [Function/Endpoint]

### Unhandled

**[Category] Description**
- Path: `function.ts:45`
- Input: `{ userId: null }`
- Expected: Error or default
- Actual: Crashes

### Handled (verification)

**[Category] Description**
- Path: `function.ts:48`
- Handling: Returns empty array
```

---

## Example

```typescript
// Function to analyze
async function getOrders(userId: string, page: number) {
  const orders = await prisma.order.findMany({
    where: { userId },
    skip: page * 20,
    take: 20,
  })
  return orders
}

// Edge cases found:
// [Null] userId is undefined → crashes
// [Boundary] page < 0 → negative skip
// [Boundary] page > total pages → empty but no indicator
// [Empty] user has no orders → works, returns []
```
