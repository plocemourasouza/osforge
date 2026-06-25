---
name: predictive-failure
description: >
  Analyze implemented code to predict potential failure points that tests
  may not catch. Uses pattern matching against common production failure modes.
  Use after implementation is complete, when asked to predict failures,
  find hidden bugs, check what could go wrong, production readiness check,
  or pre-deploy analysis. Triggers on: predict failures, what could go wrong,
  hidden bugs, production readiness, pre-deploy check, failure analysis.
metadata:
  author: paulo-cursor-setup
  version: "1.0.0"
---

# Predictive Failure Analysis

After implementation and passing tests, this skill looks for failures that
traditional tests do NOT catch — using pattern matching against common
production failure modes.

## When to Use
- Tests pass but you want extra validation before deploy
- After implementing a complex feature
- Before a production release
- When asked: "what could go wrong?", "predict failures"

## Process

### 1. Scan the Implemented Code
Read all recently modified files (git diff or a list of files).
Identify: components, API routes, Server Actions, hooks, utils.

### 2. Analysis by Category

#### Race Conditions & Timing
- Concurrent requests to the same resource (e.g., double-click on a submit button)
- Out-of-order state updates in async operations
- Missing debounce/throttle on fast inputs (search, resize)
- useEffect with async dependencies without cleanup/abort controller
- Optimistic updates without rollback when the server fails

#### Data Edge Cases
- Strings with unicode/emojis in text fields (breaks length validation)
- Numbers at the float precision limit (0.1 + 0.2 !== 0.3)
- Empty arrays where at least 1 item is expected
- Null/undefined in nested objects (missing optional chaining)
- Dates in different timezones (UTC vs local)
- Monetary values with incorrect rounding

#### Network & Infra
- Unhandled API timeout (what happens after 30s?)
- Retry without exponential backoff (DDoS on your own backend)
- Stale cache after deploy (old version in the browser)
- CORS in production different from development
- WebSocket reconnection without backoff
- Missing rate limiting on public endpoints

#### State Management
- Memory leaks in useEffect without cleanup
- Stale closures in async callbacks with state
- Hydration mismatch (server vs client rendering differs)
- Local state that should be global (or vice versa)
- Form state lost on navigation (back button)

#### Security in Production
- CSRF in mutations (Server Actions are protected, Route Handlers are not)
- XSS in dynamic content rendered with dangerouslySetInnerHTML
- SQL injection in raw queries (Prisma parameterizes, but raw queries do not)
- Exposed stack traces in production error responses
- Tokens in URL parameters (appear in logs and referrer headers)

#### UX Under Stress
- List with 10,000+ items without virtualization
- Large file upload without a progress indicator
- Many tabs/windows open with the same auth state
- Slow 3G: what does the user see during loading?
- Accessibility: does it work without a mouse? without sight?

### Concrete Examples of Vulnerable Code

#### Missing AbortController in useEffect
```tsx
// ❌ Vulnerable: if the user navigates/changes the query before the response,
// setState runs on an unmounted component or with stale data (race condition)
useEffect(() => {
  fetch(`/api/search?q=${query}`)
    .then(res => res.json())
    .then(setResults)
}, [query])

// ✅ Fix: AbortController cancels the previous request in cleanup
useEffect(() => {
  const controller = new AbortController()
  fetch(`/api/search?q=${query}`, { signal: controller.signal })
    .then(res => res.json())
    .then(setResults)
    .catch(err => { if (err.name !== 'AbortError') throw err })
  return () => controller.abort()
}, [query])
```

#### Double-click on submit without debounce/guard
```tsx
// ❌ Vulnerable: double-click creates 2 orders/2 charges
<button onClick={() => createOrder(data)}>Complete purchase</button>

// ✅ Fix: disable during submit (state guard)
const [submitting, setSubmitting] = useState(false)
async function handleSubmit() {
  if (submitting) return
  setSubmitting(true)
  try { await createOrder(data) } finally { setSubmitting(false) }
}
<button onClick={handleSubmit} disabled={submitting}>Complete purchase</button>
```

### 3. Output

For each issue found, report:

| Field | Format |
|-------|---------|
| **Severity** | 🔴 Critical / 🟠 High / 🟡 Medium / 🔵 Low |
| **Probability** | Common / Occasional / Rare |
| **Category** | One of the 6 categories above |
| **Scenario** | How to reproduce in 1-2 sentences |
| **Impact** | What the user experiences |
| **File** | Location in the code |
| **Suggested fix** | Code or pattern to resolve it |

### 4. Prioritization

Order issues by: Severity × Probability
- 🔴 Critical + Common → BLOCKS deploy
- 🔴 Critical + Rare → Resolve before v1.0
- 🟠 High + Common → Resolve this sprint
- Others → Prioritized backlog

## Important
- Do NOT list theoretical problems — only issues with evidence in the code
- Point to the FILE and LINE where the problem exists
- The suggested fix must be implementable (not generic)
- If you find no issues, say so honestly — do not invent problems
