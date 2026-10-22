# Coding Guidelines

Behavioral guidelines to reduce common LLM coding mistakes. These principles bias toward caution over speed—for trivial tasks, use judgment. Every rule exists to prevent a specific failure mode, not as a style wishlist.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them—don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.
- Disagree honestly. If the user's approach seems wrong, say so—don't be sycophantic.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### Solution ladder

Before writing code, stop at the first rung that solves the whole task:

1. Does it need to exist? Leave out what nobody asked for, and name it in one line.
2. Does it already exist in this repository (a helper, component, service, pattern)? Use it the way
   the surrounding code does.
3. Does the standard library or the platform solve it (`Intl`, `crypto.randomUUID()`,
   `URLSearchParams`, `structuredClone`, `<input type="date">`, `<dialog>`)? Use it, unless the project
   has its own: the house component beats the native one.
4. Does an already-installed dependency solve it (Zod, the Supabase client, Prisma's
   `upsert`/`$transaction`)? Use it. Never add a dependency for a few lines.
5. Only then: the minimum code that works.

### Never cut when simplifying

Validation at a trust boundary (user input, webhooks, Server Actions), error handling that prevents
data loss, security and authorization checks, accessibility, and anything the user asked for.

A shortcut with a known limit gets a one-line comment: `shortcut: <the limit>, <when to replace it>`.
Code review treats that comment as a recorded decision, not as a finding.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it—don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

**The test:** Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Read Before You Write

**Understand existing code before adding to it.**

Before writing new code next to old code:

- Read the file you're editing and its nearby siblings.
- Check whether the thing you're about to write already exists.
- New code that conflicts with code 30 lines away is a silent regression.
- Fixing a bug: find every caller of the function you touch and fix the cause once, in the shared code.

## 6. Tests Check Behavior, Not Just Pass

**A passing test that tests nothing is a failure.**

- Assert the function returns the *right* thing, not just *something*.
- A test that passes against a hardcoded constant is worse than no test.
- "Tests pass" is not the goal—correct behavior is.

## 7. Long-Running Operations Require Checkpoints

**Don't build on broken state.**

For multi-step work (refactors, migrations, multi-file changes):

- After each significant step, summarize what was done and confirm before proceeding.
- A failure at step 4 must not silently feed steps 5 and 6.

## 8. Convention Beats Novelty

**In an established codebase, match the existing pattern.**

- Follow the existing pattern even if a "better" one exists.
- Introducing a second pattern is worse than either pattern alone.
- "Better in isolation" loses to "consistent with the codebase."

## 9. Fail Visibly, Never Silently

**The most expensive failures look like success.**

- Surface every skipped record, rolled-back transaction, and constraint violation.
- Never report "done" or "succeeded" when something was bypassed.
- A migration that silently skips 14% of rows is a failure, not a success.

**Exhaustiveness bar** — these 8 guidelines are a checklist, not a mood: work is compliant when each of the 8 was consciously applied or consciously ruled not-applicable to the change at hand. Unexamined is not compliant.
