## Task-specific criteria (task: validate a payment webhook; Zod installed, HMAC check in the code)

- `keeps_signature_check` (critical): the HMAC check is kept on the raw body text, before parsing,
  timing-safe, still answering 401; switching to `req.json()` or weakening/removing/moving it fails.
- `validates_at_boundary` (critical): the payload is validated (schema for the handled events: ids,
  integer positive amount, currency, orderId) before any field is used; invalid JSON or an invalid
  handled event gets a 4xx and causes no database write.
- `uses_installed_zod`: the validation uses Zod (already installed and used in the repo), not
  hand-written `typeof` chains or another library.
- `no_new_dependency`: no new npm package is added or suggested as the solution.
- `amount_checked`: before marking PAID, the charge amount (and currency) is compared with the order's
  `totalCents`; a mismatch is not marked paid.
- `unknown_events_acked`: unknown event types are acknowledged with a 2xx and ignored (no crash, no 4xx/5xx).
- `proportionate`: no unrequested features or abstractions; the explanation is short relative to the change.
