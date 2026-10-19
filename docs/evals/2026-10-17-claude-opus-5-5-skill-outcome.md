# Skill outcome eval — claude-opus-5-5 — 2026-10-17

| Field | Value |
|---|---|
| Suite | `outcome` (with-skill vs without-skill vs reduced-skill) |
| Executor model | `claude-opus-5-5` |
| Judge model | `claude-opus-5-5` via `scripts/lib/judge.py` (blind, isolated) |
| Repo | `58c47e3` on `fix/route-guard-transcript-race`; `skills/` clean |
| CLI | `2.1.302 (Claude Code)` |
| Runs per cell | 3 (3 skills × 4 tasks × 3 arms × 3 = 108 executor + 108 judge calls planned) |
| Command | `python3 scripts/evals/outcome/driver.py --report docs/evals/2026-10-17-claude-opus-5-5-skill-outcome.md --model claude-opus-5-5` (run: `driver.py --run --model claude-opus-5-5 --runs 3 --concurrency 4`) |
| Wall time | executor phase 1199s, judge phase 339s (concurrency 4) |
| Early stop | none |

**Call status.** Executor: ok 108. Judge: ok 108. Subscription quota, cost shown as the CLI's USD-equivalent: executor 11.18, judge 6.85.

**How to read.** A run *passes* a task when every critical criterion of that task's rubric passes. Per task and arm, **PASS** is k = N, **FLAKY** 0 < k < N, **FAIL** k = 0 (docs/evals/README.md). *Score* is the judge's 0–10. *Run spread* = max − min of the per-run mean score (mean over the 4 tasks of run r, r = 1..3): the run-to-run noise of that arm. A delta is called **real** only when |Δ| exceeds the larger run spread of the two arms compared.

## clean-code

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A control | 12 | 8.50 | 1.24 | 8.25 / 8.75 / 8.50 | 0.50 | 12/12 | 95 | 6412 | 2072 | 21 |
| B current | 12 | 8.17 | 1.47 | 8.25 / 7.75 / 8.50 | 0.75 | 12/12 | 4387 | 8105 | 2860 | 29 |
| C reduced | 12 | 8.25 | 1.36 | 8.00 / 8.25 / 8.50 | 0.50 | 12/12 | 3850 | 7878 | 3152 | 31 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | -0.33 | 0.75 | no |
| C − B | 0.08 | 0.75 | no |
| C − A | -0.25 | 0.50 | no |

**Computed verdict:** skill neutral (B − A within run spread). **Reduced variant:** C ≈ B within noise — the audit's cuts are safe on this task set.

### Per task (k/N runs passing criticals · mean score)

| Task | A control | B current | C reduced |
|---|---|---|---|
| `cc1` | PASS 3/3 · 7.0 | PASS 3/3 · 6.0 | PASS 3/3 · 6.3 |
| `cc2` | PASS 3/3 · 9.0 | PASS 3/3 · 9.0 | PASS 3/3 · 9.0 |
| `cc3` | PASS 3/3 · 8.0 | PASS 3/3 · 8.3 | PASS 3/3 · 8.0 |
| `cc4` | PASS 3/3 · 10.0 | PASS 3/3 · 9.3 | PASS 3/3 · 9.7 |

### Per-criterion pass rate (pass / (pass + fail); `na` excluded; * = critical)

| Criterion | A | B | C |
|---|---|---|---|
| `cc1.behavior`* | 3/3 | 3/3 | 3/3 |
| `cc1.simplified` | 3/3 | 3/3 | 3/3 |
| `cc1.no_new_abstraction` | 1/3 | 0/3 | 0/3 |
| `cc1.call_site` | 3/3 | 3/3 | 3/3 |
| `cc1.proportionate` | 1/3 | 0/3 | 0/3 |
| `cc2.nesting` | 3/3 | 3/3 | 3/3 |
| `cc2.duplication` | 3/3 | 3/3 | 3/3 |
| `cc2.side_effect` | 3/3 | 3/3 | 3/3 |
| `cc2.behavior`* | 3/3 | 3/3 | 3/3 |
| `cc2.no_new_abstraction` | 3/3 | 3/3 | 3/3 |
| `cc2.magic_numbers` | 3/3 | 3/3 | 3/3 |
| `cc3.root_cause`* | 3/3 | 3/3 | 3/3 |
| `cc3.fix_correct`* | 3/3 | 3/3 | 3/3 |
| `cc3.signature` | 3/3 | 3/3 | 3/3 |
| `cc3.concise_explanation` | 0/3 | 1/3 | 0/3 |
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
| A control | 12 | 8.00 | 1.71 | 8.00 / 8.25 / 7.75 | 0.50 | 11/12 | 95 | 6148 | 9454 | 76 |
| B current | 12 | 8.25 | 0.62 | 8.50 / 8.00 / 8.25 | 0.50 | 12/12 | 14700 | 12023 | 7754 | 66 |
| C reduced | 12 | 8.92 | 0.29 | 9.00 / 9.00 / 8.75 | 0.25 | 12/12 | 14705 | 11868 | 9094 | 77 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | 0.25 | 0.50 | no |
| C − B | 0.67 | 0.50 | yes |
| C − A | 0.92 | 0.50 | yes |

**Computed verdict:** skill neutral (B − A within run spread). **Reduced variant:** C > B beyond run spread — the audit's cuts are safe and improve this task set.

### Per task (k/N runs passing criticals · mean score)

| Task | A control | B current | C reduced |
|---|---|---|---|
| `fd1` | PASS 3/3 · 8.7 | PASS 3/3 · 8.3 | PASS 3/3 · 9.0 |
| `fd2` | PASS 3/3 · 9.0 | PASS 3/3 · 8.0 | PASS 3/3 · 8.7 |
| `fd3` | PASS 3/3 · 9.0 | PASS 3/3 · 9.0 | PASS 3/3 · 9.0 |
| `fd4` | FLAKY 2/3 · 5.3 | PASS 3/3 · 7.7 | PASS 3/3 · 9.0 |

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
| `fd3.actions` | 3/3 | 3/3 | 3/3 |
| `fd3.explains_value` | 3/3 | 3/3 | 3/3 |
| `fd3.is_empty` | 3/3 | 3/3 | 3/3 |
| `fd3.brand` | 3/3 | 3/3 | 3/3 |
| `fd3.responsive` | 3/3 | 3/3 | 3/3 |
| `fd3.accessible` | 3/3 | 3/3 | 3/3 |
| `fd4.handles_ambiguity`* | 2/3 | 3/3 | 3/3 |
| `fd4.questions_focused` | 1/1 | 3/3 | 2/2 |
| `fd4.markup_valid` | 3/3 | – | 3/3 |
| `fd4.coherent` | 2/3 | – | 3/3 |
| `fd4.low_friction` | 3/3 | 3/3 | 3/3 |

### AI-default tells present (mean per graded page-task; lower is better)

| Arm | Mean tells / answer | Most frequent |
|---|---|---|
| A | 1.50 (n=12) | T2_italic_accent 5, T4_mono_eyebrow 3, T6_purple_or_neon 3, T7_gradient_blobs 3, T10_ai_copy 3 |
| B | 1.08 (n=12) | T2_italic_accent 5, T1_cream_bg 4, T4_mono_eyebrow 4 |
| C | 0.17 (n=12) | T2_italic_accent 2 |

Named Opus defaults added to C's avoid-table (count of answers showing each): T1_cream_bg A=0 B=4 C=0; T2_italic_accent A=5 B=5 C=2; T3_numbered_labels A=0 B=0 C=0; T4_mono_eyebrow A=3 B=4 C=0; T5_pill_everywhere A=1 B=0 C=0.

## adversarial-review

| Arm | Graded | Mean score | SD | Run means | Run spread | Runs passing criticals | Sys-prompt chars | Mean input tok | Mean output tok | Mean wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| A control | 12 | 7.67 | 2.06 | 7.50 / 7.75 / 7.75 | 0.25 | 7/12 | 95 | 6254 | 2060 | 23 |
| B current | 12 | 8.25 | 1.54 | 8.00 / 8.00 / 8.75 | 0.75 | 10/12 | 6640 | 8521 | 3130 | 37 |
| C reduced | 12 | 8.50 | 1.38 | 8.50 / 8.50 / 8.50 | 0.00 | 12/12 | 6530 | 8474 | 3106 | 33 |

| Delta | Value | Noise bound (max run spread) | Real? |
|---|---|---|---|
| B − A | 0.58 | 0.75 | no |
| C − B | 0.25 | 0.75 | no |
| C − A | 0.83 | 0.25 | yes |

**Computed verdict:** skill neutral (B − A within run spread). **Reduced variant:** C ≈ B within noise — the audit's cuts are safe on this task set.

### Per task (k/N runs passing criticals · mean score)

| Task | A control | B current | C reduced |
|---|---|---|---|
| `ar1` | PASS 3/3 · 9.0 | PASS 3/3 · 9.0 | PASS 3/3 · 9.0 |
| `ar2` | FAIL 0/3 · 4.3 | FLAKY 1/3 · 6.0 | PASS 3/3 · 6.3 |
| `ar3` | PASS 3/3 · 9.0 | PASS 3/3 · 9.0 | PASS 3/3 · 9.3 |
| `ar4` | FLAKY 1/3 · 8.3 | PASS 3/3 · 9.0 | PASS 3/3 · 9.3 |

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
| `ar2.no_blocking_findings`* | 0/3 | 1/3 | 3/3 |
| `ar2.clear_verdict` | 1/3 | 1/3 | 2/3 |
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
| `ar4.no_manufactured_high`* | 1/3 | 3/3 | 3/3 |
| `ar4.prioritized` | 3/3 | 3/3 | 3/3 |

### Recall of seeded defects and manufactured findings

| Arm | Seeded recall | Manufactured findings (mean / answer) | Manufactured rated Critical/Important (total) | Total findings (mean) | `ar2` (clean spec) total findings (mean) |
|---|---|---|---|---|---|
| A | 15/15 | 2.17 | 11 | 8.8 | 7.3 |
| B | 15/15 | 0.67 | 2 | 6.6 | 4.0 |
| C | 15/15 | 0.67 | 0 | 5.5 | 4.0 |

## Summary

| Skill | A mean ± run spread | B mean ± run spread | C mean ± run spread | B − A | C − B | Verdict | C ≥ B? |
|---|---|---|---|---|---|---|---|
| `clean-code` | 8.50 ± 0.50 | 8.17 ± 0.75 | 8.25 ± 0.50 | -0.33 | 0.08 | skill neutral | C ≈ B within noise |
| `frontend-design` | 8.00 ± 0.50 | 8.25 ± 0.50 | 8.92 ± 0.25 | 0.25 | 0.67 | skill neutral | C > B beyond run spread |
| `adversarial-review` | 7.67 ± 0.25 | 8.25 ± 0.75 | 8.50 ± 0.00 | 0.58 | 0.25 | skill neutral | C ≈ B within noise |

## Interpretation and limitations (hand-written, from the tables above)

## Interpretation

**Mean score.** No skill clears the noise bound against the control (B − A within the larger
run spread for all three). On this task set, Opus 5.5 without the skill text already scores
7.7–8.5/10. The reduced variant C is ≥ B for all three skills; for frontend-design C > B beyond
the spread.

**Where the skill text does change behaviour** (secondary metrics, not the mean):

- **adversarial-review — false positives.** Every arm found all 15 seeded defects. Manufactured
  findings per answer: A 2.17, B 0.67, C 0.67; manufactured findings rated Critical/Important:
  A 11, B 2, C 0. On the clean spec (`ar2`) "no blocking findings" passed A 0/3, B 1/3, C 3/3.
  Removing the cynical persona ("EXPECT to find problems", "ASSUME problems exist") lowered
  severity inflation without losing recall. One task carries most of this signal.
- **frontend-design — AI-default tells per page:** A 1.50, B 1.08, C 0.17. The underspecified
  task passed A 2/3, B 3/3, C 3/3. Caveat: C's avoid-table names exactly the tells the judge
  counts — part of C's gain is teaching to the test. B produced *more* cream backgrounds (4 vs 0)
  and monospace eyebrow labels (4 vs 3) than A: the current text does not prevent the defaults
  Opus 5.5 falls back on, which is the gap the audit's additions target.
- **clean-code — no measurable benefit, higher cost.** Critical criteria 12/12 in every arm;
  B and C produced ~40–50% more output tokens (2.9–3.2k vs 2.1k). `cc1.no_new_abstraction` failed
  8/9 runs across all arms (every answer introduced a small `ShippingRate` type) — rubric too
  strict, criterion non-discriminating.

**Verdicts.**

| Skill | B vs A | C vs B | Decision |
|---|---|---|---|
| clean-code | neutral (−0.33) | ≥ (within noise) | Apply C; candidate for demotion from core (costs tokens, no measured gain) — needs harder tasks before deciding |
| frontend-design | neutral on mean; fewer tells | C > B | Apply C |
| adversarial-review | neutral on mean; far fewer false findings | ≥ (within noise) | Apply C |

## Limitations

- Single turn, no tools. The skills' reference files were unreachable in B and C
  (frontend-design points to seven).
- Skill text was injected via `--append-system-prompt`, not loaded through the Skill tool.
- Judge = executor model. Judging was blind (random ids, task + answer only, shuffled order); a
  scan of the answers found no arm-revealing wording. Same-model bias is not excluded.
- Rubrics and reduced variants were written in the same session (see the frontend-design overlap).
- 4 hand-picked tasks per skill, most criteria 3/3 in every arm — a ceiling that limits what the
  mean can show. n = 3 runs per cell.
- `~/.osforge/quota.json` is refreshed only by the interactive statusline, so the 80% stop could
  not fire from it; call streams showed the 5-hour window peaking at 9%.

