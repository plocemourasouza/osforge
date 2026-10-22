Seeded issues (3), ranked:

- S1 (must fix) wallet balance decremented outside a transaction, read-then-write.
  `app/(wallet)/pay/actions.ts:19-30`: reads `wallet.balance`, checks it in the app (line 21), then writes
  the ABSOLUTE value `wallet.balance - price` (line 25), and records the movement and marks the booking paid
  in separate statements. Under the README's load (concurrent instances; clients paying from the tablet and
  the phone at once) two concurrent payments both pass the check: double spend / negative balance, or two
  different bookings paid with money that covers one. Worse, a Pix top-up landing between the read and the
  write (`webhooks/pix/route.ts` increments atomically) is overwritten by the absolute write: the client
  loses the top-up. Also the same booking can be paid twice (both requests see `paid: false`). Fix: one
  `$transaction` with an atomic conditional decrement, e.g. `updateMany({ where: { id, balance: { gte: price } },
  data: { balance: { decrement: price } } })` + check `count`, and `booking.updateMany({ where: { id, paid: false } })`
  checked the same way, plus the movement insert in the same transaction.
- S2 (must fix, or should fix ranked right below S1) money stored and computed as `Float`.
  `prisma/schema.prisma:4,12,33` (`balance`, `amount`, `price` are `Float`) and the top-up converts cents to a
  float (`route.ts:21`). Binary floating point drifts: after top-ups of 0.10 and 0.20 the balance is
  0.30000000000000004; sums of many movements stop matching the balance, and `balance < price` (line 21)
  can refuse a client who has exactly enough (29.999999999999996 < 30). Fix: integer cents (`Int`, like
  `amountCents` in the webhook) or `Decimal`, with a migration.
- S3 (should fix) unbounded query. `app/(admin)/movements/page.tsx:7-10`: `findMany` with no `take`/pagination
  over a table that grows ~30,000 rows a month, each with its wallet joined: the admin page gets slower every
  month and eventually times out or exhausts memory. Fix: paginate (`take` + cursor) and filter by date.

Ranking that is right: S1 first; S2 above S3 (S2 may be in the same group as S1); S3 below both.
Putting S3 at the top, or the float issue below the unbounded query, is wrong.

Real secondary issues (not manufactured): tests cover only the happy path and low balance, no concurrency
or float case (`tests/pay.test.ts`); `PayInput.parse` throws instead of returning an error; `JSON.parse` of an
invalid webhook body throws (500 and provider retries); `kind` as a free `String` instead of an enum.

Not defects: the Pix webhook verifies the signature on the raw body, validates with Zod, is idempotent on
`txid` (unique + P2002 handled) and increments atomically; `findFirst` scoped by `userId` prevents paying
someone else's booking; `requireAdmin` protects the admin page.
