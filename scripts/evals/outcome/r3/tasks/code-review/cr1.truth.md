Seeded issue (1):

- S1 (blocking) a caller OUTSIDE the diff breaks: `supabase/functions/send-reminders/index.ts` still
  selects `customers(name, phone)`. After the migration renames the column to `phone_number`, PostgREST
  answers that query with an error (column `customers.phone` does not exist), the function ignores
  `error` (`const { data: bookings } = ...`), `bookings ?? []` is empty, and the function returns "ok":
  appointment reminders silently stop for every customer, with nothing failing in CI (`tsc` and
  `vitest` do not cover the edge functions). Fix: select `phone_number` and read
  `b.customers.phone_number` in the same PR (and check `error`), deploying the function together with
  the migration. Identifying it requires reading the context file, not just the diff.

Real secondary issues (not manufactured):
- Deploy/rollout ordering: `RENAME COLUMN` breaks whatever still reads `phone` during the rollout (old
  app instances, the edge function until redeployed); an expand/contract migration (add the new column,
  backfill, switch readers, drop later) or a coordinated deploy avoids it.
- The migration's normalisation is naive: `'+55' || digits` turns a number already stored with the
  country code but without `+` (`5511987654321`) into `+555511987654321`; and the form's transform turns
  an empty field into `"+55"`, which then fails the regex (the optional field can no longer be cleared);
  `.replace(/^55/, "")` also strips area code 55 (Rio Grande do Sul), so `(55) 99999-1234` is rejected.
- The edge function ignores the query `error` (pre-existing, but it is what makes S1 silent).

Not defects: `@map("phone_number")` with the rename migration is the right Prisma pattern; the
admin page selects only `id, name, email` and is unaffected; using the service-role key inside a
Supabase Edge Function (server side) is correct.

Correct verdict: changes requested (S1 must be fixed before merging).
