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
