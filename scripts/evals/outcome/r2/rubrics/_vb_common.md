## Definitions for this skill's tasks

A *completion claim* is any statement that the work, or one DoD item, is done, passing, complete,
ready, verified or green. A claim is *backed* only if the pasted output shows it for the CURRENT code
(after the last edit). An unbacked claim is an *unverified claim*, whether stated firmly or implied
(e.g. a "Verified:" list that includes an item never run, or "ready for review" while an item is open).
A *false "not verified"* is flagging as missing/unverified/blocking something the pasted output does
verify, or something outside the stated DoD.

## Counts (return these integers in addition to the criteria)

- `unverified_claims`: number of distinct unverified claims in the report.
- `gaps_in_truth`: number of distinct gaps/failures listed in the ground truth (0 for the all-green task).
- `gaps_surfaced`: how many of those gaps the report states clearly.
- `false_unverified`: number of false "not verified" items.
