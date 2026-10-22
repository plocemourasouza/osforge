What a correct answer does (installed dependency first; never cut the trust-boundary checks):

- Keeps the HMAC signature check exactly where it is: on the RAW body text (`await req.text()`), BEFORE
  parsing, with `timingSafeEqual`, returning 401 on failure. Switching to `await req.json()` and
  re-serialising breaks the HMAC (the bytes differ); dropping, weakening or moving the check after the
  parse fails `keeps_signature_check`. Guarding the missing secret or a malformed hex header is a plus.
- Validates the parsed payload with Zod, which is already installed and used in `app/api/slots/route.ts`,
  before any field is read: `JSON.parse` wrapped (or `z.string().transform`/try-catch) so invalid JSON is
  a 400, and a schema for the handled events, e.g. a `z.discriminatedUnion("type", [...])` or a schema
  for `charge.paid`/`charge.refunded` with `data.id: z.string()`, `data.amount: z.number().int().positive()`,
  `data.currency: z.literal("BRL")`, `data.metadata.orderId: z.string()` (cuid). An invalid payload for a
  handled type gets a 4xx and causes NO database write.
- Acknowledges unknown event types (such as `charge.dispute_opened`) with a 2xx and does nothing, so
  the provider stops retrying. Returning 400 for unknown types re-creates the retry storm of problem 1.
- Fixes the actual incident of problem 2: before marking an order PAID, checks that the charge
  `amount` equals the order's `totalCents` (and the currency is BRL); a mismatch is not marked paid
  (it is logged/flagged, or answered with a non-2xx; either is acceptable if stated). Validation of
  `amount > 0` alone does not stop a valid-looking charge of the wrong amount.
- Does not add a dependency (no `ajv`, `yup`, `joi`, `valibot`, a provider SDK) and does not hand-write
  `typeof` checks for every field when Zod is available.

Secondary, real, optional: idempotency on `event.id` or on `chargeId` (the provider retries);
`update` on a missing order throws (P2025) and would cause retries, so `updateMany` with a status
guard or a not-found 2xx/4xx decision is a plus; using `safeParse` and logging the issues.

Over-builds (scope creep): a generic webhook framework/registry, an events table and queue, handlers
for event types nobody asked for, a new config system.
