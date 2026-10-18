A good plan for this small feature (roughly 5–9 tasks):
- Reuse the same filter parsing (`parseInvoiceFilters`) and the same `where` construction as the list
  (extract the `where` builder from `listInvoices` or add an unpaginated/streaming variant), so the CSV
  matches what is shown — a separate re-implementation of the filters is a drift risk.
- Auth + tenant scoping on the export route (`getSession()`, 401/403; `tenantId` from the session,
  never from the request).
- "Currently shown" is ambiguous: current page (50) vs all rows matching the filters. A good plan asks
  or states the assumption (all matching rows is the usual intent).
- Volume: up to ~180k rows -> stream the response (Route Handler with a ReadableStream / cursor-based
  batches) or cap/queue; do not load everything in memory.
- CSV correctness: escaping (quotes, commas, newlines), CSV/formula injection (`=`, `+`, `-`, `@`
  prefixes), encoding/BOM for Excel, money/date formatting, filename.
- Button in the UI passing the current `searchParams` to the export URL.
- Tests: Vitest for the CSV serializer + where-builder reuse; Playwright for the download.
- Exact file paths per task, a definition of done, and no code bodies (planner output is a plan).
Over-planning signs: 20+ tasks, new services/queues for a first version without justification,
architecture redesign.
