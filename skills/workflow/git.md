# Git Workflow

**Trigger:** branch, commit, worktree, merge, git, version control

---

## Branch Naming

```
feature/   → New features
bugfix/    → Bug fixes
hotfix/    → Production urgent fixes
chore/     → Maintenance tasks
refactor/  → Code restructuring
```

Examples:
- `feature/user-authentication`
- `bugfix/login-redirect-loop`
- `hotfix/payment-calculation`

---

## Conventional Commits (Mandatory)

### Format
```
type(scope): description
```

- Max 72 characters
- Lowercase
- No period at end

### Types
| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring (no behavior change) |
| `docs` | Documentation only |
| `style` | Formatting (no code change) |
| `test` | Adding/fixing tests |
| `chore` | Build, deps, tooling |
| `perf` | Performance improvement |
| `ci` | CI/CD changes |

### Breaking Changes
```bash
feat!: remove deprecated API endpoints

# Or with footer
feat(api): change response format

BREAKING CHANGE: Response now returns array instead of object
```

### Examples
```bash
feat(auth): add OAuth2 login with Google
fix(cart): prevent negative quantity input
refactor(api): extract validation middleware
docs(readme): add deployment instructions
test(user): add unit tests for password reset
```

---

## Git Worktrees for Parallel Agents

When multiple independent features need parallel implementation:

```bash
# Create worktrees
git worktree add ../project-feature-auth feature/auth
git worktree add ../project-feature-dashboard feature/dashboard

# Each agent works in its own isolated directory
# After completion: merge sequentially, resolve conflicts, test

# Clean up
git worktree remove ../project-feature-auth
git worktree remove ../project-feature-dashboard

# List worktrees
git worktree list

# Prune stale entries
git worktree prune
```

### Why Worktrees Instead of Branches
Branches share the working directory → conflicts when parallel agents edit files.
Worktrees give each agent an isolated directory → no conflicts during work.

### Setup Per Worktree
```bash
cd ../project-feature-auth
cp ../.env .env           # Copy env
bun install               # Fresh node_modules
PORT=3001 bun dev         # Different port
```

---

## Pre-Commit Checklist

Before committing:
1. `tsc --noEmit` passes
2. `lint` passes
3. No `console.log` debug statements
4. No secrets in staging
5. Tests pass (if changed)

```bash
# Quick check
bun run lint && bun tsc --noEmit && bun test
```

---

## Common Operations

### Interactive Staging (avoid -i flag)
```bash
# Stage specific files
git add src/auth.ts src/api/login.ts

# Stage hunks manually
git add -p  # NOT -i (interactive mode not supported)
```

### Stash
```bash
git stash                    # Save changes
git stash pop                # Restore and remove
git stash list               # List stashes
git stash drop stash@{0}     # Remove specific
```

### Undo
```bash
git checkout -- file.ts      # Discard changes in file
git reset HEAD file.ts       # Unstage file
git reset --soft HEAD~1      # Undo commit, keep changes staged
git reset --hard HEAD~1      # Undo commit, discard changes (DANGEROUS)
```

### Rebase
```bash
git fetch origin
git rebase origin/main       # Rebase onto main
# If conflicts: fix → git add → git rebase --continue
```

---

## Branch Protection

Never force push to:
- `main`
- `master`
- `production`

```bash
# DANGEROUS - requires explicit confirmation
git push --force  # NEVER on protected branches
```
