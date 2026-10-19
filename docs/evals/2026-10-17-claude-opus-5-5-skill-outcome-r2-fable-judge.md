# Skill outcome eval, round 2 — claude-opus-5-5 — 2026-10-17

| Field | Value |
|---|---|
| Suite | `outcome` round 2 (`--round r2`): no-skill vs current vs reduced/previous; agents: without vs with the boilerplate block |
| Executor model | `claude-opus-5-5` |
| Judge model | `claude-fable-5-1` via `scripts/lib/judge.py` (blind, isolated) |
| Repo | `4dafb78` on `fix/route-guard-transcript-race`; `skills/` + `agents/` clean; variants pinned to `656aaf0` (clean-code C from `0fb36cd`) |
| CLI | `2.1.302 (Claude Code)` |
| Runs per cell | 3 (6 targets, 20 tasks × 3 arms × 3 = 180 executor + 180 judge calls planned) |
| Command | `python3 scripts/evals/outcome/driver.py --report docs/evals/2026-10-17-claude-opus-5-5-skill-outcome-r2-fable-judge.md --round r2 --model claude-opus-5-5 --judge-model claude-fable-5-1` (run: `driver.py --run --round r2 --model claude-opus-5-5 --runs 3 --concurrency 4 --budget 40`) |
| Wall time | clean-code executor 198s; clean-code judge 133s; verification-before-completion executor 92s; verification-before-completion judge 92s; behavioral-modes executor 193s; behavioral-modes judge 132s; output-enforcement executor 167s; output-enforcement judge 94s; agent-planner executor 398s; agent-planner judge 88s; agent-code-reviewer executor 158s; agent-code-reviewer judge 76s (concurrency 4; per target: executor phase, then judge phase) |
| Early stop | none |
| Peak 5-hour utilization seen | 24% (from executor `rate_limit_event`s; judge.py reports only allowed/rejected; stop threshold 80%) |

**Call status.** Executor: ok 180. Judge: ok 180. Subscription quota, cost shown as the CLI's USD-equivalent: executor 10.27, judge 28.06, total 38.33.

**How to read.** A run *passes* a task when every critical criterion of that task's rubric passes. Per task and arm, **PASS** is k = N, **FLAKY** 0 < k < N, **FAIL** k = 0 (docs/evals/README.md). *Score* is the judge's 0–10. *Run spread* = max − min of the per-run mean score (mean over the target's tasks of run r, r = 1..3): the run-to-run noise of that arm. A delta is called **real** only when |Δ| exceeds the larger run spread of the two arms compared.

**Arm semantics differ by target.** Skills: A = a one-line neutral note only, B = note + current SKILL.md body, C = note + the audit-reduced body (for `clean-code`, C = the *previous* text, `0fb36cd`, so B − C measures v3.0 against v2.0). Agents (`agent-*`, H17): every arm carries the agent body; A = body **without** the "Reality Check" and "Quality Control Loop" sections, B = full current body, C = A + one line ("Before delivering, confirm the output answers the original request and say where you are uncertain."). So for agents B − A is the value of the boilerplate block, and C − B asks whether one line can replace it.

## clean-code

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A no skill | 12 | 8.17 | 0.83 | 8.25 / 8.25 / 8.00 | 0.25 | 12/12 | 95 | 6302 | 1806 | 20 |
| B current (v3.0) | 12 | 8.75 | 0.62 | 9.00 / 8.50 / 8.75 | 0.50 | 12/12 | 3788 | 7536 | 1980 | 21 |
| C previous (0fb36cd) | 12 | 8.17 | 1.11 | 7.75 / 8.50 / 8.25 | 0.75 | 11/12 | 3850 | 7767 | 2178 | 23 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | 0.58 | 0.50 | yes |
| C − B | -0.58 | 0.75 | no |
| C − A | 0.00 | 0.75 | no |

**Computed verdict:** skill helps (B > A beyond run spread). **Arm C:** C ≈ B within noise.

### Per task (k/N runs passing criticals · mean score · mean output tokens)

| Task | A no skill | B current (v3.0) | C previous (0fb36cd) |
|---|---|---|---|
| `cc5` | PASS 3/3 · 9.0 · 1401 tok | PASS 3/3 · 9.0 · 1397 tok | PASS 3/3 · 9.0 · 1736 tok |
| `cc6` | PASS 3/3 · 7.0 · 3048 tok | PASS 3/3 · 8.3 · 2771 tok | PASS 3/3 · 7.0 · 2968 tok |
| `cc7` | PASS 3/3 · 8.0 · 2370 tok | PASS 3/3 · 9.0 · 3179 tok | FLAKY 2/3 · 7.7 · 3292 tok |
| `cc8` | PASS 3/3 · 8.7 · 404 tok | PASS 3/3 · 8.7 · 573 tok | PASS 3/3 · 9.0 · 715 tok |

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
| `cc6.no_overbuild` | 1/3 | 3/3 | 0/3 |
| `cc7.found_swallowed_catch`* | 3/3 | 3/3 | 3/3 |
| `cc7.found_missing_validation`* | 3/3 | 3/3 | 3/3 |
| `cc7.found_pii_log` | 3/3 | 3/3 | 3/3 |
| `cc7.found_any` | 3/3 | 3/3 | 3/3 |
| `cc7.found_default_export` | 1/3 | 3/3 | 1/3 |
| `cc7.found_unrequested_option` | 3/3 | 3/3 | 3/3 |
| `cc7.no_manufactured_high`* | 3/3 | 3/3 | 2/3 |
| `cc7.actionable` | 3/3 | 3/3 | 3/3 |
| `cc8.root_cause`* | 3/3 | 3/3 | 3/3 |
| `cc8.fix_correct`* | 3/3 | 3/3 | 3/3 |
| `cc8.scope_kept`* | 3/3 | 3/3 | 3/3 |
| `cc8.mentions_rest` | 2/3 | 3/3 | 3/3 |
| `cc8.concise` | 3/3 | 2/3 | 3/3 |

### Judge counts (mean per graded answer; per task in brackets)

| Count | A | B | C |
|---|---|---|---|
| `scope_creep_changes` | 0.33 (cc5 0.0, cc6 1.3, cc7 0.0, cc8 0.0) | 0.08 (cc5 0.0, cc6 0.3, cc7 0.0, cc8 0.0) | 0.67 (cc5 1.7, cc6 1.0, cc7 0.0, cc8 0.0) |
| `behavior_breaks` | 0.00 (cc5 0.0, cc6 0.0, cc7 0.0, cc8 0.0) | 0.00 (cc5 0.0, cc6 0.0, cc7 0.0, cc8 0.0) | 0.00 (cc5 0.0, cc6 0.0, cc7 0.0, cc8 0.0) |
| `total_findings` | 2.25 (cc5 0.0, cc6 0.0, cc7 9.0, cc8 0.0) | 1.83 (cc5 0.0, cc6 0.0, cc7 7.3, cc8 0.0) | 2.33 (cc5 0.0, cc6 0.0, cc7 9.3, cc8 0.0) |
| `seeded_found` | 1.33 (cc5 0.0, cc6 0.0, cc7 5.3, cc8 0.0) | 1.50 (cc5 0.0, cc6 0.0, cc7 6.0, cc8 0.0) | 1.33 (cc5 0.0, cc6 0.0, cc7 5.3, cc8 0.0) |
| `manufactured_findings` | 0.17 (cc5 0.0, cc6 0.0, cc7 0.7, cc8 0.0) | 0.17 (cc5 0.0, cc6 0.0, cc7 0.7, cc8 0.0) | 0.08 (cc5 0.0, cc6 0.0, cc7 0.3, cc8 0.0) |
| `manufactured_high` | 0.00 (cc5 0.0, cc6 0.0, cc7 0.0, cc8 0.0) | 0.00 (cc5 0.0, cc6 0.0, cc7 0.0, cc8 0.0) | 0.08 (cc5 0.0, cc6 0.0, cc7 0.3, cc8 0.0) |

## verification-before-completion

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A no skill | 12 | 9.08 | 0.51 | 8.75 / 9.25 / 9.25 | 0.50 | 12/12 | 95 | 6316 | 729 | 10 |
| B current | 12 | 8.75 | 0.75 | 8.75 / 8.50 / 9.00 | 0.50 | 12/12 | 4392 | 7990 | 733 | 10 |
| C reduced | 12 | 8.92 | 0.29 | 9.00 / 9.00 / 8.75 | 0.25 | 12/12 | 4014 | 7856 | 686 | 10 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | -0.33 | 0.50 | no |
| C − B | 0.17 | 0.50 | no |
| C − A | -0.17 | 0.50 | no |

**Computed verdict:** skill neutral (B − A within run spread). **Arm C:** C ≈ B within noise.

### Per task (k/N runs passing criticals · mean score · mean output tokens)

| Task | A no skill | B current | C reduced |
|---|---|---|---|
| `vb1` | PASS 3/3 · 9.0 · 806 tok | PASS 3/3 · 9.0 · 789 tok | PASS 3/3 · 9.0 · 796 tok |
| `vb2` | PASS 3/3 · 9.0 · 734 tok | PASS 3/3 · 8.7 · 723 tok | PASS 3/3 · 9.0 · 653 tok |
| `vb3` | PASS 3/3 · 8.7 · 643 tok | PASS 3/3 · 8.0 · 673 tok | PASS 3/3 · 9.0 · 543 tok |
| `vb4` | PASS 3/3 · 9.7 · 732 tok | PASS 3/3 · 9.3 · 748 tok | PASS 3/3 · 8.7 · 754 tok |

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
| `vb3.concise` | 2/3 | 1/3 | 3/3 |
| `vb4.stale_run_flagged`* | 3/3 | 3/3 | 3/3 |
| `vb4.no_unverified_claim`* | 3/3 | 3/3 | 3/3 |
| `vb4.cites_evidence` | 3/3 | 3/3 | 3/3 |
| `vb4.no_false_unverified` | 3/3 | 3/3 | 3/3 |
| `vb4.usable_report` | 3/3 | 3/3 | 3/3 |

### Judge counts (mean per graded answer; per task in brackets)

| Count | A | B | C |
|---|---|---|---|
| `unverified_claims` | 0.00 (vb1 0.0, vb2 0.0, vb3 0.0, vb4 0.0) | 0.00 (vb1 0.0, vb2 0.0, vb3 0.0, vb4 0.0) | 0.00 (vb1 0.0, vb2 0.0, vb3 0.0, vb4 0.0) |
| `gaps_in_truth` | 0.75 (vb1 1.0, vb2 1.0, vb3 0.0, vb4 1.0) | 0.75 (vb1 1.0, vb2 1.0, vb3 0.0, vb4 1.0) | 0.75 (vb1 1.0, vb2 1.0, vb3 0.0, vb4 1.0) |
| `gaps_surfaced` | 0.75 (vb1 1.0, vb2 1.0, vb3 0.0, vb4 1.0) | 0.75 (vb1 1.0, vb2 1.0, vb3 0.0, vb4 1.0) | 0.75 (vb1 1.0, vb2 1.0, vb3 0.0, vb4 1.0) |
| `false_unverified` | 0.00 (vb1 0.0, vb2 0.0, vb3 0.0, vb4 0.0) | 0.00 (vb1 0.0, vb2 0.0, vb3 0.0, vb4 0.0) | 0.00 (vb1 0.0, vb2 0.0, vb3 0.0, vb4 0.0) |

## behavioral-modes

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A no skill | 12 | 8.00 | 0.60 | 8.00 / 8.25 / 7.75 | 0.50 | 12/12 | 95 | 6007 | 1749 | 20 |
| B current | 12 | 8.33 | 0.78 | 7.75 / 8.75 / 8.50 | 1.00 | 12/12 | 5803 | 8331 | 1634 | 20 |
| C reduced | 12 | 8.42 | 0.79 | 8.50 / 8.25 / 8.50 | 0.25 | 12/12 | 5538 | 8193 | 1857 | 21 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | 0.33 | 1.00 | no |
| C − B | 0.08 | 1.00 | no |
| C − A | 0.42 | 0.50 | no |

**Computed verdict:** skill neutral (B − A within run spread). **Arm C:** C ≈ B within noise.

### Per task (k/N runs passing criticals · mean score · mean output tokens)

| Task | A no skill | B current | C reduced |
|---|---|---|---|
| `bm1` | PASS 3/3 · 8.3 · 1416 tok | PASS 3/3 · 8.7 · 965 tok | PASS 3/3 · 8.7 · 1365 tok |
| `bm2` | PASS 3/3 · 7.7 · 869 tok | PASS 3/3 · 8.7 · 1009 tok | PASS 3/3 · 9.0 · 1112 tok |
| `bm3` | PASS 3/3 · 7.7 · 2982 tok | PASS 3/3 · 8.7 · 2807 tok | PASS 3/3 · 8.7 · 3006 tok |
| `bm4` | PASS 3/3 · 8.3 · 1729 tok | PASS 3/3 · 7.3 · 1755 tok | PASS 3/3 · 7.3 · 1943 tok |

### Per-criterion pass rate (pass / (pass + fail); `na` excluded; * = critical)

| Criterion | A | B | C |
|---|---|---|---|
| `bm1.correct`* | 3/3 | 3/3 | 3/3 |
| `bm1.fit_to_mode`* | 3/3 | 3/3 | 3/3 |
| `bm1.named_export` | 3/3 | 3/3 | 3/3 |
| `bm1.no_padding` | 1/3 | 2/3 | 2/3 |
| `bm1.complete` | 3/3 | 3/3 | 3/3 |
| `bm2.root_cause`* | 3/3 | 3/3 | 3/3 |
| `bm2.fix_at_source`* | 3/3 | 3/3 | 3/3 |
| `bm2.fit_to_mode` | 3/3 | 3/3 | 3/3 |
| `bm2.prevention` | 0/3 | 3/3 | 3/3 |
| `bm2.no_padding` | 3/3 | 2/3 | 3/3 |
| `bm3.fit_to_mode`* | 3/3 | 3/3 | 3/3 |
| `bm3.decision_questions` | 3/3 | 3/3 | 3/3 |
| `bm3.scale_aware` | 2/3 | 3/3 | 3/3 |
| `bm3.next_step` | 3/3 | 3/3 | 3/3 |
| `bm3.no_padding` | 2/3 | 2/3 | 1/3 |
| `bm4.found_D1`* | 3/3 | 3/3 | 3/3 |
| `bm4.found_D2` | 3/3 | 3/3 | 3/3 |
| `bm4.fit_to_mode` | 3/3 | 1/3 | 3/3 |
| `bm4.no_manufactured_high` | 3/3 | 2/3 | 1/3 |
| `bm4.no_padding` | 2/3 | 0/3 | 0/3 |

### Judge counts (mean per graded answer; per task in brackets)

| Count | A | B | C |
|---|---|---|---|
| `padding_items` | 0.33 (bm1 0.7, bm2 0.0, bm3 0.3, bm4 0.3) | 0.50 (bm1 0.3, bm2 0.3, bm3 0.3, bm4 1.0) | 0.58 (bm1 0.3, bm2 0.0, bm3 0.7, bm4 1.3) |
| `questions_asked` | 2.50 (bm1 0.0, bm2 0.0, bm3 9.7, bm4 0.3) | 2.58 (bm1 0.0, bm2 0.0, bm3 10.0, bm4 0.3) | 2.25 (bm1 0.0, bm2 0.0, bm3 9.0, bm4 0.0) |
| `seeded_found` | 0.50 (bm1 0.0, bm2 0.0, bm3 0.0, bm4 2.0) | 0.50 (bm1 0.0, bm2 0.0, bm3 0.0, bm4 2.0) | 0.50 (bm1 0.0, bm2 0.0, bm3 0.0, bm4 2.0) |
| `manufactured_findings` | 0.50 (bm1 0.0, bm2 0.0, bm3 0.0, bm4 2.0) | 0.50 (bm1 0.0, bm2 0.0, bm3 0.0, bm4 2.0) | 0.58 (bm1 0.0, bm2 0.0, bm3 0.0, bm4 2.3) |

## output-enforcement

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A no skill | 12 | 7.92 | 2.19 | 8.00 / 7.75 / 8.00 | 0.25 | 9/12 | 95 | 6086 | 1753 | 17 |
| B current | 12 | 8.00 | 2.26 | 8.25 / 7.75 / 8.00 | 0.50 | 9/12 | 4833 | 7835 | 1883 | 18 |
| C reduced | 12 | 7.83 | 1.95 | 7.75 / 8.00 / 7.75 | 0.25 | 9/12 | 4099 | 7557 | 1933 | 19 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | 0.08 | 0.50 | no |
| C − B | -0.17 | 0.50 | no |
| C − A | -0.08 | 0.25 | no |

**Computed verdict:** skill neutral (B − A within run spread). **Arm C:** C ≈ B within noise.

### Per task (k/N runs passing criticals · mean score · mean output tokens)

| Task | A no skill | B current | C reduced |
|---|---|---|---|
| `oe1` | PASS 3/3 · 9.0 · 3619 tok | PASS 3/3 · 9.0 · 3951 tok | PASS 3/3 · 9.0 · 3839 tok |
| `oe2` | PASS 3/3 · 9.3 · 969 tok | PASS 3/3 · 9.7 · 1010 tok | PASS 3/3 · 9.0 · 1085 tok |
| `oe3` | FAIL 0/3 · 4.3 · 346 tok | FAIL 0/3 · 4.3 · 398 tok | FAIL 0/3 · 4.7 · 357 tok |
| `oe4` | PASS 3/3 · 9.0 · 2077 tok | PASS 3/3 · 9.0 · 2173 tok | PASS 3/3 · 8.7 · 2451 tok |

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
| `oe2.no_padding` | 2/3 | 3/3 | 2/3 |
| `oe3.correct`* | 3/3 | 3/3 | 3/3 |
| `oe3.stays_short`* | 0/3 | 0/3 | 0/3 |
| `oe3.no_padding` | 2/3 | 1/3 | 3/3 |
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
| A body without block | 6 | 7.67 | 0.52 | 8.00 / 7.50 / 7.50 | 0.50 | 6/6 | 5459 | 8365 | 9171 | 86 |
| B full body | 6 | 7.83 | 0.75 | 8.00 / 7.50 / 8.00 | 0.50 | 6/6 | 6593 | 8764 | 8057 | 78 |
| C A + one line | 6 | 8.17 | 0.41 | 8.50 / 8.00 / 8.00 | 0.50 | 6/6 | 5560 | 8393 | 8412 | 81 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | 0.17 | 0.50 | no |
| C − B | 0.33 | 0.50 | no |
| C − A | 0.50 | 0.50 | no |

**Computed verdict:** block neutral (B − A within run spread). **Arm C:** C ≈ B within noise.

### Per task (k/N runs passing criticals · mean score · mean output tokens)

| Task | A body without block | B full body | C A + one line |
|---|---|---|---|
| `pl1` | PASS 3/3 · 7.3 · 7814 tok | PASS 3/3 · 7.3 · 8037 tok | PASS 3/3 · 8.0 · 7289 tok |
| `pl2` | PASS 3/3 · 8.0 · 10528 tok | PASS 3/3 · 8.3 · 8077 tok | PASS 3/3 · 8.3 · 9535 tok |

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
| `manufactured_findings` | 0.83 (pl1 0.7, pl2 1.0) | 0.33 (pl1 0.7, pl2 0.0) | 0.00 (pl1 0.0, pl2 0.0) |
| `manufactured_high` | 0.00 (pl1 0.0, pl2 0.0) | 0.00 (pl1 0.0, pl2 0.0) | 0.00 (pl1 0.0, pl2 0.0) |
| `unflagged_assumptions` | 0.83 (pl1 1.0, pl2 0.7) | 0.33 (pl1 0.7, pl2 0.0) | 0.83 (pl1 1.0, pl2 0.7) |

## agent-code-reviewer

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A body without block | 6 | 7.00 | 1.67 | 5.50 / 8.00 / 7.50 | 2.50 | 2/6 | 2994 | 7684 | 2794 | 31 |
| B full body | 6 | 8.33 | 0.82 | 8.50 / 7.50 / 9.00 | 1.50 | 4/6 | 4128 | 8083 | 2818 | 30 |
| C A + one line | 6 | 6.67 | 2.25 | 5.50 / 5.50 / 9.00 | 3.50 | 2/6 | 3095 | 7711 | 2935 | 32 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | 1.33 | 2.50 | no |
| C − B | -1.67 | 3.50 | no |
| C − A | -0.33 | 3.50 | no |

**Computed verdict:** block neutral (B − A within run spread). **Arm C:** C ≈ B within noise.

### Per task (k/N runs passing criticals · mean score · mean output tokens)

| Task | A body without block | B full body | C A + one line |
|---|---|---|---|
| `cr1` | FAIL 0/3 · 7.0 · 4029 tok | FLAKY 1/3 · 8.0 · 4149 tok | FLAKY 1/3 · 7.7 · 4043 tok |
| `cr2` | FLAKY 2/3 · 7.0 · 1560 tok | PASS 3/3 · 8.7 · 1488 tok | FLAKY 1/3 · 5.7 · 1828 tok |

### Per-criterion pass rate (pass / (pass + fail); `na` excluded; * = critical)

| Criterion | A | B | C |
|---|---|---|---|
| `cr1.found_B1`* | 3/3 | 3/3 | 3/3 |
| `cr1.found_B2`* | 3/3 | 3/3 | 3/3 |
| `cr1.severity_right` | 3/3 | 3/3 | 3/3 |
| `cr1.no_manufactured_high`* | 0/3 | 1/3 | 1/3 |
| `cr1.actionable` | 3/3 | 3/3 | 3/3 |
| `cr1.atomicity_noted` | 3/3 | 3/3 | 3/3 |
| `cr2.no_blocking_findings`* | 2/3 | 3/3 | 1/3 |
| `cr2.clear_verdict` | 3/3 | 3/3 | 3/3 |
| `cr2.low_noise` | 2/3 | 3/3 | 1/3 |
| `cr2.shows_work` | 3/3 | 3/3 | 3/3 |

### Judge counts (mean per graded answer; per task in brackets)

| Count | A | B | C |
|---|---|---|---|
| `seeded_found` | 1.00 (cr1 2.0, cr2 0.0) | 1.00 (cr1 2.0, cr2 0.0) | 1.00 (cr1 2.0, cr2 0.0) |
| `total_findings` | 4.17 (cr1 6.3, cr2 2.0) | 4.67 (cr1 7.3, cr2 2.0) | 4.67 (cr1 7.0, cr2 2.3) |
| `manufactured_findings` | 1.00 (cr1 1.3, cr2 0.7) | 0.50 (cr1 1.0, cr2 0.0) | 1.17 (cr1 1.3, cr2 1.0) |
| `manufactured_high` | 0.83 (cr1 1.0, cr2 0.7) | 0.50 (cr1 1.0, cr2 0.0) | 1.00 (cr1 1.0, cr2 1.0) |
| `unflagged_assumptions` | 0.00 (cr1 0.0, cr2 0.0) | 0.00 (cr1 0.0, cr2 0.0) | 0.00 (cr1 0.0, cr2 0.0) |

## Summary

| Target | A mean ± run spread | B mean ± run spread | C mean ± run spread | B − A | C − B | Verdict | Arm C | Key secondary (A / B / C) |
|---|---|---|---|---|---|---|---|---|
| `clean-code` | 8.17 ± 0.25 | 8.75 ± 0.50 | 8.17 ± 0.75 | 0.58 | -0.58 | skill helps | C ≈ B within noise | scope-creep changes / answer: 0.33 / 0.08 / 0.67 |
| `verification-before-completion` | 9.08 ± 0.50 | 8.75 ± 0.50 | 8.92 ± 0.25 | -0.33 | 0.17 | skill neutral | C ≈ B within noise | unverified claims / answer: 0.00 / 0.00 / 0.00 |
| `behavioral-modes` | 8.00 ± 0.50 | 8.33 ± 1.00 | 8.42 ± 0.25 | 0.33 | 0.08 | skill neutral | C ≈ B within noise | padding passages / answer: 0.33 / 0.50 / 0.58 |
| `output-enforcement` | 7.92 ± 0.25 | 8.00 ± 0.50 | 7.83 ± 0.25 | 0.08 | -0.17 | skill neutral | C ≈ B within noise | placeholders / answer: 0.00 / 0.00 / 0.00 |
| `agent-planner` | 7.67 ± 0.50 | 7.83 ± 0.50 | 8.17 ± 0.50 | 0.17 | 0.33 | block neutral | C ≈ B within noise | hidden deps found / answer: 2.00 / 2.00 / 2.00 |
| `agent-code-reviewer` | 7.00 ± 2.50 | 8.33 ± 1.50 | 6.67 ± 3.50 | 1.33 | -1.67 | block neutral | C ≈ B within noise | manufactured findings / answer: 1.00 / 0.50 / 1.17 |

## Interpretation and limitations (hand-written, from the tables above)

## Interpretation

Same executor outputs as the Opus-judged report, re-graded by `claude-fable-5-1`. Cross-judge agreement and the check of every decision taken on the Opus verdicts: `docs/evals/2026-10-17-judge-agreement-opus-vs-fable.md`.

## Appendix — per-call record

Executor: status, exit, wall s, output tokens, USD-equiv. Judge: status, exit, wall s, USD-equiv, score.

| Target | Task | Arm | Run | Exec | Exit | Wall | Out tok | Exec $ | Judge | Exit | Wall | Judge $ | Score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clean-code | cc5 | A | 1 | ok | 0 | 16 | 1416 | 0.049 | ok | 0 | 83 | 0.117 | 9 |
| clean-code | cc5 | A | 2 | ok | 0 | 14 | 1391 | 0.032 | ok | 0 | 46 | 0.214 | 9 |
| clean-code | cc5 | A | 3 | ok | 0 | 15 | 1395 | 0.032 | ok | 0 | 24 | 0.118 | 9 |
| clean-code | cc5 | B | 1 | ok | 0 | 14 | 1394 | 0.038 | ok | 0 | 164 | 0.114 | 9 |
| clean-code | cc5 | B | 2 | ok | 0 | 14 | 1343 | 0.031 | ok | 0 | 21 | 0.111 | 9 |
| clean-code | cc5 | B | 3 | ok | 0 | 15 | 1455 | 0.033 | ok | 0 | 16 | 0.111 | 9 |
| clean-code | cc5 | C | 1 | ok | 0 | 18 | 1768 | 0.068 | ok | 0 | 23 | 0.132 | 9 |
| clean-code | cc5 | C | 2 | ok | 0 | 19 | 1884 | 0.042 | ok | 0 | 61 | 0.112 | 9 |
| clean-code | cc5 | C | 3 | ok | 0 | 19 | 1555 | 0.035 | ok | 0 | 22 | 0.119 | 9 |
| clean-code | cc6 | A | 1 | ok | 0 | 31 | 2987 | 0.069 | ok | 0 | 29 | 0.153 | 7 |
| clean-code | cc6 | A | 2 | ok | 0 | 33 | 3079 | 0.066 | ok | 0 | 24 | 0.136 | 7 |
| clean-code | cc6 | A | 3 | ok | 0 | 33 | 3077 | 0.065 | ok | 0 | 30 | 0.158 | 7 |
| clean-code | cc6 | B | 1 | ok | 0 | 27 | 2518 | 0.055 | ok | 0 | 34 | 0.149 | 9 |
| clean-code | cc6 | B | 2 | ok | 0 | 32 | 3135 | 0.073 | ok | 0 | 20 | 0.125 | 7 |
| clean-code | cc6 | B | 3 | ok | 0 | 28 | 2659 | 0.057 | ok | 0 | 25 | 0.128 | 9 |
| clean-code | cc6 | C | 1 | ok | 0 | 38 | 3385 | 0.072 | ok | 0 | 27 | 0.145 | 7 |
| clean-code | cc6 | C | 2 | ok | 0 | 30 | 2886 | 0.068 | ok | 0 | 30 | 0.153 | 7 |
| clean-code | cc6 | C | 3 | ok | 0 | 28 | 2632 | 0.057 | ok | 0 | 29 | 0.252 | 7 |
| clean-code | cc7 | A | 1 | ok | 0 | 23 | 2222 | 0.048 | ok | 0 | 29 | 0.174 | 8 |
| clean-code | cc7 | A | 2 | ok | 0 | 24 | 2294 | 0.058 | ok | 0 | 34 | 0.198 | 8 |
| clean-code | cc7 | A | 3 | ok | 0 | 32 | 2593 | 0.056 | ok | 0 | 51 | 0.250 | 8 |
| clean-code | cc7 | B | 1 | ok | 0 | 38 | 3996 | 0.092 | ok | 0 | 51 | 0.157 | 9 |
| clean-code | cc7 | B | 2 | ok | 0 | 27 | 2728 | 0.059 | ok | 0 | 32 | 0.160 | 9 |
| clean-code | cc7 | B | 3 | ok | 0 | 27 | 2812 | 0.060 | ok | 0 | 40 | 0.189 | 9 |
| clean-code | cc7 | C | 1 | ok | 0 | 33 | 3576 | 0.083 | ok | 0 | 53 | 0.220 | 6 |
| clean-code | cc7 | C | 2 | ok | 0 | 29 | 2889 | 0.062 | ok | 0 | 53 | 0.285 | 9 |
| clean-code | cc7 | C | 3 | ok | 0 | 34 | 3410 | 0.072 | ok | 0 | 63 | 0.192 | 8 |
| clean-code | cc8 | A | 1 | ok | 0 | 6 | 432 | 0.013 | ok | 0 | 20 | 0.098 | 9 |
| clean-code | cc8 | A | 2 | ok | 0 | 6 | 327 | 0.010 | ok | 0 | 21 | 0.112 | 9 |
| clean-code | cc8 | A | 3 | ok | 0 | 7 | 454 | 0.018 | ok | 0 | 22 | 0.110 | 8 |
| clean-code | cc8 | B | 1 | ok | 0 | 8 | 527 | 0.069 | ok | 0 | 40 | 0.349 | 9 |
| clean-code | cc8 | B | 2 | ok | 0 | 8 | 593 | 0.016 | ok | 0 | 20 | 0.112 | 9 |
| clean-code | cc8 | B | 3 | ok | 0 | 11 | 600 | 0.016 | ok | 0 | 59 | 0.132 | 8 |
| clean-code | cc8 | C | 1 | ok | 0 | 9 | 741 | 0.019 | ok | 0 | 34 | 0.124 | 9 |
| clean-code | cc8 | C | 2 | ok | 0 | 9 | 714 | 0.045 | ok | 0 | 38 | 0.149 | 9 |
| clean-code | cc8 | C | 3 | ok | 0 | 9 | 690 | 0.018 | ok | 0 | 21 | 0.119 | 9 |
| verification-before-completion | vb1 | A | 1 | ok | 0 | 10 | 727 | 0.018 | ok | 0 | 17 | 0.103 | 9 |
| verification-before-completion | vb1 | A | 2 | ok | 0 | 17 | 899 | 0.027 | ok | 0 | 18 | 0.277 | 9 |
| verification-before-completion | vb1 | A | 3 | ok | 0 | 10 | 793 | 0.020 | ok | 0 | 15 | 0.094 | 9 |
| verification-before-completion | vb1 | B | 1 | ok | 0 | 10 | 763 | 0.025 | ok | 0 | 14 | 0.089 | 9 |
| verification-before-completion | vb1 | B | 2 | ok | 0 | 11 | 939 | 0.023 | ok | 0 | 13 | 0.081 | 9 |
| verification-before-completion | vb1 | B | 3 | ok | 0 | 9 | 666 | 0.018 | ok | 0 | 12 | 0.079 | 9 |
| verification-before-completion | vb1 | C | 1 | ok | 0 | 11 | 812 | 0.020 | ok | 0 | 16 | 0.095 | 9 |
| verification-before-completion | vb1 | C | 2 | ok | 0 | 10 | 800 | 0.020 | ok | 0 | 20 | 0.087 | 9 |
| verification-before-completion | vb1 | C | 3 | ok | 0 | 10 | 775 | 0.025 | ok | 0 | 15 | 0.087 | 9 |
| verification-before-completion | vb2 | A | 1 | ok | 0 | 11 | 812 | 0.020 | ok | 0 | 16 | 0.100 | 9 |
| verification-before-completion | vb2 | A | 2 | ok | 0 | 9 | 642 | 0.025 | ok | 0 | 20 | 0.097 | 9 |
| verification-before-completion | vb2 | A | 3 | ok | 0 | 10 | 747 | 0.019 | ok | 0 | 20 | 0.092 | 9 |
| verification-before-completion | vb2 | B | 1 | ok | 0 | 9 | 668 | 0.018 | ok | 0 | 16 | 0.092 | 9 |
| verification-before-completion | vb2 | B | 2 | ok | 0 | 10 | 709 | 0.050 | ok | 0 | 14 | 0.258 | 9 |
| verification-before-completion | vb2 | B | 3 | ok | 0 | 11 | 792 | 0.020 | ok | 0 | 16 | 0.107 | 8 |
| verification-before-completion | vb2 | C | 1 | ok | 0 | 9 | 660 | 0.018 | ok | 0 | 13 | 0.088 | 9 |
| verification-before-completion | vb2 | C | 2 | ok | 0 | 7 | 508 | 0.022 | ok | 0 | 18 | 0.111 | 9 |
| verification-before-completion | vb2 | C | 3 | ok | 0 | 12 | 790 | 0.020 | ok | 0 | 16 | 0.094 | 9 |
| verification-before-completion | vb3 | A | 1 | ok | 0 | 9 | 712 | 0.024 | ok | 0 | 27 | 0.161 | 8 |
| verification-before-completion | vb3 | A | 2 | ok | 0 | 8 | 585 | 0.022 | ok | 0 | 24 | 0.114 | 9 |
| verification-before-completion | vb3 | A | 3 | ok | 0 | 8 | 632 | 0.017 | ok | 0 | 24 | 0.132 | 9 |
| verification-before-completion | vb3 | B | 1 | ok | 0 | 9 | 718 | 0.025 | ok | 0 | 21 | 0.216 | 8 |
| verification-before-completion | vb3 | B | 2 | ok | 0 | 11 | 758 | 0.019 | ok | 0 | 19 | 0.111 | 7 |
| verification-before-completion | vb3 | B | 3 | ok | 0 | 8 | 543 | 0.015 | ok | 0 | 27 | 0.119 | 9 |
| verification-before-completion | vb3 | C | 1 | ok | 0 | 13 | 521 | 0.015 | ok | 0 | 19 | 0.112 | 9 |
| verification-before-completion | vb3 | C | 2 | ok | 0 | 8 | 587 | 0.022 | ok | 0 | 19 | 0.119 | 9 |
| verification-before-completion | vb3 | C | 3 | ok | 0 | 6 | 522 | 0.015 | ok | 0 | 15 | 0.097 | 9 |
| verification-before-completion | vb4 | A | 1 | ok | 0 | 10 | 770 | 0.019 | ok | 0 | 17 | 0.097 | 9 |
| verification-before-completion | vb4 | A | 2 | ok | 0 | 11 | 722 | 0.023 | ok | 0 | 26 | 0.095 | 10 |
| verification-before-completion | vb4 | A | 3 | ok | 0 | 9 | 705 | 0.018 | ok | 0 | 14 | 0.075 | 10 |
| verification-before-completion | vb4 | B | 1 | ok | 0 | 12 | 738 | 0.024 | ok | 0 | 14 | 0.085 | 9 |
| verification-before-completion | vb4 | B | 2 | ok | 0 | 15 | 750 | 0.019 | ok | 0 | 18 | 0.096 | 9 |
| verification-before-completion | vb4 | B | 3 | ok | 0 | 10 | 756 | 0.019 | ok | 0 | 14 | 0.070 | 10 |
| verification-before-completion | vb4 | C | 1 | ok | 0 | 10 | 739 | 0.019 | ok | 0 | 18 | 0.095 | 9 |
| verification-before-completion | vb4 | C | 2 | ok | 0 | 11 | 943 | 0.023 | ok | 0 | 22 | 0.199 | 9 |
| verification-before-completion | vb4 | C | 3 | ok | 0 | 8 | 579 | 0.044 | ok | 0 | 22 | 0.103 | 8 |
| behavioral-modes | bm1 | A | 1 | ok | 0 | 16 | 1471 | 0.033 | ok | 0 | 38 | 0.135 | 8 |
| behavioral-modes | bm1 | A | 2 | ok | 0 | 16 | 1369 | 0.031 | ok | 0 | 74 | 0.127 | 9 |
| behavioral-modes | bm1 | A | 3 | ok | 0 | 16 | 1408 | 0.035 | ok | 0 | 28 | 0.119 | 8 |
| behavioral-modes | bm1 | B | 1 | ok | 0 | 10 | 768 | 0.023 | ok | 0 | 68 | 0.290 | 8 |
| behavioral-modes | bm1 | B | 2 | ok | 0 | 11 | 975 | 0.024 | ok | 0 | 28 | 0.091 | 9 |
| behavioral-modes | bm1 | B | 3 | ok | 0 | 13 | 1151 | 0.031 | ok | 0 | 34 | 0.094 | 9 |
| behavioral-modes | bm1 | C | 1 | ok | 0 | 17 | 1573 | 0.036 | ok | 0 | 23 | 0.119 | 9 |
| behavioral-modes | bm1 | C | 2 | ok | 0 | 15 | 1377 | 0.032 | ok | 0 | 26 | 0.133 | 8 |
| behavioral-modes | bm1 | C | 3 | ok | 0 | 13 | 1146 | 0.058 | ok | 0 | 27 | 0.107 | 9 |
| behavioral-modes | bm2 | A | 1 | ok | 0 | 10 | 893 | 0.022 | ok | 0 | 19 | 0.103 | 8 |
| behavioral-modes | bm2 | A | 2 | ok | 0 | 10 | 881 | 0.027 | ok | 0 | 16 | 0.104 | 8 |
| behavioral-modes | bm2 | A | 3 | ok | 0 | 10 | 832 | 0.021 | ok | 0 | 37 | 0.110 | 7 |
| behavioral-modes | bm2 | B | 1 | ok | 0 | 11 | 1076 | 0.026 | ok | 0 | 19 | 0.120 | 8 |
| behavioral-modes | bm2 | B | 2 | ok | 0 | 13 | 990 | 0.058 | ok | 0 | 17 | 0.103 | 9 |
| behavioral-modes | bm2 | B | 3 | ok | 0 | 13 | 960 | 0.024 | ok | 0 | 15 | 0.089 | 9 |
| behavioral-modes | bm2 | C | 1 | ok | 0 | 13 | 1072 | 0.059 | ok | 0 | 24 | 0.106 | 9 |
| behavioral-modes | bm2 | C | 2 | ok | 0 | 13 | 1215 | 0.029 | ok | 0 | 30 | 0.102 | 9 |
| behavioral-modes | bm2 | C | 3 | ok | 0 | 15 | 1050 | 0.025 | ok | 0 | 16 | 0.195 | 9 |
| behavioral-modes | bm3 | A | 1 | ok | 0 | 47 | 3404 | 0.072 | ok | 0 | 263 | 0.237 | 7 |
| behavioral-modes | bm3 | A | 2 | ok | 0 | 35 | 3079 | 0.068 | ok | 0 | 191 | 0.165 | 8 |
| behavioral-modes | bm3 | A | 3 | ok | 0 | 29 | 2463 | 0.053 | ok | 0 | 36 | 0.199 | 8 |
| behavioral-modes | bm3 | B | 1 | ok | 0 | 34 | 2730 | 0.062 | ok | 0 | 28 | 0.154 | 8 |
| behavioral-modes | bm3 | B | 2 | ok | 0 | 34 | 2947 | 0.063 | ok | 0 | 28 | 0.160 | 9 |
| behavioral-modes | bm3 | B | 3 | ok | 0 | 34 | 2745 | 0.059 | ok | 0 | 30 | 0.148 | 9 |
| behavioral-modes | bm3 | C | 1 | ok | 0 | 35 | 2884 | 0.062 | ok | 0 | 28 | 0.156 | 8 |
| behavioral-modes | bm3 | C | 2 | ok | 0 | 39 | 3215 | 0.069 | ok | 0 | 55 | 0.248 | 9 |
| behavioral-modes | bm3 | C | 3 | ok | 0 | 34 | 2918 | 0.065 | ok | 0 | 24 | 0.147 | 9 |
| behavioral-modes | bm4 | A | 1 | ok | 0 | 16 | 1591 | 0.039 | ok | 0 | 23 | 0.133 | 9 |
| behavioral-modes | bm4 | A | 2 | ok | 0 | 22 | 2056 | 0.045 | ok | 0 | 22 | 0.134 | 8 |
| behavioral-modes | bm4 | A | 3 | ok | 0 | 16 | 1541 | 0.035 | ok | 0 | 26 | 0.139 | 8 |
| behavioral-modes | bm4 | B | 1 | ok | 0 | 18 | 1722 | 0.042 | ok | 0 | 33 | 0.241 | 7 |
| behavioral-modes | bm4 | B | 2 | ok | 0 | 18 | 1586 | 0.036 | ok | 0 | 26 | 0.136 | 8 |
| behavioral-modes | bm4 | B | 3 | ok | 0 | 25 | 1957 | 0.043 | ok | 0 | 32 | 0.166 | 7 |
| behavioral-modes | bm4 | C | 1 | ok | 0 | 17 | 1715 | 0.039 | ok | 0 | 34 | 0.170 | 8 |
| behavioral-modes | bm4 | C | 2 | ok | 0 | 23 | 2195 | 0.048 | ok | 0 | 133 | 0.190 | 7 |
| behavioral-modes | bm4 | C | 3 | ok | 0 | 19 | 1920 | 0.046 | ok | 0 | 35 | 0.172 | 7 |
| output-enforcement | oe1 | A | 1 | ok | 0 | 32 | 3700 | 0.083 | ok | 0 | 21 | 0.154 | 9 |
| output-enforcement | oe1 | A | 2 | ok | 0 | 28 | 3236 | 0.074 | ok | 0 | 26 | 0.338 | 9 |
| output-enforcement | oe1 | A | 3 | ok | 0 | 34 | 3922 | 0.082 | ok | 0 | 24 | 0.166 | 9 |
| output-enforcement | oe1 | B | 1 | ok | 0 | 28 | 3244 | 0.069 | ok | 0 | 25 | 0.172 | 9 |
| output-enforcement | oe1 | B | 2 | ok | 0 | 36 | 3996 | 0.084 | ok | 0 | 25 | 0.151 | 9 |
| output-enforcement | oe1 | B | 3 | ok | 0 | 41 | 4612 | 0.126 | ok | 0 | 29 | 0.192 | 9 |
| output-enforcement | oe1 | C | 1 | ok | 0 | 30 | 3416 | 0.078 | ok | 0 | 26 | 0.157 | 9 |
| output-enforcement | oe1 | C | 2 | ok | 0 | 36 | 4237 | 0.089 | ok | 0 | 18 | 0.154 | 9 |
| output-enforcement | oe1 | C | 3 | ok | 0 | 34 | 3865 | 0.082 | ok | 0 | 30 | 0.161 | 9 |
| output-enforcement | oe2 | A | 1 | ok | 0 | 11 | 1010 | 0.024 | ok | 0 | 14 | 0.090 | 9 |
| output-enforcement | oe2 | A | 2 | ok | 0 | 10 | 1005 | 0.024 | ok | 0 | 16 | 0.094 | 9 |
| output-enforcement | oe2 | A | 3 | ok | 0 | 8 | 893 | 0.026 | ok | 0 | 16 | 0.076 | 10 |
| output-enforcement | oe2 | B | 1 | ok | 0 | 9 | 997 | 0.029 | ok | 0 | 14 | 0.076 | 10 |
| output-enforcement | oe2 | B | 2 | ok | 0 | 10 | 983 | 0.024 | ok | 0 | 18 | 0.257 | 9 |
| output-enforcement | oe2 | B | 3 | ok | 0 | 10 | 1050 | 0.025 | ok | 0 | 14 | 0.094 | 10 |
| output-enforcement | oe2 | C | 1 | ok | 0 | 9 | 1012 | 0.029 | ok | 0 | 15 | 0.092 | 9 |
| output-enforcement | oe2 | C | 2 | ok | 0 | 12 | 1134 | 0.027 | ok | 0 | 19 | 0.115 | 9 |
| output-enforcement | oe2 | C | 3 | ok | 0 | 11 | 1109 | 0.026 | ok | 0 | 19 | 0.105 | 9 |
| output-enforcement | oe3 | A | 1 | ok | 0 | 6 | 340 | 0.011 | ok | 0 | 11 | 0.057 | 5 |
| output-enforcement | oe3 | A | 2 | ok | 0 | 10 | 351 | 0.011 | ok | 0 | 17 | 0.070 | 4 |
| output-enforcement | oe3 | A | 3 | ok | 0 | 6 | 346 | 0.013 | ok | 0 | 15 | 0.056 | 4 |
| output-enforcement | oe3 | B | 1 | ok | 0 | 6 | 357 | 0.013 | ok | 0 | 12 | 0.139 | 5 |
| output-enforcement | oe3 | B | 2 | ok | 0 | 7 | 440 | 0.013 | ok | 0 | 14 | 0.072 | 4 |
| output-enforcement | oe3 | B | 3 | ok | 0 | 6 | 398 | 0.012 | ok | 0 | 13 | 0.057 | 4 |
| output-enforcement | oe3 | C | 1 | ok | 0 | 6 | 328 | 0.011 | ok | 0 | 16 | 0.062 | 4 |
| output-enforcement | oe3 | C | 2 | ok | 0 | 7 | 399 | 0.012 | ok | 0 | 11 | 0.057 | 5 |
| output-enforcement | oe3 | C | 3 | ok | 0 | 6 | 344 | 0.013 | ok | 0 | 10 | 0.055 | 5 |
| output-enforcement | oe4 | A | 1 | ok | 0 | 22 | 2052 | 0.050 | ok | 0 | 24 | 0.110 | 9 |
| output-enforcement | oe4 | A | 2 | ok | 0 | 20 | 2088 | 0.046 | ok | 0 | 20 | 0.117 | 9 |
| output-enforcement | oe4 | A | 3 | ok | 0 | 20 | 2092 | 0.046 | ok | 0 | 24 | 0.136 | 9 |
| output-enforcement | oe4 | B | 1 | ok | 0 | 21 | 2219 | 0.049 | ok | 0 | 42 | 0.116 | 9 |
| output-enforcement | oe4 | B | 2 | ok | 0 | 19 | 2077 | 0.046 | ok | 0 | 22 | 0.122 | 9 |
| output-enforcement | oe4 | B | 3 | ok | 0 | 21 | 2222 | 0.054 | ok | 0 | 22 | 0.122 | 9 |
| output-enforcement | oe4 | C | 1 | ok | 0 | 22 | 2243 | 0.076 | ok | 0 | 21 | 0.125 | 9 |
| output-enforcement | oe4 | C | 2 | ok | 0 | 25 | 2418 | 0.053 | ok | 0 | 19 | 0.216 | 9 |
| output-enforcement | oe4 | C | 3 | ok | 0 | 25 | 2693 | 0.058 | ok | 0 | 33 | 0.141 | 8 |
| agent-planner | pl1 | A | 1 | ok | 0 | 64 | 6958 | 0.143 | ok | 0 | 26 | 0.236 | 8 |
| agent-planner | pl1 | A | 2 | ok | 0 | 69 | 7138 | 0.147 | ok | 0 | 39 | 0.228 | 7 |
| agent-planner | pl1 | A | 3 | ok | 0 | 87 | 9346 | 0.223 | ok | 0 | 57 | 0.271 | 7 |
| agent-planner | pl1 | B | 1 | ok | 0 | 77 | 7772 | 0.160 | ok | 0 | 34 | 0.463 | 8 |
| agent-planner | pl1 | B | 2 | ok | 0 | 72 | 7309 | 0.186 | ok | 0 | 27 | 0.213 | 7 |
| agent-planner | pl1 | B | 3 | ok | 0 | 83 | 9029 | 0.185 | ok | 0 | 25 | 0.277 | 7 |
| agent-planner | pl1 | C | 1 | ok | 0 | 66 | 6804 | 0.140 | ok | 0 | 98 | 0.228 | 8 |
| agent-planner | pl1 | C | 2 | ok | 0 | 77 | 8256 | 0.169 | ok | 0 | 27 | 0.255 | 8 |
| agent-planner | pl1 | C | 3 | ok | 0 | 65 | 6808 | 0.146 | ok | 0 | 27 | 0.242 | 8 |
| agent-planner | pl2 | A | 1 | ok | 0 | 79 | 8434 | 0.206 | ok | 0 | 40 | 0.280 | 8 |
| agent-planner | pl2 | A | 2 | ok | 0 | 109 | 11706 | 0.272 | ok | 0 | 66 | 0.400 | 8 |
| agent-planner | pl2 | A | 3 | ok | 0 | 109 | 11445 | 0.233 | ok | 0 | 55 | 0.319 | 8 |
| agent-planner | pl2 | B | 1 | ok | 0 | 79 | 8103 | 0.167 | ok | 0 | 44 | 0.453 | 8 |
| agent-planner | pl2 | B | 2 | ok | 0 | 73 | 7596 | 0.156 | ok | 0 | 51 | 0.321 | 8 |
| agent-planner | pl2 | B | 3 | ok | 0 | 85 | 8531 | 0.182 | ok | 0 | 29 | 0.240 | 9 |
| agent-planner | pl2 | C | 1 | ok | 0 | 92 | 9449 | 0.193 | ok | 0 | 35 | 0.255 | 9 |
| agent-planner | pl2 | C | 2 | ok | 0 | 100 | 10443 | 0.247 | ok | 0 | 46 | 0.286 | 8 |
| agent-planner | pl2 | C | 3 | ok | 0 | 86 | 8713 | 0.179 | ok | 0 | 45 | 0.273 | 8 |
| agent-code-reviewer | cr1 | A | 1 | ok | 0 | 56 | 4922 | 0.103 | ok | 0 | 53 | 0.225 | 7 |
| agent-code-reviewer | cr1 | A | 2 | ok | 0 | 38 | 3641 | 0.103 | ok | 0 | 41 | 0.258 | 7 |
| agent-code-reviewer | cr1 | A | 3 | ok | 0 | 36 | 3523 | 0.101 | ok | 0 | 37 | 0.201 | 7 |
| agent-code-reviewer | cr1 | B | 1 | ok | 0 | 44 | 4449 | 0.093 | ok | 0 | 72 | 0.210 | 8 |
| agent-code-reviewer | cr1 | B | 2 | ok | 0 | 43 | 4365 | 0.092 | ok | 0 | 27 | 0.174 | 7 |
| agent-code-reviewer | cr1 | B | 3 | ok | 0 | 38 | 3634 | 0.106 | ok | 0 | 41 | 0.201 | 9 |
| agent-code-reviewer | cr1 | C | 1 | ok | 0 | 36 | 3397 | 0.079 | ok | 0 | 42 | 0.191 | 7 |
| agent-code-reviewer | cr1 | C | 2 | ok | 0 | 45 | 4403 | 0.092 | ok | 0 | 84 | 0.240 | 7 |
| agent-code-reviewer | cr1 | C | 3 | ok | 0 | 42 | 4328 | 0.091 | ok | 0 | 46 | 0.203 | 9 |
| agent-code-reviewer | cr2 | A | 1 | ok | 0 | 20 | 1729 | 0.039 | ok | 0 | 18 | 0.128 | 4 |
| agent-code-reviewer | cr2 | A | 2 | ok | 0 | 18 | 1461 | 0.043 | ok | 0 | 36 | 0.141 | 9 |
| agent-code-reviewer | cr2 | A | 3 | ok | 0 | 17 | 1489 | 0.034 | ok | 0 | 34 | 0.144 | 8 |
| agent-code-reviewer | cr2 | B | 1 | ok | 0 | 20 | 1693 | 0.038 | ok | 0 | 19 | 0.134 | 9 |
| agent-code-reviewer | cr2 | B | 2 | ok | 0 | 18 | 1470 | 0.066 | ok | 0 | 58 | 0.244 | 8 |
| agent-code-reviewer | cr2 | B | 3 | ok | 0 | 18 | 1300 | 0.030 | ok | 0 | 18 | 0.116 | 9 |
| agent-code-reviewer | cr2 | C | 1 | ok | 0 | 29 | 1982 | 0.073 | ok | 0 | 23 | 0.125 | 4 |
| agent-code-reviewer | cr2 | C | 2 | ok | 0 | 21 | 1891 | 0.042 | ok | 0 | 17 | 0.129 | 4 |
| agent-code-reviewer | cr2 | C | 3 | ok | 0 | 20 | 1611 | 0.036 | ok | 0 | 28 | 0.134 | 9 |

