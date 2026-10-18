Seeded bugs (2):
- B1 (critical) missing tenant/ownership check: `findUniqueOrThrow({ where: { id: invoiceId } })` and the
  `update` are not scoped by `session.tenantId` (and no role check): any logged-in user of any tenant can
  refund another tenant's invoice by posting its id (IDOR). Fix: `where: { id: invoiceId, tenantId:
  session.tenantId }` (findFirst / compound unique) and authorize the role.
- B2 (critical) unit mismatch: Stripe's `amount` is in the smallest currency unit (centavos), but the
  code sends `amount` in reais (`49.90`) — Stripe rejects non-integers or refunds 100x less (R$0.49 for
  49), while the DB records `amount * 100`. Fix: compute `const amountCents = Math.round(amount * 100)`
  once and use it for the check, Stripe and the DB.
Real secondary issues (not manufactured): Stripe call and DB update are not atomic/idempotent (a DB
failure after the refund leaves `refundedCents` stale; concurrent refunds can both pass the check — race;
an idempotency key would help); `amount * 100` float imprecision in the check (minor); the error
messages surface to the client (minor).
Not defects: Zod is present and `coerce` is appropriate for FormData; `revalidatePath` is correct.
