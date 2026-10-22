---
name: repo-audit
description: "Whole-repository code audit that ranks what breaks first (leading word: blast radius). Use when: inheriting a codebase, auditing a repository before a release, or asked what is wrong with the code of a whole project. Keywords: repo audit, codebase audit, audit the repository, what breaks first, inherited project, pre-release audit. Do NOT use for: reviewing a diff or PR (code-review), auditing UI or visuals (ui-audit, redesign-audit), adversarial critique of one artifact (adversarial-review), hunting edge cases in one change (edge-case-hunter)."
model: opus
context: fork
agent: general-purpose
allowed-tools: Read, Grep, Glob, Bash
metadata:
  version: "1.0.0"
  inspired_by: "DietrichGebert/ponytail skills/ponytail-audit and skills/ponytail-debt (MIT, (c) 2026 DietrichGebert) at 09c434a: map first, proof per finding, shortcut ledger, ranked output. See THIRD_PARTY_NOTICES."
  status: "draft for outcome-eval round r3 (P-03); not installed, not in the manifest"
---

# Repo Audit (blast radius)

**Iron Law:** `NO FINDING WITHOUT A CONCRETE CASE AND A FILE:LINE`

Audit the whole repository like the engineer who just inherited it and will be paged when it breaks.
Go deep where a mistake costs the most. The report changes no code.

## When NOT to use
- A diff, a PR or a set of changed files → `code-review`
- UI, layout or visual quality → `ui-audit`, `redesign-audit`
- Tearing apart one spec, plan or document → `adversarial-review`

## Process

### 1. Map first
- Read the README, `package.json`, `next.config.*` and the deploy config (`vercel.json`, Dockerfile),
  `prisma/schema.prisma`, `supabase/migrations/` and the RLS policies.
- Read the entry points: App Router pages, Route Handlers, Server Actions, `middleware.ts`, jobs and cron.
- Read the tests.
- State the load you assume (one user, one team, many concurrent instances) and where it came from.

**Done when:** you can say in three sentences what the repository does, every entry point is listed, and
the assumed load is written down.

### 2. Follow the expensive flows end to end
Authentication and authorization, money, data writes, secrets, concurrent jobs. In a large repository go
deep where an error costs most and list what you did not read.

**Done when:** each of those flows that exists in the repository was traced from input to storage, or is
named under "Not verified".

### 3. Look for, in this order
1. **Bug:** wrong result, crash, missed edge case (empty, zero, rounding, time zones), callers that
   disagree with what a function returns.
2. **Risk:** security holes and data loss.
3. **Scale** under the declared load: check-then-write races, per-instance state that must be shared,
   lists that only grow, a query per item.
4. **Risky logic without a test** (money, auth, data writes, parsers).
5. **Big slowness.**
6. **Code that should not exist** (dead code, duplicated helpers, a dependency the platform covers).

Stack checklist:
- [ ] Supabase service-role key reachable from client code (`NEXT_PUBLIC_*`, a `"use client"` import)
- [ ] A table without RLS, or a view that bypasses it
- [ ] A Server Action or Route Handler without a session/role check
- [ ] Money in `float`/`Float`
- [ ] A balance or stock decrement outside `$transaction` / not conditional
- [ ] `findMany` without `take` on a table that grows
- [ ] N+1 queries in a Server Component

**Done when:** every class above and every checklist box has a verdict: finding, clean, or not applicable.

### 4. Prove each finding
- Every finding has a concrete case ("this input or situation leads to this wrong result") and a
  file:line. No case, no finding.
- Before calling code unused, search the whole tree, including tests, config and string references.
- A `shortcut: <limit>, <when to replace>` comment is a recorded decision, not a finding, unless the
  declared load already crosses its limit.

**Done when:** each finding left in the report has its case and its location.

### 5. Shortcut ledger
List every `shortcut:` comment as `file:line, what was simplified, limit, when to replace`. Tag
`no-trigger` the ones that do not say when to replace them: those are the ones that rot.

**Done when:** every `shortcut:` comment in the repository is in the ledger (or the ledger says "none").

### 6. Report
- **What this repository does** and the **assumed load**.
- Findings in **Must fix** / **Should fix** / **Nice to have**, numbered across groups, **at most 20**
  (say how many were left out). Each finding: what it is, the problem (the concrete case), the fix, and
  **If not fixed:** one sentence on the consequence for users or data.
- `Verdict:` what to fix first, or "healthy, nothing to fix".
- `Not verified:` what was not read or could not run.

**Done when:** the report has all four parts and no finding lacks a location, a case or a consequence.

## Anti-patterns
| WRONG | RIGHT |
|---|---|
| A long list of generic advice ("add monitoring", "consider caching") | Only problems with a concrete case in this code |
| Rating a declared `shortcut:` inside its limit as must-fix | Listing it in the ledger as a decision |
| Ranking a slow admin page above a double-spend | Ranking by what costs users or data the most |
| Reading files in alphabetical order until the context runs out | Mapping first, then going deep on the expensive flows |
| Editing code during the audit | A report only; fixes are a separate task |
