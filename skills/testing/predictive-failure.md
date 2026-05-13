# Predictive Failure Analysis

**Trigger:** predict failures, production readiness, pre-deploy, what could go wrong

---

## Purpose

Finds failures that tests DON'T catch — pattern matching against common production failure modes. Run after implementation + tests pass.

---

## Categories

### 1. Race Conditions
```
- Double-click submit (duplicate orders, payments)
- Async state out of order (stale data displayed)
- Missing debounce on search/autocomplete
- useEffect without cleanup/abort controller
- Concurrent API calls clobbering each other
```

**Detection:**
```typescript
// Look for: onClick without disable during async
// Look for: fetch without AbortController
// Look for: setState after component unmount potential
```

### 2. Data Edge Cases
```
- Unicode in text fields (emoji, RTL, special chars)
- Float precision (monetary calculations)
- Empty arrays treated as truthy
- Null in nested objects (optional chaining missing)
- Timezone mismatches (server vs client)
- Monetary rounding errors
- Integer overflow (rare but possible)
```

**Detection:**
```typescript
// Look for: price * quantity without proper decimal handling
// Look for: date comparisons without timezone normalization
// Look for: data?.nested?.value without fallback
```

### 3. Network Issues
```
- Unhandled timeouts
- Retry without exponential backoff
- Stale cache after deploy
- CORS differences prod vs dev
- Missing rate limiting
- Large payload handling
- Offline behavior
```

**Detection:**
```typescript
// Look for: fetch without timeout
// Look for: retry logic without backoff
// Look for: cache headers not set
```

### 4. State Management
```
- Memory leaks (useEffect no cleanup)
- Stale closures (referencing old state)
- Hydration mismatch (SSR vs client)
- Form state lost on back button
- Optimistic updates without rollback
```

**Detection:**
```typescript
// Look for: useEffect with subscriptions but no cleanup
// Look for: setInterval without clearInterval
// Look for: event listeners without removeEventListener
```

### 5. Security in Production
```
- CSRF on Route Handlers (Server Actions have it built-in)
- XSS via dangerouslySetInnerHTML
- Exposed stack traces in error responses
- Tokens in URL params (logged, cached)
- Missing auth checks on API routes
- Sensitive data in client state
```

**Detection:**
```typescript
// Look for: Route Handlers without CSRF protection
// Look for: dangerouslySetInnerHTML without sanitization
// Look for: error.message exposed to client
```

### 6. UX Under Stress
```
- 10k+ items without virtualization
- Large uploads without progress indicator
- Slow 3G experience (no loading states)
- Accessibility without mouse (keyboard nav)
- Long text breaking layout
- Missing empty states
```

**Detection:**
```typescript
// Look for: .map() on unbounded arrays without virtualization
// Look for: file upload without progress
// Look for: missing Skeleton/Loading components
```

---

## Analysis Process

### 1. Scan Code Patterns
```bash
# Find potential issues
grep -r "dangerouslySetInnerHTML" src/
grep -r "useEffect" src/ | grep -v "cleanup"
grep -r "fetch(" src/ | grep -v "AbortController"
```

### 2. Review Critical Paths
Focus on:
- Payment flows
- Authentication
- Data mutations
- User input handling

### 3. Check Error Handling
```typescript
// Every catch block should:
// 1. Log enough for debugging
// 2. Return safe error to user
// 3. Not expose internals
```

---

## Output Format

For each issue found:

```markdown
### 🔴 P0: Double Submit on Payment

**File:** `app/checkout/page.tsx:45`
**Category:** Race Condition
**Probability:** High

**Scenario:**
User double-clicks "Pay Now" button on slow connection.

**Impact:**
Duplicate payment charged to user.

**Evidence:**
```tsx
<button onClick={handlePayment}>Pay Now</button>
// No disable during async, no debounce
```

**Fix:**
```tsx
const [isProcessing, setIsProcessing] = useState(false)

<button
  onClick={handlePayment}
  disabled={isProcessing}
>
  {isProcessing ? 'Processing...' : 'Pay Now'}
</button>
```
```

---

## Severity Levels

| Level | Meaning | Examples |
|-------|---------|----------|
| 🔴 P0 | Critical | Security vuln, data loss, duplicate charges |
| 🟠 P1 | High | Major feature broken, bad UX for many |
| 🟡 P2 | Medium | Edge case failure, minor UX issue |
| 🔵 P3 | Low | Cosmetic, rare edge case |

---

## Rules

1. **Only report issues with evidence in actual code** — No theoretical problems
2. **Prioritize by impact × probability**
3. **Include specific file:line references**
4. **Provide actionable fix suggestions**
5. **Focus on production-specific failures** — Things tests typically miss
