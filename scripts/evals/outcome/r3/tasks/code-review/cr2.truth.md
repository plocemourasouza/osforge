Seeded issue (1):

- S1 (blocking) read-then-write race on stock, under the load the README declares: `findUnique` reads
  `stock`, the check runs in the app, and `update` writes the absolute value `product.stock - quantity`.
  Two concurrent requests (different serverless instances, the "drop" with ~2,000 buyers on 20-50 units)
  both read `stock = 1`, both pass the check, both write `0`: two reservations for one unit (overselling),
  and in general lost updates (the second write overwrites the first decrement). Wrapping the same code
  in `prisma.$transaction([...])`/interactive transaction at the default READ COMMITTED isolation does not
  fix it by itself. Fix: one atomic conditional update, e.g.
  `const r = await tx.product.updateMany({ where: { id: productId, active: true, stock: { gte: quantity } }, data: { stock: { decrement: quantity } } }); if (r.count === 0) -> "sold out"`,
  or `SELECT ... FOR UPDATE` in an interactive transaction, or SERIALIZABLE with retry; plus a
  `CHECK (stock >= 0)` constraint as a backstop.

Real secondary issues (not manufactured):
- The decrement and the `reservation.create` are separate writes: if the second fails (or the function
  times out between them), stock is lost with no reservation to expire. Both belong in one
  `$transaction`.
- No limit on reservations per user (one user can reserve 10 units repeatedly and hold the drop for
  15 minutes); a product decision, fair as a suggestion.
- `Reservation` has no `user` relation/foreign key and no index on `userId` (minor).

Not defects: Zod validation with `coerce` for FormData is right; `requireUser` covers auth; the 15-minute
expiry job is declared as a separate PR (not a finding against this one).

Correct verdict: changes requested (S1). A review that calls the race a theoretical/low-priority concern
"at scale" misreads the declared load: the drop is exactly the concurrent case.
