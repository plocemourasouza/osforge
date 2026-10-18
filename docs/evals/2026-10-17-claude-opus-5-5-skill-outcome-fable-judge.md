# Skill outcome eval — claude-opus-5-5 — 2026-10-17

| Field | Value |
|---|---|
| Suite | `outcome` (with-skill vs without-skill vs reduced-skill) |
| Executor model | `claude-opus-5-5` |
| Judge model | `claude-fable-5-1` via `scripts/lib/judge.py` (blind, isolated) |
| Repo | `4dafb78` on `fix/route-guard-transcript-race`; `skills/` clean |
| CLI | `2.1.302 (Claude Code)` |
| Runs per cell | 3 (3 skills × 4 tasks × 3 arms × 3 = 108 executor + 108 judge calls planned) |
| Command | `python3 scripts/evals/outcome/driver.py --report docs/evals/2026-10-17-claude-opus-5-5-skill-outcome-fable-judge.md --round r1 --model claude-opus-5-5 --judge-model claude-fable-5-1` (run: `driver.py --run --model claude-opus-5-5 --runs 3 --concurrency 4`) |
| Wall time | executor phase 1199s, judge phase 339s (concurrency 4) |
| Early stop | none |

**Call status.** Executor: ok 108. Judge: ok 108. Subscription quota, cost shown as the CLI's USD-equivalent: executor 11.18, judge 21.78.

**How to read.** A run *passes* a task when every critical criterion of that task's rubric passes. Per task and arm, **PASS** is k = N, **FLAKY** 0 < k < N, **FAIL** k = 0 (docs/evals/README.md). *Score* is the judge's 0–10. *Run spread* = max − min of the per-run mean score (mean over the 4 tasks of run r, r = 1..3): the run-to-run noise of that arm. A delta is called **real** only when |Δ| exceeds the larger run spread of the two arms compared.

## clean-code

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A control | 12 | 8.67 | 1.15 | 8.50 / 9.25 / 8.25 | 1.00 | 12/12 | 95 | 6412 | 2072 | 21 |
| B current | 12 | 8.58 | 1.44 | 8.75 / 8.50 / 8.50 | 0.25 | 12/12 | 4387 | 8105 | 2860 | 29 |
| C reduced | 12 | 8.58 | 1.24 | 8.75 / 8.50 / 8.50 | 0.25 | 12/12 | 3850 | 7878 | 3152 | 31 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | -0.08 | 1.00 | no |
| C − B | 0.00 | 0.25 | no |
| C − A | -0.08 | 1.00 | no |

**Computed verdict:** skill neutral (B − A within run spread). **Reduced variant:** C ≈ B within noise — the audit's cuts are safe on this task set.

### Per task (k/N runs passing criticals · mean score)

| Task | A control | B current | C reduced |
|---|---|---|---|
| `cc1` | PASS 3/3 · 7.3 | PASS 3/3 · 6.3 | PASS 3/3 · 6.7 |
| `cc2` | PASS 3/3 · 9.0 | PASS 3/3 · 9.0 | PASS 3/3 · 9.0 |
| `cc3` | PASS 3/3 · 8.7 | PASS 3/3 · 9.0 | PASS 3/3 · 9.0 |
| `cc4` | PASS 3/3 · 9.7 | PASS 3/3 · 10.0 | PASS 3/3 · 9.7 |

### Per-criterion pass rate (pass / (pass + fail); `na` excluded; * = critical)

| Criterion | A | B | C |
|---|---|---|---|
| `cc1.behavior`* | 3/3 | 3/3 | 3/3 |
| `cc1.simplified` | 3/3 | 3/3 | 3/3 |
| `cc1.no_new_abstraction` | 1/3 | 0/3 | 0/3 |
| `cc1.call_site` | 3/3 | 3/3 | 3/3 |
| `cc1.proportionate` | 2/3 | 0/3 | 2/3 |
| `cc2.nesting` | 3/3 | 3/3 | 3/3 |
| `cc2.duplication` | 3/3 | 3/3 | 3/3 |
| `cc2.side_effect` | 3/3 | 3/3 | 3/3 |
| `cc2.behavior`* | 3/3 | 3/3 | 3/3 |
| `cc2.no_new_abstraction` | 3/3 | 3/3 | 3/3 |
| `cc2.magic_numbers` | 3/3 | 3/3 | 3/3 |
| `cc3.root_cause`* | 3/3 | 3/3 | 3/3 |
| `cc3.fix_correct`* | 3/3 | 3/3 | 3/3 |
| `cc3.signature` | 3/3 | 3/3 | 3/3 |
| `cc3.concise_explanation` | 3/3 | 3/3 | 3/3 |
| `cc3.no_scope_creep` | 3/3 | 3/3 | 3/3 |
| `cc4.behavior`* | 3/3 | 3/3 | 3/3 |
| `cc4.comments_removed` | 3/3 | 3/3 | 3/3 |
| `cc4.why_comment_kept` | 3/3 | 3/3 | 3/3 |
| `cc4.dead_code_removed` | 3/3 | 3/3 | 3/3 |
| `cc4.no_additions` | 3/3 | 3/3 | 3/3 |
| `cc4.accurate_list` | 3/3 | 3/3 | 3/3 |

## frontend-design

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A control | 12 | 8.17 | 1.53 | 8.25 / 8.25 / 8.00 | 0.25 | 11/12 | 95 | 6148 | 9454 | 76 |
| B current | 12 | 8.25 | 0.62 | 8.25 / 8.50 / 8.00 | 0.50 | 12/12 | 14700 | 12023 | 7754 | 66 |
| C reduced | 12 | 8.92 | 0.29 | 9.00 / 9.00 / 8.75 | 0.25 | 12/12 | 14705 | 11868 | 9094 | 77 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | 0.08 | 0.50 | no |
| C − B | 0.67 | 0.50 | yes |
| C − A | 0.75 | 0.25 | yes |

**Computed verdict:** skill neutral (B − A within run spread). **Reduced variant:** C > B beyond run spread — the audit's cuts are safe and improve this task set.

### Per task (k/N runs passing criticals · mean score)

| Task | A control | B current | C reduced |
|---|---|---|---|
| `fd1` | PASS 3/3 · 9.0 | PASS 3/3 · 8.3 | PASS 3/3 · 9.0 |
| `fd2` | PASS 3/3 · 9.0 | PASS 3/3 · 8.3 | PASS 3/3 · 8.7 |
| `fd3` | PASS 3/3 · 9.0 | PASS 3/3 · 8.7 | PASS 3/3 · 9.0 |
| `fd4` | FLAKY 2/3 · 5.7 | PASS 3/3 · 7.7 | PASS 3/3 · 9.0 |

### Per-criterion pass rate (pass / (pass + fail); `na` excluded; * = critical)

| Criterion | A | B | C |
|---|---|---|---|
| `fd1.markup_valid`* | 3/3 | 3/3 | 3/3 |
| `fd1.brand_color` | 3/3 | 3/3 | 3/3 |
| `fd1.typeface` | 3/3 | 3/3 | 3/3 |
| `fd1.copy_verbatim` | 3/3 | 3/3 | 3/3 |
| `fd1.mockup` | 3/3 | 3/3 | 3/3 |
| `fd1.audience_fit` | 3/3 | 3/3 | 3/3 |
| `fd1.responsive` | 3/3 | 3/3 | 3/3 |
| `fd1.accessible` | 3/3 | 3/3 | 3/3 |
| `fd1.no_unneeded_questions` | 3/3 | 3/3 | 3/3 |
| `fd2.markup_valid`* | 3/3 | 3/3 | 3/3 |
| `fd2.plans_exact` | 3/3 | 3/3 | 3/3 |
| `fd2.recommended` | 3/3 | 3/3 | 3/3 |
| `fd2.toggle_works` | 3/3 | 3/3 | 3/3 |
| `fd2.brand` | 3/3 | 3/3 | 3/3 |
| `fd2.faq` | 3/3 | 3/3 | 3/3 |
| `fd2.tone_fit` | 3/3 | 3/3 | 3/3 |
| `fd2.accessible` | 3/3 | 2/3 | 2/3 |
| `fd2.responsive` | 3/3 | 3/3 | 3/3 |
| `fd3.markup_valid`* | 3/3 | 3/3 | 3/3 |
| `fd3.shell` | 3/3 | 3/3 | 3/3 |
| `fd3.actions` | 3/3 | 2/3 | 3/3 |
| `fd3.explains_value` | 3/3 | 3/3 | 3/3 |
| `fd3.is_empty` | 3/3 | 3/3 | 3/3 |
| `fd3.brand` | 3/3 | 3/3 | 3/3 |
| `fd3.responsive` | 3/3 | 3/3 | 3/3 |
| `fd3.accessible` | 3/3 | 3/3 | 3/3 |
| `fd4.handles_ambiguity`* | 2/3 | 3/3 | 3/3 |
| `fd4.questions_focused` | – | 3/3 | 2/2 |
| `fd4.markup_valid` | 2/3 | – | 3/3 |
| `fd4.coherent` | 3/3 | – | 3/3 |
| `fd4.low_friction` | 3/3 | 3/3 | 3/3 |

### AI-default tells present (mean per graded page-task; lower is better)

| Arm | Mean tells / answer | Most frequent |
|---|---|---|
| A | 1.50 (n=12) | T2_italic_accent 5, T4_mono_eyebrow 3, T6_purple_or_neon 3, T7_gradient_blobs 3, T10_ai_copy 3 |
| B | 1.00 (n=12) | T2_italic_accent 4, T1_cream_bg 4, T4_mono_eyebrow 4 |
| C | 0.08 (n=12) | T2_italic_accent 1 |

Named Opus defaults added to C's avoid-table (count of answers showing each): T1_cream_bg A=0 B=4 C=0; T2_italic_accent A=5 B=4 C=1; T3_numbered_labels A=0 B=0 C=0; T4_mono_eyebrow A=3 B=4 C=0; T5_pill_everywhere A=1 B=0 C=0.

## adversarial-review

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A control | 12 | 7.50 | 1.98 | 7.50 / 7.75 / 7.25 | 0.50 | 9/12 | 95 | 6254 | 2060 | 23 |
| B current | 12 | 8.33 | 1.30 | 8.50 / 8.00 / 8.50 | 0.50 | 12/12 | 6640 | 8521 | 3130 | 37 |
| C reduced | 12 | 8.50 | 0.90 | 8.50 / 8.50 / 8.50 | 0.00 | 12/12 | 6530 | 8474 | 3106 | 33 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | 0.83 | 0.50 | yes |
| C − B | 0.17 | 0.50 | no |
| C − A | 1.00 | 0.50 | yes |

**Computed verdict:** skill helps (B > A beyond run spread). **Reduced variant:** C ≈ B within noise — the audit's cuts are safe on this task set.

### Per task (k/N runs passing criticals · mean score)

| Task | A control | B current | C reduced |
|---|---|---|---|
| `ar1` | PASS 3/3 · 8.7 | PASS 3/3 · 9.0 | PASS 3/3 · 9.0 |
| `ar2` | FLAKY 1/3 · 4.3 | PASS 3/3 · 6.3 | PASS 3/3 · 7.0 |
| `ar3` | PASS 3/3 · 9.0 | PASS 3/3 · 9.0 | PASS 3/3 · 9.0 |
| `ar4` | FLAKY 2/3 · 8.0 | PASS 3/3 · 9.0 | PASS 3/3 · 9.0 |

### Per-criterion pass rate (pass / (pass + fail); `na` excluded; * = critical)

| Criterion | A | B | C |
|---|---|---|---|
| `ar1.found_D1` | 3/3 | 3/3 | 3/3 |
| `ar1.found_D2` | 3/3 | 3/3 | 3/3 |
| `ar1.found_D3` | 3/3 | 3/3 | 3/3 |
| `ar1.severity_right` | 3/3 | 3/3 | 3/3 |
| `ar1.no_manufactured_high`* | 3/3 | 3/3 | 3/3 |
| `ar1.actionable` | 3/3 | 3/3 | 3/3 |
| `ar1.prioritized` | 3/3 | 3/3 | 3/3 |
| `ar2.no_blocking_findings`* | 1/3 | 3/3 | 3/3 |
| `ar2.clear_verdict` | 1/3 | 3/3 | 3/3 |
| `ar2.shows_work` | 3/3 | 3/3 | 3/3 |
| `ar2.low_noise` | 0/3 | 1/3 | 0/3 |
| `ar3.found_D1`* | 3/3 | 3/3 | 3/3 |
| `ar3.severity_right` | 3/3 | 3/3 | 3/3 |
| `ar3.found_drop_timing` | 3/3 | 3/3 | 3/3 |
| `ar3.no_manufactured_high`* | 3/3 | 3/3 | 3/3 |
| `ar3.actionable` | 3/3 | 3/3 | 3/3 |
| `ar4.found_D1`* | 3/3 | 3/3 | 3/3 |
| `ar4.severity_right` | 3/3 | 3/3 | 3/3 |
| `ar4.fix_right` | 3/3 | 3/3 | 3/3 |
| `ar4.no_manufactured_high`* | 2/3 | 3/3 | 3/3 |
| `ar4.prioritized` | 3/3 | 3/3 | 3/3 |

### Recall of seeded defects and manufactured findings

| Arm | Seeded recall | Manufactured findings (mean / answer) | Manufactured rated Critical/Important (total) | Total findings (mean) | `ar2` (clean spec) total findings (mean) |
|---|---|---|---|---|---|
| A | 15/15 | 2.42 | 7 | 8.0 | 7.3 |
| B | 15/15 | 1.08 | 0 | 6.6 | 4.0 |
| C | 15/15 | 0.83 | 0 | 5.5 | 4.0 |

## Summary

| Skill | A mean ± run spread | B mean ± run spread | C mean ± run spread | B − A | C − B | Verdict | C ≥ B? |
|---|---|---|---|---|---|---|---|
| `clean-code` | 8.67 ± 1.00 | 8.58 ± 0.25 | 8.58 ± 0.25 | -0.08 | 0.00 | skill neutral | C ≈ B within noise |
| `frontend-design` | 8.17 ± 0.25 | 8.25 ± 0.50 | 8.92 ± 0.25 | 0.08 | 0.67 | skill neutral | C > B beyond run spread |
| `adversarial-review` | 7.50 ± 0.50 | 8.33 ± 0.50 | 8.50 ± 0.00 | 0.83 | 0.17 | skill helps | C ≈ B within noise |

## Interpretation and limitations (hand-written, from the tables above)

## Interpretation

Same executor outputs as the Opus-judged report, re-graded by `claude-fable-5-1`. Cross-judge agreement and the check of every decision taken on the Opus verdicts: `docs/evals/2026-10-17-judge-agreement-opus-vs-fable.md`.

