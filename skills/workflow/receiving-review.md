# Receiving Code Review

**Trigger:** responder review, feedback de review, changes requested, responder PR

---

## Purpose

Resposta estruturada a feedback de code review. Cataloga, classifica, implementa e responde formalmente.

---

## Process

### 1. Catalog Feedback

Organize items by priority:

| Priority | Description |
|----------|-------------|
| **Blocker** | Must fix before merge (security, correctness) |
| **Important** | Should fix (quality, maintainability) |
| **Optional** | Nice to have (style, preference) |

### 2. Classify Each Item

For each piece of feedback:

| Classification | Meaning | Action |
|----------------|---------|--------|
| **Agree** | Feedback is correct | Fix it |
| **Agree Partially** | Partly correct | Fix what makes sense, discuss rest |
| **Disagree** | Feedback is incorrect | Explain why respectfully |

### 3. Implement Fixes

```bash
# Atomic commits per item
git commit -m "fix(pr): address review - item 1: fix auth check"
git commit -m "fix(pr): address review - item 2: add error handling"
```

### 4. Verify Each Fix

For each change:
```
- [ ] Tests pass
- [ ] TypeScript compiles
- [ ] Fix addresses the feedback
```

### 5. Respond to Reviewer

```markdown
## Review Response

Thanks for the review! Here's my response to each item:

### Blockers
1. **[Item description]**
   - Status: Fixed
   - Commit: abc1234
   - Notes: [any context]

### Important
2. **[Item description]**
   - Status: Fixed
   - Commit: def5678

3. **[Item description]**
   - Status: Partially addressed
   - Notes: [explanation of what was done and why]

### Optional
4. **[Item description]**
   - Status: Deferred
   - Notes: Added to backlog for future cleanup

### Discussion
5. **[Item description]**
   - My perspective: [explanation]
   - Happy to discuss further

---

Ready for re-review. All blockers and important items addressed.
```

---

## Disagreement Template

When you disagree with feedback:

```markdown
I see your point about [feedback]. Here's my thinking:

**Current approach:** [what you did]
**Your suggestion:** [what they suggested]
**Trade-offs:**
- [Pro of current approach]
- [Con of suggested approach]

I'm open to changing this if you feel strongly, but wanted to share my reasoning. What do you think?
```

---

## Common Responses

### Security Concern
```markdown
Good catch! Fixed in commit abc123. I also added a test to prevent regression.
```

### Style Preference
```markdown
Fair point. I've updated to match the codebase convention.
```

### Disagree (Respectfully)
```markdown
I considered that approach, but chose this because [reason]. The trade-off is [X]. Happy to discuss if you see issues I'm missing.
```

### Need Clarification
```markdown
Could you clarify what you mean by [X]? I want to make sure I address your concern correctly.
```

---

## Request Re-Review

After addressing feedback:

```bash
# Push fixes
git push

# Request re-review via GitHub
gh pr review --request @reviewer-username

# Or comment
gh pr comment --body "Addressed all feedback. Ready for re-review. See response above."
```

---

## Anti-Patterns

### Don't
- Get defensive
- Ignore feedback without explanation
- Make excuses
- Rush fixes without testing
- Batch all fixes in one commit

### Do
- Thank the reviewer
- Be specific in responses
- Commit fixes atomically
- Verify each fix
- Ask questions if unclear
