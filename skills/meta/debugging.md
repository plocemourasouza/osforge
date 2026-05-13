# Systematic Debugging

**Trigger:** debug methodology, root cause analysis, systematic troubleshooting

---

## 4-Phase Methodology

### Phase 1: Reproduce
**Goal:** Reliably trigger the bug

```
1. Get exact reproduction steps
2. Identify required conditions:
   - User state (logged in, specific role?)
   - Data state (specific records?)
   - Environment (browser, OS, network?)
3. Write a failing test if possible
4. Document: "Bug occurs when X under conditions Y"
```

**Questions:**
- Can I reproduce it?
- Does it happen every time or intermittently?
- What's the simplest reproduction?

### Phase 2: Isolate
**Goal:** Narrow down the problem location

```
1. Binary search the codebase:
   - Comment out half the code
   - Does it still fail?
   - Narrow down which half
2. Check recent changes:
   - git log --oneline -20
   - git bisect to find breaking commit
3. Isolate variables:
   - Same data, different code path?
   - Same code, different data?
```

**Techniques:**
```typescript
// Add debug points
console.log('Checkpoint A reached')
console.log('State at B:', JSON.stringify(state, null, 2))

// Simplify inputs
// Instead of complex real data, use minimal test data

// Bypass suspected areas
// Temporarily hardcode values to skip sections
```

### Phase 3: Understand
**Goal:** Comprehend why the bug occurs

```
1. Read the code path carefully
2. Check assumptions:
   - What should this value be?
   - What is it actually?
3. Trace data flow:
   - Where does this value come from?
   - What transforms it along the way?
4. Check edge cases:
   - null/undefined?
   - Empty arrays/objects?
   - Boundary values?
```

**Common Root Causes:**
- Race condition
- Stale closure
- Missing null check
- Wrong variable type
- Incorrect assumption about API
- Off-by-one error
- State mutation

### Phase 4: Fix
**Goal:** Correct the issue without breaking other things

```
1. Write a test that fails (captures the bug)
2. Make the smallest fix possible
3. Run the test - does it pass?
4. Run all tests - any regressions?
5. Review the fix:
   - Does it address root cause?
   - Any similar bugs elsewhere?
6. Document the fix
```

---

## Debugging Tools

### Browser DevTools
```
Console:
- console.log(), console.table(), console.trace()
- debugger; // Breakpoint in code

Network:
- Check request/response
- Look for failed requests
- Check timing

Sources:
- Set breakpoints
- Step through code
- Watch expressions
```

### Node.js/Bun
```bash
# Node inspector
node --inspect src/index.ts

# Bun debugger
bun --inspect src/index.ts

# Then open chrome://inspect
```

### React DevTools
```
Components tab:
- Inspect component tree
- Check props and state
- Find re-render causes

Profiler tab:
- Record render timing
- Find performance issues
```

---

## Common Patterns

### Async/Race Condition
```typescript
// Bug: Data shows stale value
// Check: Is there a race condition?

// Fix: Cancel previous request
useEffect(() => {
  const controller = new AbortController()

  fetch(url, { signal: controller.signal })
    .then(setData)
    .catch(err => {
      if (err.name !== 'AbortError') throw err
    })

  return () => controller.abort()
}, [url])
```

### Stale Closure
```typescript
// Bug: Callback uses old state value
// Check: Is state captured at creation time?

// Fix: Use functional update or ref
setItems(prev => [...prev, newItem])

// Or
const itemsRef = useRef(items)
useEffect(() => { itemsRef.current = items }, [items])
```

### Null/Undefined
```typescript
// Bug: "Cannot read property X of undefined"
// Check: What's undefined? Why?

// Fix: Add defensive checks
const value = data?.nested?.value ?? defaultValue
```

---

## Investigation Template

```markdown
## Bug Investigation: [Title]

### Symptoms
- What happens: [description]
- Expected: [what should happen]
- Frequency: [always / intermittent]

### Reproduction
1. [Step 1]
2. [Step 2]
3. [Bug occurs]

**Environment:**
- Browser: [Chrome 120]
- OS: [macOS 14.2]
- User state: [logged in as admin]

### Investigation Log
- [timestamp] Checked X, found Y
- [timestamp] Narrowed to file Z
- [timestamp] Root cause: [description]

### Root Cause
[Explanation of why the bug occurs]

### Fix
[Description of the fix]

### Verification
- [ ] Bug no longer reproduces
- [ ] New test added
- [ ] All tests pass
- [ ] No regressions

### Prevention
[How to prevent similar bugs]
```

---

## Anti-Patterns

### Don't
- Random changes hoping something works
- Fixing symptoms instead of root cause
- Skipping reproduction ("I think I know what it is")
- Not writing a test for the bug

### Do
- Methodical, evidence-based investigation
- Understand before fixing
- Verify fix with test
- Document for future reference
