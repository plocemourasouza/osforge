## Task-specific criteria (task: audit a Prisma + money mini-repo; balance race, float money, unbounded query)

- `found_race` (critical): identifies the read-then-write on the wallet balance outside a transaction
  (double spend / lost top-up / double payment under concurrent requests).
- `found_float_money` (critical): identifies money stored/computed as `Float` and why it is wrong.
- `found_unbounded_query`: identifies the admin `findMany` without a limit/pagination on a growing table.
- `ranked_right` (critical): the race is ranked first (top group), the float issue above the unbounded query,
  and the unbounded query below both.
- `actionable`: findings carry file:line (or file and the exact code) and a concrete fix (atomic conditional
  decrement in a transaction; integer cents or Decimal; pagination).
- `no_manufactured_high`: zero manufactured findings rated must-fix/critical/high.
