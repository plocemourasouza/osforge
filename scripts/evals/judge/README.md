# scripts/evals/judge/

The first consumers of `scripts/lib/judge.py` (B-029, `docs/intake/laya/SPEC-L02-juiz-isolado.md`).

- `e4/` -- rubric + schema for **E4** (reviewer leniency): did a review (`adversarial-review`,
  `code-review`, ...) find the real problems in what it reviewed, or did it go lenient after
  B-004. Run: `python3 ../../lib/judge.py --model <id> --schema e4/schema-v1.json --rubric
  e4/rubric-v1.md --input <artifact-then-review.md>`. Consume `k` of `N` runs like B-010 --
  never a single verdict.
- `e-j0/` -- the E-J0 isolation experiment for `judge.py` itself: prepared, not run. See its
  own README before passing `--run`.
