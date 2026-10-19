## Counts (return these integers in addition to the criteria)

- `seeded_found`: how many of the ground truth's seeded items (B1..Bn bugs for a review, H1..Hn hidden
  dependencies for a plan) the answer identifies with the right mechanism; 0 when the ground truth has none.
- `total_findings`: for a review, the number of distinct problems asserted (any severity); for a plan, 0.
- `manufactured_findings`: for a review, findings that are not real problems in the given code (invented
  failure, already handled, generic "consider adding X" without a concrete trigger, style nit presented
  as a problem); real secondary issues in the ground truth are not manufactured. For a plan, the number of
  tasks/risks that address problems that do not exist in the given context.
- `manufactured_high`: manufactured findings rated blocking/critical/warning/must-fix (review only; 0 for a plan).
- `unflagged_assumptions`: for a plan, the number of material assumptions the plan relies on without
  stating them (e.g. silently choosing "current page" vs "all rows"); 0 for a review.
