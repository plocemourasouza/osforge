---
name: clean-code
description: "Pragmatic clean-code standards: concise, direct, no over-engineering, and no unnecessary comments. Use when: code is over-engineered or has premature abstractions, a request to 'simplify this', reviewing names/functions/structure, a giant function or excessively deep nesting, removing redundant comments and dead code. Keywords: clean code, refactor, simplify, SRP, DRY, KISS, YAGNI, naming, over-engineering. Do NOT use for: system architecture decisions, performance optimization, or testing strategy."
metadata:
  author: antigravity-kit (adapted)
  version: "3.0"
  source: "antigravity-kit"
allowed-tools: Read, Write, Edit
---

# Clean Code

What good code looks like in this portfolio, and the bar a review holds it to. How to *work* —
assumptions, surgical scope, verification — lives in `coding-guidelines`; this skill covers the
shape of the code itself. Where the two touch, `coding-guidelines` wins on scope: improve the
code you were asked to change, not the code beside it.

## Simplicity

Write the least code that solves the stated problem. An abstraction earns its place when it has
a second real caller or isolates something genuinely volatile (an external API, a storage
backend); before that, inline it. The usual over-builds to undo:

| Over-build | Instead |
|---|---|
| Factory / strategy / registry for two cases | An `if` or a lookup object |
| `utils.ts` holding one function | Put the function where it is used |
| Wrapper that only forwards arguments | Call the underlying function |
| Config option nobody asked for | Hard-code it; add the option when someone needs it |
| Error handling for states the types already rule out | Trust the types; validate at the boundary instead |

Duplication of two or three similar lines is cheaper than the wrong abstraction. Extract when
the copies must change together, not when they merely look alike.

## Names

A name says what a thing is or does in the domain's words — use the project glossary
(`CONTEXT.md`) when there is one. Functions read as verb + object (`getInvoiceById`), booleans
as a question (`isOverdue`, `canRefund`), constants carry their unit (`TIMEOUT_MS`). If a name
needs a comment to be understood, rename it.

## Functions and structure

These are heuristics for judgment, not limits to enforce mechanically:

- One function, one job at one level of abstraction. Split when a function mixes levels
  (parsing + business rule + I/O), not when it crosses a line count.
- Guard clauses and early returns instead of nested conditionals; nesting past two or three
  levels is a signal to restructure.
- Pass an options object once positional arguments stop being self-explanatory.
- Do not mutate inputs; return new values. Side effects live at the edges (handlers, jobs,
  repositories), pure logic in the middle where it is easy to test.
- Keep related code together; colocate a component's types, helpers and tests with it.

## Errors and boundaries

- Validate external input once, at the boundary (Zod in this stack), then work with typed data.
- Fail visibly: a caught error is handled, rethrown with context, or logged with structured
  fields (`{ action, tenantId, userId, duration, error }`, never PII) — never swallowed.
- Generic messages to the client, detail in server logs.

## Comments

Comment *why* — a constraint, a workaround, a non-obvious invariant — never *what* the next line
does. Delete commented-out code and comments that restate the code. Keep doc comments on public
APIs.

## Stack conventions

TypeScript strict with no `any`, `as const` instead of `enum`, named exports, path aliases and
Server Components by default: these are defined once in the global spine (*TypeScript Strict
Mode* and *Code Style*). Apply them; do not restate them here.

## Reviewing against this skill

Report each finding with file:line, the section above it violates, and the concrete fix. A
finding that only restates personal taste, or that a linter already catches, is not a finding.
Zero findings is a valid result once every section was checked.

**Exhaustiveness bar** — a review under this skill is done when every section (Simplicity,
Names, Functions and structure, Errors and boundaries, Comments, Stack conventions) was swept
against the artifact and each violation carries file+line.
