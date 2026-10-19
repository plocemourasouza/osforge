## Task-specific criteria (task: password-reset spec with 3 seeded defects)

Ground truth (seeded, 3):
- D1 account enumeration: step 2 shows "No account found for this email".
- D2 token not single-use: step 5 checks only age; `used_at` is never set or checked; link replayable.
- D3 existing sessions not revoked after the reset.
Real secondary issues (not manufactured if raised): no rate limiting of reset requests; other
outstanding tokens not invalidated; no AC for the invalid/unknown-token case; password mismatch case
not covered by an AC.

- `found_D1`: identifies D1.
- `found_D2`: identifies D2.
- `found_D3`: identifies D3.
- `severity_right`: D1 and D2 (if found) are rated at blocking/high severity (Critical or Important).
  `na` if neither was found.
- `no_manufactured_high` (critical): zero manufactured findings rated Critical/Important.
- `actionable`: each finding has a location (step/AC) and a concrete fix.
- `prioritized`: findings are separated by severity.
