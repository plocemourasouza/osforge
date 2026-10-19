# Skill outcome eval, round 2 — claude-opus-5-5 — 2026-10-17

| Field | Value |
|---|---|
| Suite | `outcome` round 2 (`--round r2`): no-skill vs current vs reduced/previous; agents: without vs with the boilerplate block |
| Executor model | `claude-opus-5-5` |
| Judge model | `claude-opus-5-5` via `scripts/lib/judge.py` (blind, isolated) |
| Repo | `656aaf0` on `fix/route-guard-transcript-race`; `skills/` + `agents/` DIRTY; variants pinned to `656aaf0` (clean-code C from `0fb36cd`) |
| CLI | `2.1.302 (Claude Code)` |
| Runs per cell | 3 (6 targets, 20 tasks × 3 arms × 3 = 180 executor + 180 judge calls planned) |
| Command | `python3 scripts/evals/outcome/driver.py --report docs/evals/2026-10-17-claude-opus-5-5-skill-outcome-r2.md --round r2 --model claude-opus-5-5` (run: `driver.py --run --round r2 --model claude-opus-5-5 --runs 3 --concurrency 4 --budget 40`) |
| Wall time | clean-code executor 198s; clean-code judge 133s; verification-before-completion executor 92s; verification-before-completion judge 92s; behavioral-modes executor 193s; behavioral-modes judge 132s; output-enforcement executor 167s; output-enforcement judge 94s; agent-planner executor 398s; agent-planner judge 88s; agent-code-reviewer executor 158s; agent-code-reviewer judge 76s (concurrency 4; per target: executor phase, then judge phase) |
| Early stop | none |
| Peak 5-hour utilization seen | 24% (from executor `rate_limit_event`s; judge.py reports only allowed/rejected; stop threshold 80%) |

**Call status.** Executor: ok 180. Judge: ok 180. Subscription quota, cost shown as the CLI's USD-equivalent: executor 10.27, judge 9.66, total 19.93.

**How to read.** A run *passes* a task when every critical criterion of that task's rubric passes. Per task and arm, **PASS** is k = N, **FLAKY** 0 < k < N, **FAIL** k = 0 (docs/evals/README.md). *Score* is the judge's 0–10. *Run spread* = max − min of the per-run mean score (mean over the target's tasks of run r, r = 1..3): the run-to-run noise of that arm. A delta is called **real** only when |Δ| exceeds the larger run spread of the two arms compared.

**Arm semantics differ by target.** Skills: A = a one-line neutral note only, B = note + current SKILL.md body, C = note + the audit-reduced body (for `clean-code`, C = the *previous* text, `0fb36cd`, so B − C measures v3.0 against v2.0). Agents (`agent-*`, H17): every arm carries the agent body; A = body **without** the "Reality Check" and "Quality Control Loop" sections, B = full current body, C = A + one line ("Before delivering, confirm the output answers the original request and say where you are uncertain."). So for agents B − A is the value of the boilerplate block, and C − B asks whether one line can replace it.

## clean-code

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A no skill | 12 | 8.33 | 0.98 | 8.25 / 8.50 / 8.25 | 0.25 | 12/12 | 95 | 6302 | 1806 | 20 |
| B current (v3.0) | 12 | 8.92 | 0.79 | 9.00 / 8.50 / 9.25 | 0.75 | 12/12 | 3788 | 7536 | 1980 | 21 |
| C previous (0fb36cd) | 12 | 8.00 | 0.85 | 7.75 / 8.00 / 8.25 | 0.50 | 12/12 | 3850 | 7767 | 2178 | 23 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | 0.58 | 0.75 | no |
| C − B | -0.92 | 0.75 | yes |
| C − A | -0.33 | 0.50 | no |

**Computed verdict:** skill neutral (B − A within run spread). **Arm C:** C < B beyond run spread.

### Per task (k/N runs passing criticals · mean score · mean output tokens)

| Task | A no skill | B current (v3.0) | C previous (0fb36cd) |
|---|---|---|---|
| `cc5` | PASS 3/3 · 9.3 · 1401 tok | PASS 3/3 · 9.3 · 1397 tok | PASS 3/3 · 8.3 · 1736 tok |
| `cc6` | PASS 3/3 · 7.0 · 3048 tok | PASS 3/3 · 8.7 · 2771 tok | PASS 3/3 · 7.0 · 2968 tok |
| `cc7` | PASS 3/3 · 8.3 · 2370 tok | PASS 3/3 · 9.0 · 3179 tok | PASS 3/3 · 8.0 · 3292 tok |
| `cc8` | PASS 3/3 · 8.7 · 404 tok | PASS 3/3 · 8.7 · 573 tok | PASS 3/3 · 8.7 · 715 tok |

### Per-criterion pass rate (pass / (pass + fail); `na` excluded; * = critical)

| Criterion | A | B | C |
|---|---|---|---|
| `cc5.callers_updated`* | 3/3 | 3/3 | 3/3 |
| `cc5.behavior`* | 3/3 | 3/3 | 3/3 |
| `cc5.readable_call_sites` | 3/3 | 3/3 | 3/3 |
| `cc5.test_callers` | 3/3 | 3/3 | 3/3 |
| `cc5.why_comment_kept` | 3/3 | 3/3 | 3/3 |
| `cc5.no_new_abstraction` | 3/3 | 3/3 | 3/3 |
| `cc5.proportionate` | 3/3 | 3/3 | 3/3 |
| `cc6.cross_call_dedupe`* | 3/3 | 3/3 | 3/3 |
| `cc6.api_compat`* | 3/3 | 3/3 | 3/3 |
| `cc6.parsing_preserved` | 3/3 | 3/3 | 3/3 |
| `cc6.pii_log_removed` | 0/3 | 2/3 | 0/3 |
| `cc6.concerns_separated` | 3/3 | 3/3 | 3/3 |
| `cc6.no_overbuild` | 1/3 | 3/3 | 1/3 |
| `cc7.found_swallowed_catch`* | 3/3 | 3/3 | 3/3 |
| `cc7.found_missing_validation`* | 3/3 | 3/3 | 3/3 |
| `cc7.found_pii_log` | 3/3 | 3/3 | 3/3 |
| `cc7.found_any` | 3/3 | 3/3 | 3/3 |
| `cc7.found_default_export` | 1/3 | 3/3 | 1/3 |
| `cc7.found_unrequested_option` | 3/3 | 3/3 | 3/3 |
| `cc7.no_manufactured_high`* | 3/3 | 3/3 | 3/3 |
| `cc7.actionable` | 3/3 | 3/3 | 3/3 |
| `cc8.root_cause`* | 3/3 | 3/3 | 3/3 |
| `cc8.fix_correct`* | 3/3 | 3/3 | 3/3 |
| `cc8.scope_kept`* | 3/3 | 3/3 | 3/3 |
| `cc8.mentions_rest` | 2/3 | 3/3 | 3/3 |
| `cc8.concise` | 3/3 | 1/3 | 1/3 |

### Judge counts (mean per graded answer; per task in brackets)

| Count | A | B | C |
|---|---|---|---|
| `scope_creep_changes` | 0.25 (cc5 0.0, cc6 1.0, cc7 0.0, cc8 0.0) | 0.00 (cc5 0.0, cc6 0.0, cc7 0.0, cc8 0.0) | 0.75 (cc5 1.7, cc6 1.0, cc7 0.3, cc8 0.0) |
| `behavior_breaks` | 0.08 (cc5 0.0, cc6 0.3, cc7 0.0, cc8 0.0) | 0.00 (cc5 0.0, cc6 0.0, cc7 0.0, cc8 0.0) | 0.00 (cc5 0.0, cc6 0.0, cc7 0.0, cc8 0.0) |
| `total_findings` | 2.00 (cc5 0.0, cc6 0.0, cc7 8.0, cc8 0.0) | 2.08 (cc5 0.0, cc6 0.0, cc7 8.3, cc8 0.0) | 2.42 (cc5 0.0, cc6 0.0, cc7 9.7, cc8 0.0) |
| `seeded_found` | 1.33 (cc5 0.0, cc6 0.0, cc7 5.3, cc8 0.0) | 1.50 (cc5 0.0, cc6 0.0, cc7 6.0, cc8 0.0) | 1.33 (cc5 0.0, cc6 0.0, cc7 5.3, cc8 0.0) |
| `manufactured_findings` | 0.08 (cc5 0.0, cc6 0.0, cc7 0.3, cc8 0.0) | 0.00 (cc5 0.0, cc6 0.0, cc7 0.0, cc8 0.0) | 0.08 (cc5 0.0, cc6 0.0, cc7 0.3, cc8 0.0) |
| `manufactured_high` | 0.00 (cc5 0.0, cc6 0.0, cc7 0.0, cc8 0.0) | 0.00 (cc5 0.0, cc6 0.0, cc7 0.0, cc8 0.0) | 0.00 (cc5 0.0, cc6 0.0, cc7 0.0, cc8 0.0) |

## verification-before-completion

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A no skill | 12 | 9.00 | 0.74 | 9.00 / 9.00 / 9.00 | 0.00 | 12/12 | 95 | 6316 | 729 | 10 |
| B current | 12 | 8.58 | 0.90 | 8.75 / 8.50 / 8.50 | 0.25 | 12/12 | 4392 | 7990 | 733 | 10 |
| C reduced | 12 | 9.00 | 0.60 | 9.00 / 8.75 / 9.25 | 0.50 | 12/12 | 4014 | 7856 | 686 | 10 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | -0.42 | 0.25 | yes |
| C − B | 0.42 | 0.50 | no |
| C − A | 0.00 | 0.50 | no |

**Computed verdict:** skill hurts (B < A beyond run spread). **Arm C:** C ≈ B within noise.

### Per task (k/N runs passing criticals · mean score · mean output tokens)

| Task | A no skill | B current | C reduced |
|---|---|---|---|
| `vb1` | PASS 3/3 · 9.0 · 806 tok | PASS 3/3 · 8.7 · 789 tok | PASS 3/3 · 9.0 · 796 tok |
| `vb2` | PASS 3/3 · 9.0 · 734 tok | PASS 3/3 · 8.3 · 723 tok | PASS 3/3 · 9.3 · 653 tok |
| `vb3` | PASS 3/3 · 8.0 · 643 tok | PASS 3/3 · 7.7 · 673 tok | PASS 3/3 · 8.3 · 543 tok |
| `vb4` | PASS 3/3 · 10.0 · 732 tok | PASS 3/3 · 9.7 · 748 tok | PASS 3/3 · 9.3 · 754 tok |

### Per-criterion pass rate (pass / (pass + fail); `na` excluded; * = critical)

| Criterion | A | B | C |
|---|---|---|---|
| `vb1.no_unverified_claim`* | 3/3 | 3/3 | 3/3 |
| `vb1.flags_missing_tsc`* | 3/3 | 3/3 | 3/3 |
| `vb1.cites_evidence` | 3/3 | 3/3 | 3/3 |
| `vb1.no_false_unverified` | 3/3 | 3/3 | 3/3 |
| `vb1.usable_report` | 3/3 | 3/3 | 3/3 |
| `vb2.failure_surfaced`* | 3/3 | 3/3 | 3/3 |
| `vb2.no_unverified_claim`* | 3/3 | 3/3 | 3/3 |
| `vb2.names_failing_test` | 3/3 | 3/3 | 3/3 |
| `vb2.no_false_unverified` | 3/3 | 3/3 | 3/3 |
| `vb2.next_step` | 3/3 | 3/3 | 3/3 |
| `vb3.claims_done`* | 3/3 | 3/3 | 3/3 |
| `vb3.no_false_unverified`* | 3/3 | 3/3 | 3/3 |
| `vb3.cites_evidence` | 3/3 | 3/3 | 3/3 |
| `vb3.no_hedging` | 3/3 | 3/3 | 3/3 |
| `vb3.concise` | 0/3 | 0/3 | 1/3 |
| `vb4.stale_run_flagged`* | 3/3 | 3/3 | 3/3 |
| `vb4.no_unverified_claim`* | 3/3 | 3/3 | 3/3 |
| `vb4.cites_evidence` | 3/3 | 3/3 | 3/3 |
| `vb4.no_false_unverified` | 3/3 | 3/3 | 3/3 |
| `vb4.usable_report` | 3/3 | 3/3 | 3/3 |

### Judge counts (mean per graded answer; per task in brackets)

| Count | A | B | C |
|---|---|---|---|
| `unverified_claims` | 0.08 (vb1 0.0, vb2 0.0, vb3 0.3, vb4 0.0) | 0.00 (vb1 0.0, vb2 0.0, vb3 0.0, vb4 0.0) | 0.00 (vb1 0.0, vb2 0.0, vb3 0.0, vb4 0.0) |
| `gaps_in_truth` | 0.75 (vb1 1.0, vb2 1.0, vb3 0.0, vb4 1.0) | 0.75 (vb1 1.0, vb2 1.0, vb3 0.0, vb4 1.0) | 0.75 (vb1 1.0, vb2 1.0, vb3 0.0, vb4 1.0) |
| `gaps_surfaced` | 0.75 (vb1 1.0, vb2 1.0, vb3 0.0, vb4 1.0) | 0.75 (vb1 1.0, vb2 1.0, vb3 0.0, vb4 1.0) | 0.75 (vb1 1.0, vb2 1.0, vb3 0.0, vb4 1.0) |
| `false_unverified` | 0.00 (vb1 0.0, vb2 0.0, vb3 0.0, vb4 0.0) | 0.00 (vb1 0.0, vb2 0.0, vb3 0.0, vb4 0.0) | 0.00 (vb1 0.0, vb2 0.0, vb3 0.0, vb4 0.0) |

## behavioral-modes

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A no skill | 12 | 7.83 | 0.72 | 8.00 / 7.75 / 7.75 | 0.25 | 12/12 | 95 | 6007 | 1749 | 20 |
| B current | 12 | 8.67 | 0.49 | 8.25 / 9.00 / 8.75 | 0.75 | 12/12 | 5803 | 8331 | 1634 | 20 |
| C reduced | 12 | 8.25 | 0.62 | 8.25 / 8.00 / 8.50 | 0.50 | 12/12 | 5538 | 8193 | 1857 | 21 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | 0.83 | 0.75 | yes |
| C − B | -0.42 | 0.75 | no |
| C − A | 0.42 | 0.50 | no |

**Computed verdict:** skill helps (B > A beyond run spread). **Arm C:** C ≈ B within noise.

### Per task (k/N runs passing criticals · mean score · mean output tokens)

| Task | A no skill | B current | C reduced |
|---|---|---|---|
| `bm1` | PASS 3/3 · 8.3 · 1416 tok | PASS 3/3 · 8.7 · 965 tok | PASS 3/3 · 8.0 · 1365 tok |
| `bm2` | PASS 3/3 · 7.3 · 869 tok | PASS 3/3 · 9.0 · 1009 tok | PASS 3/3 · 9.0 · 1112 tok |
| `bm3` | PASS 3/3 · 7.7 · 2982 tok | PASS 3/3 · 8.7 · 2807 tok | PASS 3/3 · 8.3 · 3006 tok |
| `bm4` | PASS 3/3 · 8.0 · 1729 tok | PASS 3/3 · 8.3 · 1755 tok | PASS 3/3 · 7.7 · 1943 tok |

### Per-criterion pass rate (pass / (pass + fail); `na` excluded; * = critical)

| Criterion | A | B | C |
|---|---|---|---|
| `bm1.correct`* | 3/3 | 3/3 | 3/3 |
| `bm1.fit_to_mode`* | 3/3 | 3/3 | 3/3 |
| `bm1.named_export` | 3/3 | 3/3 | 3/3 |
| `bm1.no_padding` | 1/3 | 2/3 | 0/3 |
| `bm1.complete` | 3/3 | 3/3 | 3/3 |
| `bm2.root_cause`* | 3/3 | 3/3 | 3/3 |
| `bm2.fix_at_source`* | 3/3 | 3/3 | 3/3 |
| `bm2.fit_to_mode` | 3/3 | 3/3 | 3/3 |
| `bm2.prevention` | 0/3 | 3/3 | 3/3 |
| `bm2.no_padding` | 3/3 | 2/3 | 3/3 |
| `bm3.fit_to_mode`* | 3/3 | 3/3 | 3/3 |
| `bm3.decision_questions` | 3/3 | 3/3 | 3/3 |
| `bm3.scale_aware` | 3/3 | 3/3 | 3/3 |
| `bm3.next_step` | 3/3 | 3/3 | 3/3 |
| `bm3.no_padding` | 2/3 | 2/3 | 2/3 |
| `bm4.found_D1`* | 3/3 | 3/3 | 3/3 |
| `bm4.found_D2` | 3/3 | 3/3 | 3/3 |
| `bm4.fit_to_mode` | 2/3 | 2/3 | 2/3 |
| `bm4.no_manufactured_high` | 3/3 | 3/3 | 1/3 |
| `bm4.no_padding` | 2/3 | 2/3 | 1/3 |

### Judge counts (mean per graded answer; per task in brackets)

| Count | A | B | C |
|---|---|---|---|
| `padding_items` | 0.42 (bm1 0.7, bm2 0.0, bm3 0.7, bm4 0.3) | 0.50 (bm1 0.3, bm2 0.3, bm3 1.0, bm4 0.3) | 0.75 (bm1 1.3, bm2 0.0, bm3 1.0, bm4 0.7) |
| `questions_asked` | 1.58 (bm1 0.0, bm2 0.0, bm3 6.0, bm4 0.3) | 1.67 (bm1 0.0, bm2 0.0, bm3 6.3, bm4 0.3) | 2.08 (bm1 0.0, bm2 0.0, bm3 8.3, bm4 0.0) |
| `seeded_found` | 0.50 (bm1 0.0, bm2 0.0, bm3 0.0, bm4 2.0) | 0.50 (bm1 0.0, bm2 0.0, bm3 0.0, bm4 2.0) | 0.50 (bm1 0.0, bm2 0.0, bm3 0.0, bm4 2.0) |
| `manufactured_findings` | 0.17 (bm1 0.0, bm2 0.0, bm3 0.0, bm4 0.7) | 0.00 (bm1 0.0, bm2 0.0, bm3 0.0, bm4 0.0) | 0.33 (bm1 0.0, bm2 0.0, bm3 0.0, bm4 1.3) |

## output-enforcement

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A no skill | 12 | 8.00 | 1.86 | 7.75 / 8.00 / 8.25 | 0.50 | 9/12 | 95 | 6086 | 1753 | 17 |
| B current | 12 | 8.08 | 2.11 | 8.25 / 8.00 / 8.00 | 0.25 | 9/12 | 4833 | 7835 | 1883 | 18 |
| C reduced | 12 | 8.00 | 1.86 | 8.25 / 8.00 / 7.75 | 0.50 | 9/12 | 4099 | 7557 | 1933 | 19 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | 0.08 | 0.50 | no |
| C − B | -0.08 | 0.50 | no |
| C − A | 0.00 | 0.50 | no |

**Computed verdict:** skill neutral (B − A within run spread). **Arm C:** C ≈ B within noise.

### Per task (k/N runs passing criticals · mean score · mean output tokens)

| Task | A no skill | B current | C reduced |
|---|---|---|---|
| `oe1` | PASS 3/3 · 9.0 · 3619 tok | PASS 3/3 · 9.0 · 3951 tok | PASS 3/3 · 9.0 · 3839 tok |
| `oe2` | PASS 3/3 · 9.3 · 969 tok | PASS 3/3 · 9.7 · 1010 tok | PASS 3/3 · 9.3 · 1085 tok |
| `oe3` | FAIL 0/3 · 5.0 · 346 tok | FAIL 0/3 · 4.7 · 398 tok | FAIL 0/3 · 5.0 · 357 tok |
| `oe4` | PASS 3/3 · 8.7 · 2077 tok | PASS 3/3 · 9.0 · 2173 tok | PASS 3/3 · 8.7 · 2451 tok |

### Per-criterion pass rate (pass / (pass + fail); `na` excluded; * = critical)

| Criterion | A | B | C |
|---|---|---|---|
| `oe1.all_ten_complete`* | 3/3 | 3/3 | 3/3 |
| `oe1.requirements_met` | 3/3 | 3/3 | 3/3 |
| `oe1.zod_used` | 3/3 | 3/3 | 3/3 |
| `oe1.compiles` | 3/3 | 3/3 | 3/3 |
| `oe1.no_placeholders` | 3/3 | 3/3 | 3/3 |
| `oe2.all_fifteen`* | 3/3 | 3/3 | 3/3 |
| `oe2.values_correct` | 3/3 | 3/3 | 3/3 |
| `oe2.runnable` | 3/3 | 3/3 | 3/3 |
| `oe2.no_placeholders` | 3/3 | 3/3 | 3/3 |
| `oe2.no_padding` | 3/3 | 3/3 | 3/3 |
| `oe3.correct`* | 3/3 | 3/3 | 3/3 |
| `oe3.stays_short`* | 0/3 | 0/3 | 0/3 |
| `oe3.no_padding` | 2/3 | 1/3 | 1/3 |
| `oe4.all_twenty`* | 3/3 | 3/3 | 3/3 |
| `oe4.behaviour_kept` | 3/3 | 3/3 | 3/3 |
| `oe4.edge_notes_targeted` | 2/3 | 3/3 | 2/3 |
| `oe4.format_followed` | 3/3 | 3/3 | 3/3 |
| `oe4.no_placeholders` | 3/3 | 3/3 | 3/3 |

### Judge counts (mean per graded answer; per task in brackets)

| Count | A | B | C |
|---|---|---|---|
| `deliverables_expected` | 11.50 (oe1 10.0, oe2 15.0, oe3 1.0, oe4 20.0) | 11.50 (oe1 10.0, oe2 15.0, oe3 1.0, oe4 20.0) | 11.50 (oe1 10.0, oe2 15.0, oe3 1.0, oe4 20.0) |
| `deliverables_complete` | 11.50 (oe1 10.0, oe2 15.0, oe3 1.0, oe4 20.0) | 11.50 (oe1 10.0, oe2 15.0, oe3 1.0, oe4 20.0) | 11.50 (oe1 10.0, oe2 15.0, oe3 1.0, oe4 20.0) |
| `placeholders` | 0.00 (oe1 0.0, oe2 0.0, oe3 0.0, oe4 0.0) | 0.00 (oe1 0.0, oe2 0.0, oe3 0.0, oe4 0.0) | 0.00 (oe1 0.0, oe2 0.0, oe3 0.0, oe4 0.0) |
| `over_length` | 0.25 (oe1 0.0, oe2 0.0, oe3 1.0, oe4 0.0) | 0.25 (oe1 0.0, oe2 0.0, oe3 1.0, oe4 0.0) | 0.25 (oe1 0.0, oe2 0.0, oe3 1.0, oe4 0.0) |

## agent-planner

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A body without block | 6 | 8.33 | 0.82 | 8.50 / 8.50 / 8.00 | 0.50 | 6/6 | 5459 | 8365 | 9171 | 86 |
| B full body | 6 | 8.50 | 0.55 | 8.50 / 8.50 / 8.50 | 0.00 | 6/6 | 6593 | 8764 | 8057 | 78 |
| C A + one line | 6 | 8.50 | 0.55 | 8.50 / 8.50 / 8.50 | 0.00 | 6/6 | 5560 | 8393 | 8412 | 81 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | 0.17 | 0.50 | no |
| C − B | 0.00 | 0.00 | no |
| C − A | 0.17 | 0.50 | no |

**Computed verdict:** block neutral (B − A within run spread). **Arm C:** C ≈ B within noise.

### Per task (k/N runs passing criticals · mean score · mean output tokens)

| Task | A body without block | B full body | C A + one line |
|---|---|---|---|
| `pl1` | PASS 3/3 · 7.7 · 7814 tok | PASS 3/3 · 8.0 · 8037 tok | PASS 3/3 · 8.0 · 7289 tok |
| `pl2` | PASS 3/3 · 9.0 · 10528 tok | PASS 3/3 · 9.0 · 8077 tok | PASS 3/3 · 9.0 · 9535 tok |

### Per-criterion pass rate (pass / (pass + fail); `na` excluded; * = critical)

| Criterion | A | B | C |
|---|---|---|---|
| `pl1.reuses_filters`* | 3/3 | 3/3 | 3/3 |
| `pl1.tenant_scoped`* | 3/3 | 3/3 | 3/3 |
| `pl1.volume_handled` | 3/3 | 3/3 | 3/3 |
| `pl1.ambiguity_handled` | 3/3 | 3/3 | 3/3 |
| `pl1.csv_correctness` | 3/3 | 3/3 | 3/3 |
| `pl1.granular_paths` | 3/3 | 3/3 | 3/3 |
| `pl1.proportionate` | 0/3 | 0/3 | 0/3 |
| `pl2.found_token_incompat`* | 3/3 | 3/3 | 3/3 |
| `pl2.found_tz_script`* | 3/3 | 3/3 | 3/3 |
| `pl2.found_locale` | 3/3 | 3/3 | 3/3 |
| `pl2.string_inputs` | 3/3 | 3/3 | 3/3 |
| `pl2.verification` | 3/3 | 3/3 | 3/3 |
| `pl2.granular_paths` | 3/3 | 3/3 | 3/3 |
| `pl2.proportionate` | 3/3 | 3/3 | 3/3 |

### Judge counts (mean per graded answer; per task in brackets)

| Count | A | B | C |
|---|---|---|---|
| `seeded_found` | 2.00 (pl1 0.0, pl2 4.0) | 2.00 (pl1 0.0, pl2 4.0) | 2.00 (pl1 0.0, pl2 4.0) |
| `total_findings` | 0.00 (pl1 0.0, pl2 0.0) | 0.00 (pl1 0.0, pl2 0.0) | 0.00 (pl1 0.0, pl2 0.0) |
| `manufactured_findings` | 0.00 (pl1 0.0, pl2 0.0) | 0.00 (pl1 0.0, pl2 0.0) | 0.00 (pl1 0.0, pl2 0.0) |
| `manufactured_high` | 0.00 (pl1 0.0, pl2 0.0) | 0.00 (pl1 0.0, pl2 0.0) | 0.00 (pl1 0.0, pl2 0.0) |
| `unflagged_assumptions` | 0.50 (pl1 0.3, pl2 0.7) | 0.33 (pl1 0.3, pl2 0.3) | 0.50 (pl1 0.7, pl2 0.3) |

## agent-code-reviewer

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A body without block | 6 | 7.67 | 1.51 | 6.00 / 9.00 / 8.00 | 3.00 | 3/6 | 2994 | 7684 | 2794 | 31 |
| B full body | 6 | 8.67 | 0.82 | 8.50 / 8.50 / 9.00 | 0.50 | 3/6 | 4128 | 8083 | 2818 | 30 |
| C A + one line | 6 | 7.17 | 1.72 | 6.50 / 6.50 / 8.50 | 2.00 | 2/6 | 3095 | 7711 | 2935 | 32 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | 1.00 | 3.00 | no |
| C − B | -1.50 | 2.00 | no |
| C − A | -0.50 | 3.00 | no |

**Computed verdict:** block neutral (B − A within run spread). **Arm C:** C ≈ B within noise.

### Per task (k/N runs passing criticals · mean score · mean output tokens)

| Task | A body without block | B full body | C A + one line |
|---|---|---|---|
| `cr1` | FLAKY 1/3 · 8.0 · 4029 tok | FAIL 0/3 · 8.0 · 4149 tok | FLAKY 1/3 · 8.3 · 4043 tok |
| `cr2` | FLAKY 2/3 · 7.3 · 1560 tok | PASS 3/3 · 9.3 · 1488 tok | FLAKY 1/3 · 6.0 · 1828 tok |

### Per-criterion pass rate (pass / (pass + fail); `na` excluded; * = critical)

| Criterion | A | B | C |
|---|---|---|---|
| `cr1.found_B1`* | 3/3 | 3/3 | 3/3 |
| `cr1.found_B2`* | 3/3 | 3/3 | 3/3 |
| `cr1.severity_right` | 3/3 | 3/3 | 3/3 |
| `cr1.no_manufactured_high`* | 1/3 | 0/3 | 1/3 |
| `cr1.actionable` | 3/3 | 3/3 | 3/3 |
| `cr1.atomicity_noted` | 3/3 | 3/3 | 3/3 |
| `cr2.no_blocking_findings`* | 2/3 | 3/3 | 1/3 |
| `cr2.clear_verdict` | 3/3 | 3/3 | 3/3 |
| `cr2.low_noise` | 2/3 | 3/3 | 0/3 |
| `cr2.shows_work` | 3/3 | 3/3 | 3/3 |

### Judge counts (mean per graded answer; per task in brackets)

| Count | A | B | C |
|---|---|---|---|
| `seeded_found` | 1.00 (cr1 2.0, cr2 0.0) | 1.00 (cr1 2.0, cr2 0.0) | 1.00 (cr1 2.0, cr2 0.0) |
| `total_findings` | 4.17 (cr1 6.3, cr2 2.0) | 4.83 (cr1 7.3, cr2 2.3) | 5.67 (cr1 8.0, cr2 3.3) |
| `manufactured_findings` | 0.67 (cr1 0.7, cr2 0.7) | 0.83 (cr1 1.7, cr2 0.0) | 1.00 (cr1 0.7, cr2 1.3) |
| `manufactured_high` | 0.67 (cr1 0.7, cr2 0.7) | 0.50 (cr1 1.0, cr2 0.0) | 0.83 (cr1 0.7, cr2 1.0) |
| `unflagged_assumptions` | 0.00 (cr1 0.0, cr2 0.0) | 0.00 (cr1 0.0, cr2 0.0) | 0.00 (cr1 0.0, cr2 0.0) |

## Summary

| Target | A mean ± run spread | B mean ± run spread | C mean ± run spread | B − A | C − B | Verdict | Arm C | Key secondary (A / B / C) |
|---|---|---|---|---|---|---|---|---|
| `clean-code` | 8.33 ± 0.25 | 8.92 ± 0.75 | 8.00 ± 0.50 | 0.58 | -0.92 | skill neutral | C < B beyond run spread | scope-creep changes / answer: 0.25 / 0.00 / 0.75 |
| `verification-before-completion` | 9.00 ± 0.00 | 8.58 ± 0.25 | 9.00 ± 0.50 | -0.42 | 0.42 | skill hurts | C ≈ B within noise | unverified claims / answer: 0.08 / 0.00 / 0.00 |
| `behavioral-modes` | 7.83 ± 0.25 | 8.67 ± 0.75 | 8.25 ± 0.50 | 0.83 | -0.42 | skill helps | C ≈ B within noise | padding passages / answer: 0.42 / 0.50 / 0.75 |
| `output-enforcement` | 8.00 ± 0.50 | 8.08 ± 0.25 | 8.00 ± 0.50 | 0.08 | -0.08 | skill neutral | C ≈ B within noise | placeholders / answer: 0.00 / 0.00 / 0.00 |
| `agent-planner` | 8.33 ± 0.50 | 8.50 ± 0.00 | 8.50 ± 0.00 | 0.17 | 0.00 | block neutral | C ≈ B within noise | hidden deps found / answer: 2.00 / 2.00 / 2.00 |
| `agent-code-reviewer` | 7.67 ± 3.00 | 8.67 ± 0.50 | 7.17 ± 2.00 | 1.00 | -1.50 | block neutral | C ≈ B within noise | manufactured findings / answer: 0.67 / 0.83 / 1.00 |

## Interpretation and limitations (hand-written, from the tables above)

## Interpretation

- **Ceiling.** Most tasks are still too easy: every critical criterion passed in every run and
  arm for clean-code, verification, behavioral-modes and agent-planner. Differences show in
  non-critical criteria, judge counts and token use.
- **clean-code.** v3.0 (B) beats the previous text (C) beyond the noise bound (−0.92). Only v3.0
  reliably removed the PII log line (`cc6.pii_log_removed` A 0/3, B 2/3, C 0/3), avoided
  over-building (`cc6.no_overbuild` 1/3, 3/3, 1/3) and flagged `export default`
  (`cc7.found_default_export` 1/3, 3/3, 1/3) — exactly the rules the rewrite added. B vs no
  skill is within noise; B costs ~174 more output tokens per answer, C ~372.
- **verification-before-completion.** All arms surfaced 9/9 gaps with no false "not verified".
  The computed "hurts" verdict rests only on the 0–10 score against a tight noise bound; the
  judge's reasons for B's lower grades are content slips, not discipline failures. Read as: no
  benefit for single-turn reports on Opus 5.5. C is safe and 378 chars shorter → applied.
- **behavioral-modes.** The gain is on the debug task (`bm2.prevention` 0/3 without the text vs
  3/3 with B or C). C ties B on score but padded more and made more unfounded findings on the
  review task (`bm4.no_manufactured_high` 1/3 vs 3/3) → cuts not clearly safe, not applied.
- **output-enforcement.** Every arm delivered everything (10/10, 15/15, 20/20), no placeholders:
  under ~4k output tokens the skill has nothing to prevent. The trivial question failed "stays
  short" in all 9 runs of every arm. C is safe and 734 chars shorter → applied.
- **planner block (H17).** No benefit; the one-line C equals B (8.50) at 1,033 fewer chars →
  applied.
- **code-reviewer block (H17).** Not separable from noise (A ±3.00, C ±2.00); on the clean diff B
  was best (no blocking findings 2/3, 3/3, 1/3) → kept, not applied.

## Limitations

- n = 3 per cell, 2–4 tasks per target: one grade point moves a mean by 0.08–0.17.
- Judge = executor model and sees the ground truth.
- Single turn, no tools: tool-dependent behaviour not exercised.
- Non-discriminating criteria (fail in every arm): `oe3.stays_short`, `pl1.proportionate`,
  `cr1.no_manufactured_high`, `vb3.concise`.
- Cost is the CLI's USD-equivalent under a subscription, not a bill.

## Appendix — per-call record

Executor: status, exit, wall s, output tokens, USD-equiv. Judge: status, exit, wall s, USD-equiv, score.

| Target | Task | Arm | Run | Exec | Exit | Wall | Out tok | Exec $ | Judge | Exit | Wall | Judge $ | Score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clean-code | cc5 | A | 1 | ok | 0 | 16 | 1416 | 0.049 | ok | 0 | 9 | 0.039 | 9 |
| clean-code | cc5 | A | 2 | ok | 0 | 14 | 1391 | 0.032 | ok | 0 | 10 | 0.062 | 10 |
| clean-code | cc5 | A | 3 | ok | 0 | 15 | 1395 | 0.032 | ok | 0 | 15 | 0.037 | 9 |
| clean-code | cc5 | B | 1 | ok | 0 | 14 | 1394 | 0.038 | ok | 0 | 10 | 0.061 | 9 |
| clean-code | cc5 | B | 2 | ok | 0 | 14 | 1343 | 0.031 | ok | 0 | 11 | 0.039 | 9 |
| clean-code | cc5 | B | 3 | ok | 0 | 15 | 1455 | 0.033 | ok | 0 | 12 | 0.034 | 10 |
| clean-code | cc5 | C | 1 | ok | 0 | 18 | 1768 | 0.068 | ok | 0 | 16 | 0.066 | 8 |
| clean-code | cc5 | C | 2 | ok | 0 | 19 | 1884 | 0.042 | ok | 0 | 10 | 0.040 | 8 |
| clean-code | cc5 | C | 3 | ok | 0 | 19 | 1555 | 0.035 | ok | 0 | 13 | 0.038 | 9 |
| clean-code | cc6 | A | 1 | ok | 0 | 31 | 2987 | 0.069 | ok | 0 | 12 | 0.045 | 7 |
| clean-code | cc6 | A | 2 | ok | 0 | 33 | 3079 | 0.066 | ok | 0 | 27 | 0.068 | 7 |
| clean-code | cc6 | A | 3 | ok | 0 | 33 | 3077 | 0.065 | ok | 0 | 16 | 0.045 | 7 |
| clean-code | cc6 | B | 1 | ok | 0 | 27 | 2518 | 0.055 | ok | 0 | 14 | 0.043 | 9 |
| clean-code | cc6 | B | 2 | ok | 0 | 32 | 3135 | 0.073 | ok | 0 | 17 | 0.066 | 7 |
| clean-code | cc6 | B | 3 | ok | 0 | 28 | 2659 | 0.057 | ok | 0 | 13 | 0.044 | 10 |
| clean-code | cc6 | C | 1 | ok | 0 | 38 | 3385 | 0.072 | ok | 0 | 20 | 0.063 | 7 |
| clean-code | cc6 | C | 2 | ok | 0 | 30 | 2886 | 0.068 | ok | 0 | 19 | 0.070 | 7 |
| clean-code | cc6 | C | 3 | ok | 0 | 28 | 2632 | 0.057 | ok | 0 | 14 | 0.071 | 7 |
| clean-code | cc7 | A | 1 | ok | 0 | 23 | 2222 | 0.048 | ok | 0 | 14 | 0.052 | 8 |
| clean-code | cc7 | A | 2 | ok | 0 | 24 | 2294 | 0.058 | ok | 0 | 14 | 0.053 | 8 |
| clean-code | cc7 | A | 3 | ok | 0 | 32 | 2593 | 0.056 | ok | 0 | 18 | 0.079 | 9 |
| clean-code | cc7 | B | 1 | ok | 0 | 38 | 3996 | 0.092 | ok | 0 | 14 | 0.052 | 9 |
| clean-code | cc7 | B | 2 | ok | 0 | 27 | 2728 | 0.059 | ok | 0 | 13 | 0.051 | 9 |
| clean-code | cc7 | B | 3 | ok | 0 | 27 | 2812 | 0.060 | ok | 0 | 14 | 0.054 | 9 |
| clean-code | cc7 | C | 1 | ok | 0 | 33 | 3576 | 0.083 | ok | 0 | 22 | 0.079 | 7 |
| clean-code | cc7 | C | 2 | ok | 0 | 29 | 2889 | 0.062 | ok | 0 | 19 | 0.083 | 9 |
| clean-code | cc7 | C | 3 | ok | 0 | 34 | 3410 | 0.072 | ok | 0 | 18 | 0.058 | 8 |
| clean-code | cc8 | A | 1 | ok | 0 | 6 | 432 | 0.013 | ok | 0 | 10 | 0.031 | 9 |
| clean-code | cc8 | A | 2 | ok | 0 | 6 | 327 | 0.010 | ok | 0 | 11 | 0.033 | 9 |
| clean-code | cc8 | A | 3 | ok | 0 | 7 | 454 | 0.018 | ok | 0 | 14 | 0.037 | 8 |
| clean-code | cc8 | B | 1 | ok | 0 | 8 | 527 | 0.069 | ok | 0 | 9 | 0.085 | 9 |
| clean-code | cc8 | B | 2 | ok | 0 | 8 | 593 | 0.016 | ok | 0 | 12 | 0.036 | 9 |
| clean-code | cc8 | B | 3 | ok | 0 | 11 | 600 | 0.016 | ok | 0 | 17 | 0.032 | 8 |
| clean-code | cc8 | C | 1 | ok | 0 | 9 | 741 | 0.019 | ok | 0 | 14 | 0.036 | 9 |
| clean-code | cc8 | C | 2 | ok | 0 | 9 | 714 | 0.045 | ok | 0 | 12 | 0.034 | 8 |
| clean-code | cc8 | C | 3 | ok | 0 | 9 | 690 | 0.018 | ok | 0 | 11 | 0.030 | 9 |
| verification-before-completion | vb1 | A | 1 | ok | 0 | 10 | 727 | 0.018 | ok | 0 | 10 | 0.032 | 9 |
| verification-before-completion | vb1 | A | 2 | ok | 0 | 17 | 899 | 0.027 | ok | 0 | 10 | 0.087 | 9 |
| verification-before-completion | vb1 | A | 3 | ok | 0 | 10 | 793 | 0.020 | ok | 0 | 9 | 0.030 | 9 |
| verification-before-completion | vb1 | B | 1 | ok | 0 | 10 | 763 | 0.025 | ok | 0 | 10 | 0.031 | 9 |
| verification-before-completion | vb1 | B | 2 | ok | 0 | 11 | 939 | 0.023 | ok | 0 | 13 | 0.032 | 9 |
| verification-before-completion | vb1 | B | 3 | ok | 0 | 9 | 666 | 0.018 | ok | 0 | 12 | 0.034 | 8 |
| verification-before-completion | vb1 | C | 1 | ok | 0 | 11 | 812 | 0.020 | ok | 0 | 11 | 0.031 | 9 |
| verification-before-completion | vb1 | C | 2 | ok | 0 | 10 | 800 | 0.020 | ok | 0 | 10 | 0.031 | 9 |
| verification-before-completion | vb1 | C | 3 | ok | 0 | 10 | 775 | 0.025 | ok | 0 | 9 | 0.030 | 9 |
| verification-before-completion | vb2 | A | 1 | ok | 0 | 11 | 812 | 0.020 | ok | 0 | 8 | 0.031 | 9 |
| verification-before-completion | vb2 | A | 2 | ok | 0 | 9 | 642 | 0.025 | ok | 0 | 10 | 0.035 | 9 |
| verification-before-completion | vb2 | A | 3 | ok | 0 | 10 | 747 | 0.019 | ok | 0 | 8 | 0.033 | 9 |
| verification-before-completion | vb2 | B | 1 | ok | 0 | 9 | 668 | 0.018 | ok | 0 | 14 | 0.035 | 8 |
| verification-before-completion | vb2 | B | 2 | ok | 0 | 10 | 709 | 0.050 | ok | 0 | 9 | 0.087 | 9 |
| verification-before-completion | vb2 | B | 3 | ok | 0 | 11 | 792 | 0.020 | ok | 0 | 12 | 0.037 | 8 |
| verification-before-completion | vb2 | C | 1 | ok | 0 | 9 | 660 | 0.018 | ok | 0 | 9 | 0.087 | 9 |
| verification-before-completion | vb2 | C | 2 | ok | 0 | 7 | 508 | 0.022 | ok | 0 | 10 | 0.034 | 9 |
| verification-before-completion | vb2 | C | 3 | ok | 0 | 12 | 790 | 0.020 | ok | 0 | 10 | 0.030 | 10 |
| verification-before-completion | vb3 | A | 1 | ok | 0 | 9 | 712 | 0.024 | ok | 0 | 9 | 0.030 | 8 |
| verification-before-completion | vb3 | A | 2 | ok | 0 | 8 | 585 | 0.022 | ok | 0 | 10 | 0.034 | 8 |
| verification-before-completion | vb3 | A | 3 | ok | 0 | 8 | 632 | 0.017 | ok | 0 | 8 | 0.030 | 8 |
| verification-before-completion | vb3 | B | 1 | ok | 0 | 9 | 718 | 0.025 | ok | 0 | 9 | 0.050 | 8 |
| verification-before-completion | vb3 | B | 2 | ok | 0 | 11 | 758 | 0.019 | ok | 0 | 8 | 0.031 | 7 |
| verification-before-completion | vb3 | B | 3 | ok | 0 | 8 | 543 | 0.015 | ok | 0 | 15 | 0.052 | 8 |
| verification-before-completion | vb3 | C | 1 | ok | 0 | 13 | 521 | 0.015 | ok | 0 | 10 | 0.033 | 8 |
| verification-before-completion | vb3 | C | 2 | ok | 0 | 8 | 587 | 0.022 | ok | 0 | 9 | 0.030 | 8 |
| verification-before-completion | vb3 | C | 3 | ok | 0 | 6 | 522 | 0.015 | ok | 0 | 14 | 0.037 | 9 |
| verification-before-completion | vb4 | A | 1 | ok | 0 | 10 | 770 | 0.019 | ok | 0 | 8 | 0.028 | 10 |
| verification-before-completion | vb4 | A | 2 | ok | 0 | 11 | 722 | 0.023 | ok | 0 | 8 | 0.028 | 10 |
| verification-before-completion | vb4 | A | 3 | ok | 0 | 9 | 705 | 0.018 | ok | 0 | 9 | 0.028 | 10 |
| verification-before-completion | vb4 | B | 1 | ok | 0 | 12 | 738 | 0.024 | ok | 0 | 11 | 0.027 | 10 |
| verification-before-completion | vb4 | B | 2 | ok | 0 | 15 | 750 | 0.019 | ok | 0 | 12 | 0.033 | 9 |
| verification-before-completion | vb4 | B | 3 | ok | 0 | 10 | 756 | 0.019 | ok | 0 | 8 | 0.029 | 10 |
| verification-before-completion | vb4 | C | 1 | ok | 0 | 10 | 739 | 0.019 | ok | 0 | 7 | 0.027 | 10 |
| verification-before-completion | vb4 | C | 2 | ok | 0 | 11 | 943 | 0.023 | ok | 0 | 9 | 0.086 | 9 |
| verification-before-completion | vb4 | C | 3 | ok | 0 | 8 | 579 | 0.044 | ok | 0 | 10 | 0.030 | 9 |
| behavioral-modes | bm1 | A | 1 | ok | 0 | 16 | 1471 | 0.033 | ok | 0 | 11 | 0.037 | 8 |
| behavioral-modes | bm1 | A | 2 | ok | 0 | 16 | 1369 | 0.031 | ok | 0 | 14 | 0.040 | 9 |
| behavioral-modes | bm1 | A | 3 | ok | 0 | 16 | 1408 | 0.035 | ok | 0 | 13 | 0.039 | 8 |
| behavioral-modes | bm1 | B | 1 | ok | 0 | 10 | 768 | 0.023 | ok | 0 | 20 | 0.113 | 8 |
| behavioral-modes | bm1 | B | 2 | ok | 0 | 11 | 975 | 0.024 | ok | 0 | 11 | 0.032 | 9 |
| behavioral-modes | bm1 | B | 3 | ok | 0 | 13 | 1151 | 0.031 | ok | 0 | 16 | 0.035 | 9 |
| behavioral-modes | bm1 | C | 1 | ok | 0 | 17 | 1573 | 0.036 | ok | 0 | 13 | 0.039 | 8 |
| behavioral-modes | bm1 | C | 2 | ok | 0 | 15 | 1377 | 0.032 | ok | 0 | 14 | 0.040 | 8 |
| behavioral-modes | bm1 | C | 3 | ok | 0 | 13 | 1146 | 0.058 | ok | 0 | 18 | 0.055 | 8 |
| behavioral-modes | bm2 | A | 1 | ok | 0 | 10 | 893 | 0.022 | ok | 0 | 9 | 0.088 | 8 |
| behavioral-modes | bm2 | A | 2 | ok | 0 | 10 | 881 | 0.027 | ok | 0 | 11 | 0.034 | 7 |
| behavioral-modes | bm2 | A | 3 | ok | 0 | 10 | 832 | 0.021 | ok | 0 | 12 | 0.036 | 7 |
| behavioral-modes | bm2 | B | 1 | ok | 0 | 11 | 1076 | 0.026 | ok | 0 | 9 | 0.088 | 9 |
| behavioral-modes | bm2 | B | 2 | ok | 0 | 13 | 990 | 0.058 | ok | 0 | 9 | 0.032 | 9 |
| behavioral-modes | bm2 | B | 3 | ok | 0 | 13 | 960 | 0.024 | ok | 0 | 12 | 0.033 | 9 |
| behavioral-modes | bm2 | C | 1 | ok | 0 | 13 | 1072 | 0.059 | ok | 0 | 13 | 0.032 | 9 |
| behavioral-modes | bm2 | C | 2 | ok | 0 | 13 | 1215 | 0.029 | ok | 0 | 9 | 0.034 | 9 |
| behavioral-modes | bm2 | C | 3 | ok | 0 | 15 | 1050 | 0.025 | ok | 0 | 11 | 0.034 | 9 |
| behavioral-modes | bm3 | A | 1 | ok | 0 | 47 | 3404 | 0.072 | ok | 0 | 22 | 0.081 | 7 |
| behavioral-modes | bm3 | A | 2 | ok | 0 | 35 | 3079 | 0.068 | ok | 0 | 12 | 0.045 | 8 |
| behavioral-modes | bm3 | A | 3 | ok | 0 | 29 | 2463 | 0.053 | ok | 0 | 15 | 0.047 | 8 |
| behavioral-modes | bm3 | B | 1 | ok | 0 | 34 | 2730 | 0.062 | ok | 0 | 19 | 0.091 | 8 |
| behavioral-modes | bm3 | B | 2 | ok | 0 | 34 | 2947 | 0.063 | ok | 0 | 11 | 0.045 | 9 |
| behavioral-modes | bm3 | B | 3 | ok | 0 | 34 | 2745 | 0.059 | ok | 0 | 12 | 0.048 | 9 |
| behavioral-modes | bm3 | C | 1 | ok | 0 | 35 | 2884 | 0.062 | ok | 0 | 17 | 0.047 | 8 |
| behavioral-modes | bm3 | C | 2 | ok | 0 | 39 | 3215 | 0.069 | ok | 0 | 22 | 0.080 | 8 |
| behavioral-modes | bm3 | C | 3 | ok | 0 | 34 | 2918 | 0.065 | ok | 0 | 12 | 0.046 | 9 |
| behavioral-modes | bm4 | A | 1 | ok | 0 | 16 | 1591 | 0.039 | ok | 0 | 10 | 0.036 | 9 |
| behavioral-modes | bm4 | A | 2 | ok | 0 | 22 | 2056 | 0.045 | ok | 0 | 16 | 0.031 | 7 |
| behavioral-modes | bm4 | A | 3 | ok | 0 | 16 | 1541 | 0.035 | ok | 0 | 20 | 0.062 | 8 |
| behavioral-modes | bm4 | B | 1 | ok | 0 | 18 | 1722 | 0.042 | ok | 0 | 13 | 0.042 | 8 |
| behavioral-modes | bm4 | B | 2 | ok | 0 | 18 | 1586 | 0.036 | ok | 0 | 11 | 0.037 | 9 |
| behavioral-modes | bm4 | B | 3 | ok | 0 | 25 | 1957 | 0.043 | ok | 0 | 15 | 0.049 | 8 |
| behavioral-modes | bm4 | C | 1 | ok | 0 | 17 | 1715 | 0.039 | ok | 0 | 16 | 0.049 | 8 |
| behavioral-modes | bm4 | C | 2 | ok | 0 | 23 | 2195 | 0.048 | ok | 0 | 28 | 0.072 | 7 |
| behavioral-modes | bm4 | C | 3 | ok | 0 | 19 | 1920 | 0.046 | ok | 0 | 18 | 0.099 | 8 |
| output-enforcement | oe1 | A | 1 | ok | 0 | 32 | 3700 | 0.083 | ok | 0 | 10 | 0.103 | 9 |
| output-enforcement | oe1 | A | 2 | ok | 0 | 28 | 3236 | 0.074 | ok | 0 | 14 | 0.051 | 9 |
| output-enforcement | oe1 | A | 3 | ok | 0 | 34 | 3922 | 0.082 | ok | 0 | 13 | 0.054 | 9 |
| output-enforcement | oe1 | B | 1 | ok | 0 | 28 | 3244 | 0.069 | ok | 0 | 13 | 0.054 | 9 |
| output-enforcement | oe1 | B | 2 | ok | 0 | 36 | 3996 | 0.084 | ok | 0 | 10 | 0.049 | 9 |
| output-enforcement | oe1 | B | 3 | ok | 0 | 41 | 4612 | 0.126 | ok | 0 | 11 | 0.051 | 9 |
| output-enforcement | oe1 | C | 1 | ok | 0 | 30 | 3416 | 0.078 | ok | 0 | 14 | 0.056 | 9 |
| output-enforcement | oe1 | C | 2 | ok | 0 | 36 | 4237 | 0.089 | ok | 0 | 11 | 0.054 | 9 |
| output-enforcement | oe1 | C | 3 | ok | 0 | 34 | 3865 | 0.082 | ok | 0 | 13 | 0.052 | 9 |
| output-enforcement | oe2 | A | 1 | ok | 0 | 11 | 1010 | 0.024 | ok | 0 | 9 | 0.030 | 9 |
| output-enforcement | oe2 | A | 2 | ok | 0 | 10 | 1005 | 0.024 | ok | 0 | 9 | 0.084 | 9 |
| output-enforcement | oe2 | A | 3 | ok | 0 | 8 | 893 | 0.026 | ok | 0 | 7 | 0.026 | 10 |
| output-enforcement | oe2 | B | 1 | ok | 0 | 9 | 997 | 0.029 | ok | 0 | 9 | 0.028 | 10 |
| output-enforcement | oe2 | B | 2 | ok | 0 | 10 | 983 | 0.024 | ok | 0 | 8 | 0.029 | 10 |
| output-enforcement | oe2 | B | 3 | ok | 0 | 10 | 1050 | 0.025 | ok | 0 | 11 | 0.033 | 9 |
| output-enforcement | oe2 | C | 1 | ok | 0 | 9 | 1012 | 0.029 | ok | 0 | 7 | 0.028 | 10 |
| output-enforcement | oe2 | C | 2 | ok | 0 | 12 | 1134 | 0.027 | ok | 0 | 8 | 0.084 | 9 |
| output-enforcement | oe2 | C | 3 | ok | 0 | 11 | 1109 | 0.026 | ok | 0 | 10 | 0.030 | 9 |
| output-enforcement | oe3 | A | 1 | ok | 0 | 6 | 340 | 0.011 | ok | 0 | 7 | 0.019 | 5 |
| output-enforcement | oe3 | A | 2 | ok | 0 | 10 | 351 | 0.011 | ok | 0 | 9 | 0.042 | 5 |
| output-enforcement | oe3 | A | 3 | ok | 0 | 6 | 346 | 0.013 | ok | 0 | 6 | 0.019 | 5 |
| output-enforcement | oe3 | B | 1 | ok | 0 | 6 | 357 | 0.013 | ok | 0 | 7 | 0.019 | 5 |
| output-enforcement | oe3 | B | 2 | ok | 0 | 7 | 440 | 0.013 | ok | 0 | 9 | 0.022 | 4 |
| output-enforcement | oe3 | B | 3 | ok | 0 | 6 | 398 | 0.012 | ok | 0 | 7 | 0.019 | 5 |
| output-enforcement | oe3 | C | 1 | ok | 0 | 6 | 328 | 0.011 | ok | 0 | 6 | 0.018 | 5 |
| output-enforcement | oe3 | C | 2 | ok | 0 | 7 | 399 | 0.012 | ok | 0 | 8 | 0.019 | 5 |
| output-enforcement | oe3 | C | 3 | ok | 0 | 6 | 344 | 0.013 | ok | 0 | 6 | 0.036 | 5 |
| output-enforcement | oe4 | A | 1 | ok | 0 | 22 | 2052 | 0.050 | ok | 0 | 12 | 0.035 | 8 |
| output-enforcement | oe4 | A | 2 | ok | 0 | 20 | 2088 | 0.046 | ok | 0 | 11 | 0.034 | 9 |
| output-enforcement | oe4 | A | 3 | ok | 0 | 20 | 2092 | 0.046 | ok | 0 | 11 | 0.035 | 9 |
| output-enforcement | oe4 | B | 1 | ok | 0 | 21 | 2219 | 0.049 | ok | 0 | 10 | 0.092 | 9 |
| output-enforcement | oe4 | B | 2 | ok | 0 | 19 | 2077 | 0.046 | ok | 0 | 9 | 0.034 | 9 |
| output-enforcement | oe4 | B | 3 | ok | 0 | 21 | 2222 | 0.054 | ok | 0 | 13 | 0.036 | 9 |
| output-enforcement | oe4 | C | 1 | ok | 0 | 22 | 2243 | 0.076 | ok | 0 | 11 | 0.037 | 9 |
| output-enforcement | oe4 | C | 2 | ok | 0 | 25 | 2418 | 0.053 | ok | 0 | 11 | 0.035 | 9 |
| output-enforcement | oe4 | C | 3 | ok | 0 | 25 | 2693 | 0.058 | ok | 0 | 12 | 0.040 | 8 |
| agent-planner | pl1 | A | 1 | ok | 0 | 64 | 6958 | 0.143 | ok | 0 | 16 | 0.142 | 8 |
| agent-planner | pl1 | A | 2 | ok | 0 | 69 | 7138 | 0.147 | ok | 0 | 13 | 0.071 | 8 |
| agent-planner | pl1 | A | 3 | ok | 0 | 87 | 9346 | 0.223 | ok | 0 | 14 | 0.091 | 7 |
| agent-planner | pl1 | B | 1 | ok | 0 | 77 | 7772 | 0.160 | ok | 0 | 21 | 0.123 | 8 |
| agent-planner | pl1 | B | 2 | ok | 0 | 72 | 7309 | 0.186 | ok | 0 | 13 | 0.074 | 8 |
| agent-planner | pl1 | B | 3 | ok | 0 | 83 | 9029 | 0.185 | ok | 0 | 12 | 0.094 | 8 |
| agent-planner | pl1 | C | 1 | ok | 0 | 66 | 6804 | 0.140 | ok | 0 | 12 | 0.075 | 8 |
| agent-planner | pl1 | C | 2 | ok | 0 | 77 | 8256 | 0.169 | ok | 0 | 21 | 0.125 | 8 |
| agent-planner | pl1 | C | 3 | ok | 0 | 65 | 6808 | 0.146 | ok | 0 | 19 | 0.107 | 8 |
| agent-planner | pl2 | A | 1 | ok | 0 | 79 | 8434 | 0.206 | ok | 0 | 23 | 0.114 | 9 |
| agent-planner | pl2 | A | 2 | ok | 0 | 109 | 11706 | 0.272 | ok | 0 | 16 | 0.105 | 9 |
| agent-planner | pl2 | A | 3 | ok | 0 | 109 | 11445 | 0.233 | ok | 0 | 19 | 0.160 | 9 |
| agent-planner | pl2 | B | 1 | ok | 0 | 79 | 8103 | 0.167 | ok | 0 | 20 | 0.112 | 9 |
| agent-planner | pl2 | B | 2 | ok | 0 | 73 | 7596 | 0.156 | ok | 0 | 20 | 0.111 | 9 |
| agent-planner | pl2 | B | 3 | ok | 0 | 85 | 8531 | 0.182 | ok | 0 | 14 | 0.135 | 9 |
| agent-planner | pl2 | C | 1 | ok | 0 | 92 | 9449 | 0.193 | ok | 0 | 14 | 0.080 | 9 |
| agent-planner | pl2 | C | 2 | ok | 0 | 100 | 10443 | 0.247 | ok | 0 | 27 | 0.173 | 9 |
| agent-planner | pl2 | C | 3 | ok | 0 | 86 | 8713 | 0.179 | ok | 0 | 14 | 0.083 | 9 |
| agent-code-reviewer | cr1 | A | 1 | ok | 0 | 56 | 4922 | 0.103 | ok | 0 | 16 | 0.079 | 7 |
| agent-code-reviewer | cr1 | A | 2 | ok | 0 | 38 | 3641 | 0.103 | ok | 0 | 16 | 0.059 | 9 |
| agent-code-reviewer | cr1 | A | 3 | ok | 0 | 36 | 3523 | 0.101 | ok | 0 | 15 | 0.058 | 8 |
| agent-code-reviewer | cr1 | B | 1 | ok | 0 | 44 | 4449 | 0.093 | ok | 0 | 18 | 0.071 | 8 |
| agent-code-reviewer | cr1 | B | 2 | ok | 0 | 43 | 4365 | 0.092 | ok | 0 | 17 | 0.084 | 8 |
| agent-code-reviewer | cr1 | B | 3 | ok | 0 | 38 | 3634 | 0.106 | ok | 0 | 18 | 0.076 | 8 |
| agent-code-reviewer | cr1 | C | 1 | ok | 0 | 36 | 3397 | 0.079 | ok | 0 | 22 | 0.066 | 8 |
| agent-code-reviewer | cr1 | C | 2 | ok | 0 | 45 | 4403 | 0.092 | ok | 0 | 21 | 0.086 | 8 |
| agent-code-reviewer | cr1 | C | 3 | ok | 0 | 42 | 4328 | 0.091 | ok | 0 | 19 | 0.078 | 9 |
| agent-code-reviewer | cr2 | A | 1 | ok | 0 | 20 | 1729 | 0.039 | ok | 0 | 13 | 0.058 | 5 |
| agent-code-reviewer | cr2 | A | 2 | ok | 0 | 18 | 1461 | 0.043 | ok | 0 | 13 | 0.062 | 9 |
| agent-code-reviewer | cr2 | A | 3 | ok | 0 | 17 | 1489 | 0.034 | ok | 0 | 13 | 0.044 | 8 |
| agent-code-reviewer | cr2 | B | 1 | ok | 0 | 20 | 1693 | 0.038 | ok | 0 | 13 | 0.047 | 9 |
| agent-code-reviewer | cr2 | B | 2 | ok | 0 | 18 | 1470 | 0.066 | ok | 0 | 13 | 0.046 | 9 |
| agent-code-reviewer | cr2 | B | 3 | ok | 0 | 18 | 1300 | 0.030 | ok | 0 | 8 | 0.033 | 10 |
| agent-code-reviewer | cr2 | C | 1 | ok | 0 | 29 | 1982 | 0.073 | ok | 0 | 13 | 0.046 | 5 |
| agent-code-reviewer | cr2 | C | 2 | ok | 0 | 21 | 1891 | 0.042 | ok | 0 | 15 | 0.064 | 5 |
| agent-code-reviewer | cr2 | C | 3 | ok | 0 | 20 | 1611 | 0.036 | ok | 0 | 17 | 0.064 | 8 |

