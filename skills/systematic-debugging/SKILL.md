---
name: systematic-debugging
description: "Systematic 4-phase debugging with root-cause analysis. Use when: a bug is hard to reproduce, a crash has no clear stacktrace, intermittent behavior, a regression with no obvious cause, deep root-cause investigation. Keywords: debug, bug, error, crash, fix, issue, not working, broken, regression, investigate."
model: sonnet
context: fork
agent: general-purpose
allowed-tools: Read, Bash, Glob, Grep
metadata:
  author: antigravity-kit (adapted)
  version: "1.1"
  source: "antigravity-kit"
---

# Systematic Debugging

> Source: obra/superpowers

## Overview
This skill provides a structured approach to debugging that prevents random guessing and ensures problems are properly understood before solving.

## 4-Phase Debugging Process

### Phase 1: Reproduce
Before fixing, reliably reproduce the issue.

```markdown
## Reproduction Steps
1. [Exact step to reproduce]
2. [Next step]
3. [Expected vs actual result]

## Reproduction Rate
- [ ] Always (100%)
- [ ] Often (50-90%)
- [ ] Sometimes (10-50%)
- [ ] Rare (<10%)
```

### Phase 2: Isolate
Narrow down the source.

```markdown
## Isolation Questions
- When did this start happening?
- What changed recently?
- Does it happen in all environments?
- Can we reproduce with minimal code?
- What's the smallest change that triggers it?
```

### Phase 3: Understand
Find the root cause, not just symptoms.

```markdown
## Root Cause Analysis
### The 5 Whys
1. Why: [First observation]
2. Why: [Deeper reason]
3. Why: [Still deeper]
4. Why: [Getting closer]
5. Why: [Root cause]
```

### Phase 4: Fix & Verify
Fix and verify it's truly fixed.

```markdown
## Fix Verification
- [ ] Bug no longer reproduces
- [ ] Related functionality still works
- [ ] No new issues introduced
- [ ] Test added to prevent regression
```

## Debugging Checklist

```markdown
## Before Starting
- [ ] Can reproduce consistently
- [ ] Have minimal reproduction case
- [ ] Understand expected behavior

## During Investigation
- [ ] Check recent changes (git log)
- [ ] Check logs for errors
- [ ] Add logging if needed
- [ ] Use debugger/breakpoints

## After Fix
- [ ] Root cause documented
- [ ] Fix verified
- [ ] Regression test added
- [ ] Similar code checked
```

## Common Debugging Commands

```bash
# Recent changes
git log --oneline -20
git diff HEAD~5

# Search for pattern
grep -r "errorPattern" --include="*.ts"

# Check logs
pm2 logs app-name --err --lines 100
```

## Anti-Patterns

❌ **Random changes** - "Maybe if I change this..."
❌ **Ignoring evidence** - "That can't be the cause"
❌ **Assuming** - "It must be X" without proof
❌ **Not reproducing first** - Fixing blindly
❌ **Stopping at symptoms** - Not finding root cause

---

## Gotchas

- **Starting to fix before reproducing**: the most common cause of a wrong fix. Always reproduce reliably before any change — if you can't reproduce it, you don't know what you're fixing.
- **Stopping at symptoms**: "the button doesn't work" is a symptom, not a cause. Always dig deeper with the 5 Whys until you reach a cause that makes mechanical sense. Stopping at the first plausible explanation is the most frequent mistake.
- **Not checking `git log` first**: most bugs have a temporal correlation with a recent change. `git log --oneline -20` should be the first action, not the last.
- **Multiple simultaneous changes**: when testing a hypothesis, make ONE change at a time. Multiple simultaneous changes make it impossible to identify what fixed the problem — or introduced another.
- **Assuming an identical environment**: different behaviors across dev/staging/prod usually indicate different environment variables, seed data, or dependency versions. Always verify with `node -e "require('./package.json').dependencies"` or equivalent.
- **Not adding a regression test**: after fixing, always add a test that fails without the fix and passes with it. Without it, the bug will come back in 3 months.
