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
