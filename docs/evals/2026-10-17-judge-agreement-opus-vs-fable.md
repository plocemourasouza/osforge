# Judge agreement — Opus 5.5 vs Fable 5.1 — 2026-10-17

The outcome evals (round 1 and round 2) were re-graded by `claude-fable-5-1` over the **same
cached executor outputs** (`claude-opus-5-5`), with the same blind, isolated `judge.py` recipe.
288 verdicts, all ok; isolation verified on every call (tools: StructuredOutput only, no MCP).
Cost ≈ US$49.8 CLI-equivalent (r1 21.78, r2 28.06), run as 6 parallel processes in ~19 min.

Reports per judge: `2026-10-17-claude-opus-5-5-skill-outcome{,-r2}.md` (Opus judge) and
`…{,-r2}-fable-judge.md` (Fable judge). Table produced by
`python3 scripts/evals/outcome/compare_judges.py --judge-dir judge-claude-fable-5-1`
(direction = sign of the delta with a ±0.25 dead band; "NO" can be two deltas inside noise).

| Round | Target | n pairs | Opus judge A/B/C | Fable judge A/B/C | mean abs gap | B−A direction agrees | C−B direction agrees | criterion flips |
|---|---|---|---|---|---|---|---|---|
| r1 | adversarial-review | 36 | 7.67/8.25/8.50 | 7.50/8.33/8.50 | 0.25 | yes | NO | 9 |
| r1 | clean-code | 36 | 8.50/8.17/8.25 | 8.67/8.58/8.58 | 0.47 | NO | yes | 11 |
| r1 | frontend-design | 36 | 8.00/8.25/8.92 | 8.17/8.25/8.92 | 0.17 | NO | yes | 4 |
| r2 | agent-code-reviewer | 18 | 7.67/8.67/7.17 | 7.00/8.33/6.67 | 0.72 | yes | yes | 3 |
| r2 | agent-planner | 18 | 8.33/8.50/8.50 | 7.67/7.83/8.17 | 0.56 | yes | NO | 0 |
| r2 | behavioral-modes | 36 | 7.83/8.67/8.25 | 8.00/8.33/8.42 | 0.28 | yes | NO | 11 |
| r2 | clean-code | 36 | 8.33/8.92/8.00 | 8.17/8.75/8.17 | 0.22 | yes | yes | 5 |
| r2 | output-enforcement | 36 | 8.00/8.08/8.00 | 7.92/8.00/7.83 | 0.22 | yes | yes | 6 |
| r2 | verification-before-completion | 36 | 9.00/8.58/9.00 | 9.08/8.75/8.92 | 0.33 | yes | NO | 5 |

## Do the decisions taken on the Opus verdicts hold?

| Decision (commit) | Opus judge | Fable judge | Holds? |
|---|---|---|---|
| adversarial-review → C (0fb36cd) | C 8.50 ≥ B 8.25 | C 8.50 ≥ B 8.33 | yes |
| clean-code r1 reduction (0fb36cd, superseded by v3.0) | C 8.25 ≈ B 8.17 | C 8.58 = B 8.58 | yes |
| frontend-design → C (0fb36cd) | C 8.92 > B 8.25 | C 8.92 > B 8.25 | yes |
| clean-code v3.0 kept over old text (4dafb78) | B 8.92 > C 8.00 | B 8.75 > C 8.17 (> spread) | yes |
| verification-before-completion → C (4dafb78) | C 9.00 ≥ B 8.58 | C 8.92 ≥ B 8.75 | yes |
| output-enforcement → C (4dafb78) | C 8.00 ≈ B 8.08 | C 7.83 ≈ B 8.00 (within spread) | yes |
| planner block → one line (4dafb78) | C 8.50 = B 8.50 | C 8.17 > B 7.83 | yes |
| behavioral-modes kept (4dafb78) | B 8.67 > C 8.25 | C 8.42 ≈ B 8.33 on score; C worse on `bm4.no_manufactured_high` (1/3 vs 2/3) and padding (0.58 vs 0.50) | yes — score tie, secondary still favours B |
| code-reviewer block kept (4dafb78) | B 8.67 > C 7.17 | B 8.33 > C 6.67 | yes |

**Every decision holds under the second judge.** Mean absolute score gap per pair is 0.17–0.72;
the judges never disagree on a direction outside the noise band. Fable grades agents harder
(planner −0.7, code-reviewer −0.5 on average) and scores no-skill clean-code slightly higher.

## What the second judge adds

- The main known limitation of rounds 1–2 — judge = executor model — is now bounded: a
  different, stronger model reaches the same verdicts on the same outputs.
- Secondary findings replicate: behavioral-modes prevention step (A 0/3 vs B/C 3/3 under both
  judges); clean-code v3.0's convention rules; code-reviewer block best on the clean diff.
- Fable is ~5× the Opus judge cost per verdict (≈US$0.17–0.35 vs ≈US$0.06). For future rounds,
  Opus as the default judge with Fable as a spot-check on contested targets is enough.
