Plan the migration from moment.js to date-fns and removal of moment from the repo. The decision is made; I need the execution plan.

What exists:

```ts
// lib/format.ts
import moment from "moment";
export function formatDate(d: Date | string, fmt = "DD/MM/YYYY"): string {
  return moment(d).format(fmt);
}
export function fromNow(d: Date | string): string {
  return moment(d).fromNow();
}
```

```
$ grep -rn "formatDate(\|fromNow(\|from \"moment" --include=*.ts --include=*.tsx . | grep -v node_modules
app/(app)/invoices/invoices-table.tsx:31:   {formatDate(inv.dueDate)}
app/(app)/invoices/[id]/page.tsx:44:        {formatDate(invoice.issuedAt, "DD MMM YYYY")}
app/(app)/dashboard/activity.tsx:18:         {fromNow(event.createdAt)}
packages/emails/src/overdue.tsx:22:          Due on {formatDate(invoice.dueDate, "dddd, D [de] MMMM")}
packages/emails/src/receipt.tsx:15:          {formatDate(payment.paidAt, "YYYY-MM-DD HH:mm")}
scripts/reports/monthly.ts:3:import moment from "moment-timezone";
lib/format.ts:1:import moment from "moment";
```

package.json dependencies: `moment`, `moment-timezone`, `date-fns`, `next`, `react`. The emails package renders pt-BR emails; moment's global locale is set to `pt-br` in `packages/emails/src/setup.ts`.
