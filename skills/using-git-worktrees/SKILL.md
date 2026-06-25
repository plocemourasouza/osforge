---
name: using-git-worktrees
description: "Setup and use of git worktrees for parallel development. Use when: working on multiple features simultaneously, needing isolated branches for each parallel agent, testing a hotfix without interrupting feature development. Keywords: git worktree, worktrees, parallel development, multiple branches, isolated workspace, parallel branch."
model: sonnet
allowed-tools: Read, Bash, Glob
metadata:
  author: osforge
  version: '1.0'
  source: obra/superpowers (MIT)
  adapted_by: osforge
---

## Current worktree state
!`git worktree list 2>/dev/null || echo "Git worktrees unavailable or repository not initialized"`
!`git branch -a 2>/dev/null | head -10 || echo "Branches unavailable"`

# Using Git Worktrees

## What are worktrees?

Git worktrees let you have multiple checkouts of the same repository in
different directories, each on a different branch. Ideal for:

- Parallel agents working on independent features at the same time
- Testing a hotfix without committing/stashing work in progress
- Code review of one branch while implementing another

---

## Initial setup

### Create a worktree for a new feature

```bash
# Create branch + worktree in one step
git worktree add ../my-project-feature-A feature/feature-A

# Or create from an existing branch
git worktree add ../my-project-hotfix hotfix/bug-123

# Check active worktrees
git worktree list
```

The `../my-project-feature-A` directory is completely isolated — changes there do not affect the main directory.

> ⚠️ **WARNING: a branch checked out in one worktree CANNOT be used in another.** Git blocks `git checkout`/`git worktree add` of a branch that is already active in any other worktree (error: `fatal: '<branch>' is already checked out at '<path>'`). Plan an exclusive branch per worktree; if you need the branch elsewhere, remove the worktree using it first.

### Recommended structure for OSForge + parallel agents

```
/Users/paulosouza/Development/
├── my-project/                ← main (primary worktree)
├── my-project-feature-A/      ← worktree for Agent 1
├── my-project-feature-B/      ← worktree for Agent 2
└── my-project-hotfix/         ← worktree for an urgent hotfix
```

---

## Flow with dispatching-parallel-agents

When `dispatching-parallel-agents` identifies parallel tasks:

```bash
# 1. Create one worktree per parallel task
git worktree add ../project-task-api feature/task-api
git worktree add ../project-task-ui feature/task-ui
git worktree add ../project-task-tests feature/task-tests

# 2. Each agent works in its isolated directory
# Agent 1: cd ../project-task-api && implement
# Agent 2: cd ../project-task-ui && implement
# Agent 3: cd ../project-task-tests && implement

# 3. After completion, merge each branch
git checkout main
git merge feature/task-api --no-ff
git merge feature/task-ui --no-ff
git merge feature/task-tests --no-ff

# 4. Clean up worktrees
git worktree remove ../project-task-api
git worktree remove ../project-task-ui
git worktree remove ../project-task-tests
```

---

## Essential commands

```bash
# List all worktrees
git worktree list

# Create worktree + new branch
git worktree add <path> <new-branch>

# Create worktree on an existing branch
git worktree add <path> <existing-branch>

# Remove worktree (after merge)
git worktree remove <path>

# Force removal (if path no longer exists)
git worktree prune

# Move worktree to another directory
git worktree move <current-path> <new-path>
```

---

## Setup in each worktree

Each worktree is a complete project directory but shares the `.git` with the main one. What is NOT shared:

- `node_modules/` — run `bun install` in each worktree
- `.env` — copy or create `.env.local` in each worktree
- Running processes (dev server, etc.)

```bash
# In each new worktree:
cd ../my-project-feature-A
bun install                    # install dependencies
cp ../my-project/.env.local .  # copy environment variables
bun dev --port 3001            # different port to avoid conflicts
```

---

## Gotchas

- **Using the same port in multiple worktrees**: each `bun dev` needs a different port (`--port 3001`, `--port 3002`, etc). Conflicting ports cause a startup error.
- **Forgetting to run `bun install` in the new worktree**: `node_modules` is not shared. Without installing, imports fail with confusing errors.
- **Leaving orphaned worktrees**: unremoved worktrees accumulate space and clutter `git worktree list`. Always remove after merge with `git worktree remove`.
- **Checking out a branch in use by another worktree**: git does not allow it. If Agent 1 is using `feature/A`, you cannot run `git checkout feature/A` in the main worktree. Solution: create a new worktree or remove the existing one.
- **Modifying `.git/config` in a worktree**: worktrees share the git configuration. Changes to `.git/config` in one worktree affect all of them. Use `.git/config.worktree` for worktree-local configuration.
- **Not running `git worktree prune` after deleting a directory manually**: if the worktree directory was deleted without `git worktree remove`, git keeps the dead reference. Run `git worktree prune` to clean it up.
