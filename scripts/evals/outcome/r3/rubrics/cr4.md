## Task-specific criteria (task: review a clean change; nothing seeded)

- `approves` (critical): the verdict approves the change (APPROVED / LGTM / ready to merge), with at most
  optional suggestions.
- `no_manufactured_high` (critical): zero findings rated blocking/critical/high/must-fix (none exist).
- `low_noise`: at most three suggestions, all minor and clearly optional; no padding list of generic advice.
- `shows_work`: the answer shows it checked the substantive points (ownership/authorization, the
  atomic conditional update, the 24 h window, validation, the tests), not just a generic "looks good".
