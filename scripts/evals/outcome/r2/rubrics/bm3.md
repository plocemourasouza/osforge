## Task-specific criteria (task: brainstorm request)

- `fit_to_mode` (critical): offers at least 3 genuinely different options (architecture, channel or
  ownership choices — not three variations of one design) with trade-offs, and does not deliver an
  implementation (no full code, no full schema/migration).
- `decision_questions`: surfaces the questions that decide between options (at least two of: who the
  recipient is, tenant branding/opt-in/configuration, timezone/business days, compliance/opt-out,
  idempotency, partial payments).
- `scale_aware`: uses the given scale (2,000 tenants, up to 5,000 customers each) in at least one
  trade-off.
- `next_step`: ends with a provisional recommendation or a concrete way to decide.
- `no_padding`: no padding passages.
