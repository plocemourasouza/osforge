---
name: clean-code
description: "Pragmatic clean-code standards: concise, direct, no over-engineering, and no unnecessary comments. Use when: code is over-engineered or has premature abstractions, a request to 'simplify this', reviewing names/functions/structure, a giant function or excessively deep nesting, removing redundant comments and dead code. Keywords: clean code, refactor, simplify, SRP, DRY, KISS, YAGNI, naming, over-engineering. Do NOT use for: system architecture decisions, performance optimization, or testing strategy."
metadata:
  author: antigravity-kit (adapted)
  version: "2.0"
  priority: "CRITICAL"
  source: "antigravity-kit"
allowed-tools: Read, Write, Edit
---

# Clean Code - Pragmatic AI Coding Standards

> **CRITICAL SKILL** - Be **concise, direct, and solution-focused**.

---

## Core Principles

| Principle | Rule |
|-----------|------|
| **SRP** | Single Responsibility - each function/class does ONE thing |
| **DRY** | Don't Repeat Yourself - extract duplicates, reuse |
| **KISS** | Keep It Simple - simplest solution that works |
| **YAGNI** | You Aren't Gonna Need It - don't build unused features |
| **Boy Scout** | Leave code cleaner than you found it |

---

## Naming Rules

| Element | Convention |
|---------|------------|
| **Variables** | Reveal intent: `userCount` not `n` |
| **Functions** | Verb + noun: `getUserById()` not `user()` |
| **Booleans** | Question form: `isActive`, `hasPermission`, `canEdit` |
| **Constants** | SCREAMING_SNAKE: `MAX_RETRY_COUNT` |

> **Rule:** If you need a comment to explain a name, rename it.

---

## Function Rules

| Rule | Description |
|------|-------------|
| **Small** | Max 20 lines, ideally 5-10 |
| **One Thing** | Does one thing, does it well |
| **One Level** | One level of abstraction per function |
| **Few Args** | Max 3 arguments, prefer 0-2 |
| **No Side Effects** | Don't mutate inputs unexpectedly |

---

## Code Structure

| Pattern | Apply |
|---------|-------|
| **Guard Clauses** | Early returns for edge cases |
| **Flat > Nested** | Avoid deep nesting (max 2 levels) |
| **Composition** | Small functions composed together |
| **Colocation** | Keep related code close |

---

## AI Coding Style

| Situation | Action |
|-----------|--------|
| User asks for feature | Write it directly |
| User reports bug | Fix it, then state the root cause in a sentence or two |
| No clear requirement | Ask, don't assume |

---

## Anti-Patterns (DON'T)

| Pattern | Fix |
|---------|-----|
| Comment every line | Delete obvious comments |
| Helper for one-liner | Inline the code |
| Factory for 2 objects | Direct instantiation |
| utils.ts with 1 function | Put code where used |
| "First we import..." | Just write code |
| Deep nesting | Guard clauses |
| Magic numbers | Named constants |
| God functions | Split by responsibility |

---

## Before Editing ANY File (THINK FIRST!)

**Before changing a file, ask yourself:**

| Question | Why |
|----------|-----|
| **What imports this file?** | They might break |
| **What does this file import?** | Interface changes |
| **What tests cover this?** | Tests might fail |
| **Is this a shared component?** | Multiple places affected |

**Quick Check:**
```
File to edit: UserService.ts
└── Who imports this? → UserController.ts, AuthController.ts
└── Do they need changes too? → Check function signatures
```

> **Rule:** Edit the file + all dependent files in the SAME task.
> **Never leave broken imports or missing updates.**

---

## Summary

| Do | Don't |
|----|--------|
| Write code directly | Write tutorials |
| Let code self-document | Add obvious comments |
| Fix bugs directly | Write a tutorial before fixing |
| Inline small things | Create unnecessary files |
| Name things clearly | Use abbreviations |
| Keep functions small | Write 100+ line functions |

> The user wants working code plus enough context to trust it.

---

## Self-Check Before Completing (MANDATORY)

**Before saying "task complete", verify:**

| Check | Question |
|-------|----------|
| ✅ **Goal met?** | Did I do exactly what user asked? |
| ✅ **Files edited?** | Did I modify all necessary files? |
| ✅ **Code works?** | Did I test/verify the change? |
| ✅ **No errors?** | Lint and TypeScript pass? |
| ✅ **Nothing forgotten?** | Any edge cases missed? |

> **Rule:** If ANY check fails, fix it before completing.

---

## Validation output

Run the project's own lint, type-check and test commands. Read the full output and report errors, warnings and passes with file:line. Fix errors in the files you changed; ask before fixing anything outside the requested scope, then re-run to confirm.

**Exhaustiveness bar** — a review under this skill is done when every rule section (Naming, Function, Structure, AI Coding Style, Anti-Patterns) was swept against the artifact and each violation carries file+line. Three sections checked reads exactly like six; the skipped one is where the debt lives.
