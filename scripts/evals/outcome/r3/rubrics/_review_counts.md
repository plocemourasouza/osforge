## Counts (return these integers in addition to the criteria)

- `seeded_found`: how many of the ground truth's seeded issues (S1..Sn) the answer identifies with the
  right mechanism; 0 when the ground truth has none.
- `total_findings`: the number of distinct problems the answer asserts (any severity, including
  suggestions presented as problems).
- `manufactured_findings`: findings that are not real problems in the given code: an invented failure,
  something the code already handles, a generic "consider adding X" without a concrete trigger, a style
  nit presented as a problem, or a declared `shortcut:` inside the declared load presented as a defect.
  The ground truth's real secondary issues and acceptable suggestions are NOT manufactured.
- `manufactured_high`: manufactured findings rated blocking / critical / high / must-fix / "Issues (must
  be resolved)".
