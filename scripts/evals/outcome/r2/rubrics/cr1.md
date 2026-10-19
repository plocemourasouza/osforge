## Task-specific criteria (task: review a diff with two seeded bugs)

- `found_B1` (critical): identifies the missing tenant/ownership scoping (any user can refund another
  tenant's invoice).
- `found_B2` (critical): identifies the reais-vs-centavos mismatch in the Stripe `amount`.
- `severity_right`: B1 and B2 (if found) are rated at the top severity (critical / must-fix). `na` if neither found.
- `no_manufactured_high` (critical): zero manufactured findings rated blocking/critical/warning.
- `actionable`: findings carry a location and a concrete fix.
- `atomicity_noted`: mentions the non-atomic Stripe-then-DB sequence, the race between concurrent
  refunds, or the missing idempotency key (secondary, real).
