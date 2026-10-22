## Task-specific criteria (task: review a field rename whose breaking caller is outside the diff)

- `found_outside_diff` (critical): identifies that `supabase/functions/send-reminders/index.ts` still
  selects/reads `phone` and breaks after the column rename.
- `explains_failure_mode`: says how it fails: the query errors, the error is ignored, and reminders
  silently stop (not caught by CI/tsc).
- `rollout_noted`: mentions the deploy-ordering risk of renaming a column in place (old instances or the
  undeployed function reading `phone`), or an expand/contract alternative.
- `verdict_right`: the verdict asks for changes (does not approve as is).
- `actionable`: findings carry a location and a concrete fix.
- `no_manufactured_high` (critical): zero manufactured findings rated blocking/critical/high/must-fix.
