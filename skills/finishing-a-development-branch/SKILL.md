---
name: finishing-a-development-branch
description: "Development branch finalization workflow. Use when: all tasks on a branch are complete, the user wants to merge or open a PR, ready to ship. Keywords: finalize branch, merge, pull request, PR, ship, branch complete, done, completed, finish feature, close branch."
model: sonnet
allowed-tools: Read, Bash, Glob, Grep
metadata:
  author: osforge
  version: '1.0'
  source: obra/superpowers (MIT)
  adapted_by: osforge
---

## Branch state
!`git log --oneline -5 2>/dev/null || echo "Git not available"`
!`git status --short 2>/dev/null | head -10 || echo "Status not available"`
!`git diff --stat main...HEAD 2>/dev/null | tail -3 || echo "Diff not available"`

# Finishing a Development Branch

## Role

Finalization agent. Verifies that the work is genuinely complete,
presents clear options to the user, and executes the chosen action
safely. Focused on not shipping broken code and not losing work.

Inspired by the `finishing-a-development-branch` pattern from obra/superpowers.

---

## Process

### 1. Pre-finalization checks

Before any action, verify:

```bash
# Tests passing?
bun test 2>&1 | tail -20

# TypeScript clean?
bun tsc --noEmit 2>&1

# Lint clean?
bun lint 2>&1 | tail -10

# No uncommitted files?
git status --short

# No conflicts?
git diff --check
```

**If any check fails:** stop, report the problem to the user, do not proceed.

### 2. Work summary

Present a summary of what was done on the branch:

```markdown
## Branch Summary: {branch-name}

**Commits:** {N} commits
**Files modified:** {N} files
**Main changes:**
- {file}: {what changed}
- {file}: {what changed}

**Tests:** {N} passing / {N} failing
**TypeScript:** clean ✅ / {N} errors ❌
```

### 3. Present options

```markdown
## What do you want to do?

**[M] Direct merge** — merges to main now
   Ideal when: solo work, small branch, CI passes

**[P] Open Pull Request** — opens a PR for review before merge
   Ideal when: team work, significant changes, want review

**[K] Keep branch** — keep the branch open without merging
   Ideal when: incomplete work, want to continue later

**[D] Discard branch** — discard all the work
   Ideal when: wrong approach, want to start over
   ⚠️  IRREVERSIBLE — confirm explicitly
```

Wait for an explicit choice from the user.

### 4. Execute the chosen action

**[M] Direct merge:**
```bash
git checkout main
git merge {branch} --no-ff -m "feat: {feature description}"
git push origin main
git branch -d {branch}
```

**[P] Pull Request:**
```bash
git push origin {branch}

# Check whether the gh CLI is installed and authenticated before creating the PR
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  gh pr create --title "{title}" --body "{description}" --base main
else
  # Fallback: gh not available — build a PR creation URL for the user
  remote_url=$(git remote get-url origin | sed -e 's/\.git$//' -e 's#git@github\.com:#https://github.com/#')
  echo "gh CLI not installed/authenticated. Open manually:"
  echo "${remote_url}/compare/main...{branch}?expand=1"
fi
```

**[K] Keep branch:**
```bash
git push origin {branch}
echo "Branch kept at origin/{branch}"
```

**[D] Discard branch:**
```bash
# MANDATORY CHECKPOINT before discard
echo "WARNING: This will delete all the work on branch {branch}."
echo "Type 'confirm discard' to proceed:"
# Wait for explicit confirmation
git checkout main
git branch -D {branch}
```

### 5. Update STATUS.md

After merge or PR:
```bash
# Mark the feature as complete in .osforge/status.yaml
# Archive specs in .osforge/archive/
```

---

## Gotchas

- **Not checking tests before merging**: a merge with failing tests breaks main for the whole team. The pre-finalization check is mandatory, not optional.
- **Discard without a checkpoint**: discarding a branch is irreversible. Always confirm with the user explicitly before running `git branch -D`.
- **Merge without --no-ff on feature branches**: `--no-ff` preserves the branch's history in the commit graph. Without it, feature commits appear as a direct part of main, making rollback and bisect harder.
- **Not archiving specs**: specs of completed features should go to `.osforge/archive/` after merge. Without archiving, `.osforge/` accumulates specs of old features with no state distinction.
- **PR without a description**: PRs without a description reach the reviewer with no context. Always include: what changed, why it changed, how to test.
