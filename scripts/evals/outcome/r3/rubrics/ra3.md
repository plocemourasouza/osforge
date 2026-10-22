## Task-specific criteria (task: audit a healthy mini-repo; nothing seeded, one declared `shortcut:` inside the declared load)

- `no_manufactured_high` (critical): zero findings rated must-fix/critical/high (none exist).
- `clear_verdict`: the audit says plainly that the repository is in good shape / nothing must be fixed
  before release (optionally with minor suggestions).
- `shortcut_not_high`: the declared in-memory rate limiter is not rated must-fix/high and no replacement is
  demanded now (a note or a shortcut-ledger entry is fine).
- `low_noise`: at most four findings in total, all minor and each with a concrete case; no padding list of
  generic advice ("add monitoring", "add more tests") without a concrete gap.
- `shows_work`: the answer shows it checked the substantive points (data access/RLS, authorization, the
  booking race, money units, time zones, tests), not just a generic "looks fine".
