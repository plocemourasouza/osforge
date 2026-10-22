## Task-specific criteria (task: review a stock reservation; read-then-write without a transaction; README declares many concurrent instances)

- `found_race_under_load` (critical): identifies the read-check-write race / lost update on `stock`
  (overselling) AND ties it to the concurrency the README declares (serverless instances, the drop).
- `fix_atomic`: proposes a fix that is actually atomic (conditional `updateMany` with `stock >= quantity`
  and `decrement`, `SELECT ... FOR UPDATE`, or serializable + retry); "wrap it in `$transaction`" alone fails.
- `reservation_atomic`: notes that the stock decrement and the reservation insert should be in one transaction.
- `severity_right`: the race is rated at the top severity (blocking / must fix), not a suggestion.
- `actionable`: findings carry a location and a concrete fix.
- `no_manufactured_high`: zero manufactured findings rated blocking/critical/high/must-fix.
