Plan this feature (the decision to build it is made; I need the execution plan). Feature: "Export CSV" button on the invoices list that downloads the invoices currently shown, with the active filters applied.

What exists (Next.js 15 App Router, Prisma, Postgres, multi-tenant; every table has `tenantId`):
- `app/(app)/invoices/page.tsx` — Server Component; reads `searchParams` (`status`, `dateFrom`, `dateTo`, `q`), calls `listInvoices(session.tenantId, filters)` and renders `<InvoicesTable>` with pagination (50 per page).
- `lib/invoices/queries.ts` — `listInvoices(tenantId: string, filters: InvoiceFilters, page = 1)` builds the Prisma `where` from the filters and paginates.
- `lib/invoices/filters.ts` — `parseInvoiceFilters(searchParams): InvoiceFilters` (Zod).
- `lib/auth.ts` — `getSession()` returns `{ userId, tenantId, role }` or null.
- Largest tenant has ~180k invoices. Tests: Vitest for `lib/`, Playwright for flows.
