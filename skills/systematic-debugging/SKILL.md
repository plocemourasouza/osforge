---
name: systematic-debugging
description: "Diagnosis discipline anchored on the **feedback loop**: build a fast, deterministic pass/fail signal for the bug before touching any code. Use when: a bug is hard to reproduce, behavior is intermittent, a crash has no clear stacktrace, a regression has no obvious cause, or a performance problem needs root-cause work. Keywords: debug, crash, intermittent, flaky, regression, root cause, performance regression. Do NOT use for: a trivial bug with an obvious stack trace (fix it directly), a type or lint error (clean-code), an already-red test with a clear cause (tdd-workflow)."
model: sonnet
context: fork
agent: general-purpose
allowed-tools: Read, Bash, Glob, Grep, Edit
metadata:
  version: "2.0"
  author: antigravity-kit (adapted)
  source: "antigravity-kit"
  inspired_by: mattpocock/skills (diagnose)
  license_note: "Phase structure adapted from mattpocock/skills under MIT"
---

# Systematic Debugging (feedback loop)

**Iron Law:** `NO HYPOTHESIS UNTIL THE LOOP EXISTS — NO FIX UNTIL THE LOOP GOES RED`

The feedback loop **is** the skill. Everything after it is mechanical: with a fast, deterministic,
agent-runnable pass/fail signal, bisection and hypothesis-testing just consume the signal. Without
one, no amount of staring at code compensates. Spend disproportionate effort here.

## When NOT to use

- Obvious stack trace pointing at the line → fix it directly
- Type/lint error → `clean-code`
- A red test whose cause is clear → `tdd-workflow`

## Process

### Phase 1 — Build the feedback loop

Try, in rough order: a failing test at whatever seam reaches the bug · a curl/HTTP script against
the dev server · a CLI invocation diffing stdout against a known-good snapshot · a headless browser
script · replaying a captured payload/trace through the code path in isolation · a throwaway
harness (one service, mocked deps, single function call) · a property/fuzz loop for
"sometimes wrong output" · a bisection harness (`git bisect run`) when the bug appeared between two
known states · a differential loop (old vs new version, same input, diff outputs).

Then treat the loop as a product: make it faster (skip unrelated init), sharper (assert the
specific symptom, not "didn't crash"), more deterministic (pin time, seed RNG, freeze network).
A 2-second deterministic loop is a superpower; a 30-second flaky one is barely better than none.

**Non-deterministic bugs:** the goal is not a clean repro but a **higher reproduction rate** — loop
the trigger 100×, parallelise, add stress, narrow timing windows. A 50% flake is debuggable; 1% is
not. Raise the rate until it is.

**If you genuinely cannot build a loop:** stop and say so. List what you tried; ask for a captured
artifact (HAR, log dump, core dump) or access to the reproducing environment. Do NOT proceed to
hypotheses without a loop.

**Done when:** running one command shows the bug failing, deterministically or at a rate high
enough to debug against — and you have SEEN it fail. "I believe this would catch it" is not a loop.

### Phase 2 — Reproduce

Run the loop. Watch the bug appear.

**Done when:** the loop shows the failure mode the USER described — not a different failure that
happens to live nearby — and the exact symptom (message, wrong output, timing) is captured so
later phases can verify the fix addresses it. Wrong bug = wrong fix.

### Phase 3 — Hypothesise (before testing anything)

Generate **3–5 ranked hypotheses** before testing any of them — single-hypothesis generation
anchors on the first plausible idea. Each must be **falsifiable**:

> "If X is the cause, then changing Y makes the bug disappear / changing Z makes it worse."

Cannot state the prediction? It is a vibe, not a hypothesis — discard or sharpen. Show the ranked
list to the user before testing: they often re-rank instantly ("we just deployed a change to #3").
Don't block on it; proceed with your ranking if they are AFK.

**Done when:** 3–5 hypotheses exist, each with its written prediction, ranked.

### Phase 4 — Instrument

Each probe maps to one prediction from Phase 3. **One variable at a time.** Prefer a debugger or
REPL over logs; when logging, target the boundaries that distinguish hypotheses — never "log
everything and grep".

**Tag every debug log with a unique prefix** (e.g. `[DEBUG-a4f2]`). Cleanup becomes one grep;
untagged logs survive into production.

For performance regressions: measure first (timing harness, profiler, query plan), then bisect.
Logs are usually the wrong tool.

**Done when:** the surviving hypothesis is confirmed by its own prediction coming true under the
loop — not by plausibility.

### Phase 5 — Fix + regression test

Write the regression test **before** the fix, at a seam that exercises the real bug pattern as it
occurred. If the only available seam is too shallow to replicate the triggering chain, **that
itself is the finding** — record it and flag the architecture. False confidence from the wrong
seam is worse than a documented gap.

Then: watch the test fail → apply the fix → watch it pass → re-run the Phase 1 loop against the
original, un-minimised scenario.

**Done when:** the original loop no longer reproduces the bug AND the regression test passed from
red, or the absence of a correct seam is documented.

### Phase 6 — Cleanup + post-mortem

- [ ] `grep` the `[DEBUG-…]` prefix returns nothing
- [ ] Throwaway harnesses deleted or moved to a marked debug location
- [ ] The confirmed hypothesis stated in the commit message — the next debugger learns
- [ ] Ask: **what would have prevented this bug?** If the answer is architectural (no good test
  seam, tangled callers, hidden coupling), hand off to `codebase-design` with the specifics —
  after the fix is in, when you know more than when you started

**Done when:** all four boxes are checked. An undeleted debug log is a defect you authored.

## Anti-patterns

| WRONG | RIGHT |
|---|---|
| Read code → guess → edit → hope | Build the loop first; the loop decides |
| One plausible hypothesis, tested immediately | 3–5 ranked, falsifiable, THEN test |
| "Added logging everywhere" | Targeted probes, one per prediction, tagged |
| Test written after the fix, passing immediately | Test written before, seen red, then green |
| "Fixed — the error stopped appearing" | The original loop re-run and green, evidence quoted |
| Flaky bug set aside as untestable | Reproduction rate raised until debuggable |
