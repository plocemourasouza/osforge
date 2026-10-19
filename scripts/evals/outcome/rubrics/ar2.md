## Task-specific criteria (task: a deliberately clean, small spec — no seeded defects)

Ground truth: there are NO material defects. The column is NOT NULL and set transactionally, the
API already returns it, helpers already exist, authorization is unchanged, refetch-after-save
already exists. Optional low-severity suggestions (e.g. relative time going stale while the page is
open, tooltip on touch devices) are acceptable as Improvements but are not required.

- `no_blocking_findings` (critical): the review raises zero Critical/Important (blocking/must-fix)
  findings. Any blocking finding fails unless it names a concrete, reachable failure in this text.
- `clear_verdict`: the review states plainly that the spec is sound / ready (or "nothing material
  found"), rather than burying that under a list.
- `shows_work`: it indicates what was checked (areas worked, or the specific assumptions verified),
  so a reader can tell a review happened.
- `low_noise`: at most 3 findings in total, all low severity.
