---
name: git-workflow
description: >
  Git workflow patterns for AI agent development: worktrees for parallel agents,
  branching strategy, commit discipline, and merge workflows.
  Use when creating branches, setting up parallel work, managing merges,
  resolving conflicts, or structuring git operations for agent-driven development.
  Triggers on: git workflow, create branch, parallel features, worktree,
  merge strategy, git setup, branching, git conflict.
metadata:
  author: paulo-cursor-setup
  version: "1.0.0"
---

# Git Workflow for Agent-Driven Development

## Branching Strategy

### Branch Naming (Conventional)
```
feature/short-description
bugfix/bug-description
hotfix/critical-fix
chore/maintenance
refactor/refactored-area
```

### Basic Workflow
1. Always create the branch from `main` (or `develop` if the project uses it)
2. Small, frequent commits (1 logical change per commit)
3. Conventional Commits required (see the commit-conventions rule)
4. PR with squash merge to main
5. Delete the branch after merge

## Git Worktrees — Parallelism for Agents

### When to Use Worktrees
- Multiple independent features need to be implemented
- Parallel agents working simultaneously
- Features that touch different files (no conflict)

### When NOT to Use Worktrees
- Features that depend on each other (one needs the other)
- A single feature that touches many files
- Sequential work (one feature at a time)

### Why Worktrees > Branches for Agents
Branches share the same working directory. If two agents try to
work on different branches of the same repo, they step on each
other's files. Worktrees create separate directories, each with its
own isolated working directory.

### Worktree Setup

```bash
# 1. From the main repo, create worktrees
git worktree add ../project-feature-auth feature/auth
git worktree add ../project-feature-dashboard feature/dashboard
git worktree add ../project-feature-api feature/api

# 2. Check active worktrees
git worktree list

# 3. Each agent works in its own directory
# Agent 1 → ../project-feature-auth/
# Agent 2 → ../project-feature-dashboard/
# Agent 3 → ../project-feature-api/

# 4. After implementation, sequential merge
cd /path/to/main-repo
git merge feature/auth
git merge feature/dashboard
git merge feature/api

# 5. Cleanup
git worktree remove ../project-feature-auth
git worktree remove ../project-feature-dashboard
git worktree remove ../project-feature-api
```

### Rules for Worktrees with Agents
- ALWAYS commit in the worktree before attempting a merge
- NEVER delete the worktree without merging or confirming abandonment
- Each worktree must have its own `node_modules` (run `npm install`)
- Resolve merge conflicts one at a time, from simplest to most complex
- After merging all of them, run the full test suite on the main branch

## Commit Discipline for Agents

### Commit Structure
```
type(scope): short description

- Detail 1
- Detail 2

Refs: #issue-number (if applicable)
```

### Frequency
- Commit after each complete logical unit of work
- NEVER pile multiple features into a single commit
- If the agent implemented something that works, commit it immediately

### Pre-Commit Checklist
Before each commit, verify:
1. `npx tsc --noEmit` passes (TypeScript)
2. `npm run lint` passes (ESLint)
3. No debug `console.log`
4. No `.env` file or secret in staging
5. Relevant tests pass

The `scan-secrets.sh` hook performs an automatic secret check before the commit.

## Merge & Conflict Resolution

### Merge Strategy
- **Feature → main**: Squash merge (clean history)
- **Hotfix → main**: Regular merge (preserves the fix's context)
- **Worktree merges**: Regular merge (preserves individual commits)

### Conflict Resolution
1. Identify the conflicting files: `git diff --name-only --diff-filter=U`
2. For each file, understand the intent of BOTH sides
3. Resolve while preserving the functionality of both features
4. Run tests after resolving each file
5. Commit the merge with a descriptive message

### Anti-patterns
- NEVER use `git merge --strategy=ours` without review (discards work)
- NEVER force push to shared branches
- NEVER resolve conflicts by blindly picking one side
- NEVER merge without running tests first

## Integration with Other Skills and Rules
- **commit-conventions rule**: Commit format is enforced globally
- **tdd-enforcement rule**: Tests are protected during implementation
- **scan-secrets hook**: Checks for secrets before git commit/push
- **validator agent**: Validate against the spec before creating a PR
- **tlc-spec-driven**: Use STATE.md for cross-session tracking
