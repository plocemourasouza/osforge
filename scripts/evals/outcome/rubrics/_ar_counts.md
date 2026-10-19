## Counting findings

A "finding" is each distinct problem the review asserts (a numbered/bulleted item or equivalent).
Also return:
- `total_findings`: how many findings the review lists at any severity.
- `seeded_found`: how many of the seeded defects in the ground truth the review identifies, at any
  severity, with the right substance (the mechanism, not a vague gesture). 0 for a task with no seeded defects.
- `manufactured_findings`: how many findings are NOT real problems in this artifact: invented
  failures with no path to happen in the text given, issues already handled by the text, generic
  "consider adding X" with no concrete trigger, or style nits presented as problems. Real secondary
  issues listed in the ground truth are NOT manufactured. Count at any severity.
- `manufactured_high`: how many of the manufactured findings were rated Critical or Important (or
  the review's equivalent of blocking / must-fix).
