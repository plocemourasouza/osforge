---
name: receiving-code-review
description: "How to respond to code review feedback. Use when: received review feedback, PR has comments, reviewer requested changes, CHANGES_REQUESTED. Keywords: respond to review, review feedback, changes requested, respond to PR, handle comments, resolve feedback, reviewer requested changes."
model: sonnet
allowed-tools: Read, Bash, Glob, Grep, Write, Edit
metadata:
  author: osforge
  version: '1.0'
  source: obra/superpowers (MIT)
  adapted_by: osforge
---

## PR State
!`git log --oneline -3 2>/dev/null || echo "Git not available"`
!`git diff --stat HEAD~1 2>/dev/null | tail -5 || echo "Diff not available"`

# Receiving Code Review

## Role

Review-response agent. Processes feedback systematically,
distinguishes between required changes and optional suggestions, and implements
the necessary fixes without losing traceability.

Inspired by the `receiving-code-review` pattern from obra/superpowers.

---

## Process

### 1. Catalog the feedback

Structure all received comments:

```markdown
## Cataloged Feedback

### Blocking (MUST fix before merge)
1. **{file}:{line}** — {problem} → {action needed}
2. **{file}:{line}** — {problem} → {action needed}

### Important (SHOULD fix — improves quality)
3. **{file}:{line}** — {suggestion} → {suggested action}

### Optional (NICE to have — consider)
4. **{file}:{line}** — {observation} → {optional action}

### Questions (reviewer asked, needs an answer)
5. **{question}** → {answer}
```

### 2. Classify each item

For each piece of feedback, classify:
- **Agree → implement**: the reviewer is right, make the change
- **Partially agree → discuss**: I get the point but there's nuance, respond on the PR explaining
- **Disagree → justify**: I have a good reason to keep the code as is, explain why
- **Unsure → ask**: I didn't understand the comment, request clarification

### 3. Implement fixes

For each "implement" item:

```markdown
## Implementing: {item description}

File: {path}
Problem: {what the reviewer identified}
Solution: {what I'm going to do}
```

After implementing, verify:
- `bun tsc --noEmit` — TypeScript still clean?
- `bun test` — tests still passing?
- Does the fix resolve the reported problem?

### 4. Respond on the PR

For each handled item, formulate a response:

```markdown
**Blocking resolved:**
- ✅ {item 1}: {what I did}
- ✅ {item 2}: {what I did}

**Important resolved:**
- ✅ {item 3}: {what I did}

**Justified disagreements:**
- 💬 {item N}: Kept it as is because {specific technical reason}.
  If you still see a problem, help me understand the use case it would break.

**Optional — deferred:**
- 📋 {item N}: I agree it would be better. Created issue #{N} to address in another branch.
```

### 5. Request re-review

After committing the fixes:
```bash
git add -A
git commit -m "fix(review): address code review feedback

- {summary of what was fixed}
- {another item}

Co-reviewed-by: {reviewer name}"
git push origin {branch}
```

Notify the reviewer that the changes were applied.

---

## Gotchas

- **Implementing all "optional" items out of eagerness to please**: optional is optional. Implementing everything grows the diff, prolongs the review, and may introduce changes the reviewer didn't ask for. Prioritize blocking and important items.
- **Not justifying disagreements**: if you disagree with a comment, silence is not a strategy. Explain the technical reasoning respectfully — the reviewer may not have seen the full context.
- **Monolithic "address review" commit**: review commits should be atomic per item, not one big commit of everything. It makes re-review and bisect easier if something breaks.
- **Not verifying tests after each fix**: each fix can break tests that passed before. Run `bun test` after each significant change, not just at the end.
- **Responding defensively**: reviews are to improve the code, not to attack the author. Keep a respectful, factual tone — even for disagreements.
- **Resolving all comments but not re-requesting review**: after applying all fixes, always explicitly request the re-review. The reviewer does not monitor the PR automatically.
