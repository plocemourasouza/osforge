Mode: BRAINSTORM. Expected shape: several genuinely different options with trade-offs, not an
implementation. Reasonable option space (not all required): scheduled job (daily cron scanning
overdue invoices) vs event/queue-based (scheduled message at due date), channel choices (email,
SMS/WhatsApp, in-app, webhook to the tenant), who owns the message (platform vs tenant-branded,
tenant-configurable reminder cadence/dunning sequence), build vs buy (email provider sequences,
dunning tools). Key questions that change the choice: who is "the customer" (tenant's end customer vs
tenant admin), tenant opt-in/branding, timezone/business-day rules, deliverability and compliance
(opt-out, LGPD), idempotency (no duplicate reminders), and what "overdue" means with partial
payments. A good answer surfaces decision criteria and may give a provisional recommendation; it does
not dump code or a full schema.
