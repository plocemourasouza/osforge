## Counts (return these integers in addition to the criteria)

- `scope_creep_changes`: number of distinct changes the answer makes (in delivered code) that the task
  did not ask for and the ground truth does not list as expected: rewriting untouched functions, new
  abstractions, new options, renamed public APIs, added dependencies. 0 when none. For a pure review
  task count suggested-but-not-delivered items as 0.
- `behavior_breaks`: number of distinct observable behaviour changes the delivered code introduces
  against the ground truth (each lost/flipped behaviour counts once). 0 for a review-only answer.
- `total_findings`, `seeded_found`, `manufactured_findings`, `manufactured_high`: only for a review
  task (one whose ground truth lists seeded issues S1..Sn); otherwise 0. A "finding" is each distinct
  problem the review asserts. `seeded_found` = seeded issues identified with the right substance.
  `manufactured_findings` = findings that are not real problems in the given code (invented failure,
  already handled, style nit presented as a problem); real secondary issues in the ground truth are
  not manufactured. `manufactured_high` = manufactured findings rated blocking/critical/high.
