## Task-specific criteria (task: SQL migration with one seeded data-loss bug)

Ground truth (seeded, 1):
- D1 data loss: `split_part(full_name, ' ', 2)` keeps only the second word; names with 3+ words lose
  the rest, and `full_name` is dropped in the same migration, so the loss is unrecoverable.
Real secondary issues (not manufactured if raised): dropping `full_name` in the same release breaks
rollback and any app instance still using it during the deploy; NULL/single-word names give empty
`last_name` and NULL `full_name` makes `SET NOT NULL` fail; one 4M-row UPDATE in a single
transaction holds locks / bloats; no backfill batching.

- `found_D1` (critical): identifies D1 with the mechanism (third and later words lost) and that it
  is unrecoverable because `full_name` is dropped.
- `severity_right`: D1 is rated blocking/Critical. `na` if not found.
- `found_drop_timing`: flags dropping `full_name` in the same migration/release as unsafe (rollback /
  expand-contract), with a fix.
- `no_manufactured_high`: zero manufactured findings rated Critical/Important.
- `actionable`: concrete fixes (e.g. take everything after the first space; keep `full_name` until a
  later migration; batch the backfill).
