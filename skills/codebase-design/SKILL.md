---
name: codebase-design
description: "Shared vocabulary and discipline for designing **deep modules** — a lot of behaviour behind a small interface, placed at a clean **seam**. Use when: designing or improving a module's interface, deciding where a seam goes, making code testable or AI-navigable, a debugging post-mortem flagged an architectural cause, or another skill needs the deep-module vocabulary. Keywords: deep module, seam, interface, depth, adapter, testability, coupling, architecture refactor, deletion test. Do NOT use for: pragmatic code cleanup and naming (clean-code), stack or ADR decisions (technical-design-doc-creator, arch-builder), domain terminology (domain-modeling)."
model: sonnet
allowed-tools: Read, Grep, Glob
metadata:
  version: "1.0.0"
  inspired_by: mattpocock/skills (codebase-design, improve-codebase-architecture)
  source: mattpocock/skills
  license_note: "Adapted under MIT; concepts from Ousterhout (A Philosophy of Software Design) and Feathers"
---

# Codebase Design (seam)

**Iron Law:** `USE THESE TERMS EXACTLY — A SECOND VOCABULARY FOR THE SAME IDEA HIDES THE IDEA`

This skill is mostly reference: a glossary-as-contract. Consistent language is the point — do not
drift into "component", "service", "API" or "boundary". When `CONTEXT.md` names the domain concept,
combine both: "the **Order intake** module", not "the FooBarHandler".

## Glossary (use verbatim)

- **Module** — anything with an interface and an implementation: function, class, package, slice.
- **Interface** — everything a caller must know to use the module: types, invariants, error modes,
  ordering, config. Not just the type signature.
- **Implementation** — the code inside.
- **Depth** — leverage at the interface: a lot of behaviour behind a small interface. **Deep** =
  high leverage. **Shallow** = interface nearly as complex as the implementation it fronts.
- **Seam** — where an interface lives; a place behaviour can be altered without editing in place.
  (Use this, never "boundary".)
- **Adapter** — a concrete thing satisfying an interface at a seam. One adapter = hypothetical
  seam. **Two adapters = real seam.**
- **Leverage** — what callers get from depth.
- **Locality** — what maintainers get from depth: change, bugs and knowledge concentrated in one
  place instead of smeared across callers.

## The three tests

- **Deletion test** — imagine deleting the module. If complexity simply vanishes, it was a
  pass-through that never earned its keep. If complexity reappears scattered across N callers, the
  module was concentrating it — it is deep.
- **The interface is the test surface** — a module you cannot test through its own interface is
  telling you the interface is wrong, not that you need private-method tests.
- **Two-adapter test** — before designing for "swappability", count adapters. With one, the seam
  is hypothetical and its abstraction cost is paid for nothing yet.

## Applying it (when asked to review or improve architecture)

### 1. Explore for friction

Walk the code organically — no rigid heuristic — noting where you feel friction: understanding one
concept requires bouncing between many small modules · a module is shallow (interface ≈
implementation) · pure functions were extracted "for testability" but the bugs live in how they
are called (no locality) · a part is untestable through its current interface. Apply the deletion
test to every suspect.

Read the project's `CONTEXT.md` and existing ADRs first — the domain language names good seams,
and ADRs record decisions you should not re-litigate.

**Done when:** every candidate carries the files involved, the friction observed, and its deletion
test verdict. A candidate without a verdict is an impression.

### 2. Present candidates, then stop

Numbered list; for each: **files · problem · proposed deepening · what it buys in leverage,
locality and testability**. If a candidate contradicts an ADR, surface it only when the friction
justifies reopening — marked explicitly ("contradicts ADR-007, but worth reopening because…").

Do NOT design interfaces yet. Ask which candidate to pursue — the user's context re-ranks the list
in ways the code cannot.

**Done when:** the list is presented and a candidate chosen by the user, not by you.

### 3. Grill the chosen design

Walk the design tree with the user (`grilling` discipline: one question at a time, recommendation
attached): what sits behind the seam, what the interface promises, which tests survive the
refactor. Side effects happen inline:

- A deepened module named after a concept missing from `CONTEXT.md` → add the term
  (`domain-modeling`).
- The user rejects a candidate for a load-bearing reason → offer to record it
  (`osforge-db add-decision`), so the next architecture pass does not re-suggest it. Skip
  ephemeral reasons ("not now").

**Done when:** the interface is agreed, the surviving tests are named, and every rejection worth
remembering is recorded.

## Anti-patterns

| WRONG | RIGHT |
|---|---|
| "Extract an interface so it's flexible" (one adapter) | Two adapters or no seam — count first |
| Many tiny functions, each trivially testable, bugs in the wiring | Deepen: move the wiring behind one interface with locality |
| Testing private methods through exposure | Fix the interface until it is the test surface |
| Re-proposing what an ADR already rejected | Read ADRs first; reopen explicitly or not at all |
| "Boundary", "component", "service", "layer" | Module, interface, seam, adapter — the contract vocabulary |
