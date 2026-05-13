# Finishing a Development Branch

**Trigger:** finalizar branch, merge, pull request, PR, ship, branch completa, done, concluído

---

## Purpose

Workflow de finalização de branch com verificação pré-merge e opções de conclusão.

---

## Pre-Merge Verification

Run all checks before completing:

```bash
# 1. Tests
bun test

# 2. TypeScript
bun tsc --noEmit

# 3. Lint
bun run lint

# 4. Build (if applicable)
bun run build

# 5. Git status
git status
```

All must pass before proceeding.

---

## Work Summary

Generate summary of branch work:

```bash
# Commits in this branch
git log main..HEAD --oneline

# Files changed
git diff --stat main

# Diff summary
git diff main --shortstat
```

---

## Completion Menu

```
[M] Merge — Merge to main locally
[P] Pull Request — Create PR on GitHub
[K] Keep — Keep branch, not ready yet
[D] Discard — Delete branch and changes (DANGEROUS)
```

---

## Option: Merge

```bash
# Ensure main is up to date
git checkout main
git pull origin main

# Merge feature branch
git merge feature/my-feature

# If conflicts, resolve then:
git add .
git commit

# Push
git push origin main

# Delete feature branch
git branch -d feature/my-feature
```

---

## Option: Pull Request

```bash
# Push branch
git push -u origin feature/my-feature

# Create PR
gh pr create --title "feat: add new feature" --body "$(cat <<'EOF'
## Summary
- [Change 1]
- [Change 2]

## Test plan
- [ ] Unit tests pass
- [ ] Manual testing done

🤖 Generated with Claude Code
EOF
)"
```

---

## Option: Keep

```bash
# Just stay on branch
echo "Branch kept. Continue working or come back later."
```

---

## Option: Discard

**REQUIRES EXPLICIT CONFIRMATION**

```bash
# Confirm discard
read -p "Type 'DISCARD' to confirm deletion: " confirm
if [ "$confirm" = "DISCARD" ]; then
  git checkout main
  git branch -D feature/my-feature
  echo "Branch discarded"
else
  echo "Discard cancelled"
fi
```

---

## Archive Specs

After merge/PR, archive related specs:

```bash
# Move specs to archive
mkdir -p .osforge/archive/$(date +%Y-%m)
mv docs/specs/feature-name.md .osforge/archive/$(date +%Y-%m)/
```

---

## Checklist

Before finishing:

```
- [ ] All tasks in spec completed
- [ ] All acceptance criteria verified
- [ ] Tests pass
- [ ] TypeScript compiles
- [ ] Lint passes
- [ ] No debug code (console.log, etc.)
- [ ] Documentation updated (if needed)
- [ ] Changelog updated (if needed)
```

---

## Verification Evidence

```
✅ Pre-merge verification:
- `bun test` → 47 tests passed, 0 failed
- `bun tsc --noEmit` → exit 0
- `bun run lint` → 0 errors, 0 warnings
- `bun run build` → exit 0

📊 Branch summary:
- 12 commits
- 8 files changed
- +342 insertions, -56 deletions
```
