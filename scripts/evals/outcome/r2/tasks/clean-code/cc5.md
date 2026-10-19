Our `calcTotal` takes positional booleans and people keep swapping them at call sites. Please refactor it so call sites are readable, and show every file that has to change. `pricing.test.ts` (not shown) also calls `calcTotal` positionally in 6 places.

```ts
// pricing.ts
export interface LineItem {
  unitCents: number;
  qty: number;
}

export function calcTotal(
  items: LineItem[],
  discountPct: number,
  includeTax: boolean,
  roundUp: boolean,
  taxRate = 0.17,
): number {
  let total = 0;
  for (const i of items) total += i.unitCents * i.qty;
  if (discountPct > 0) total = total - (total * discountPct) / 100;
  if (includeTax) total = total + total * taxRate;
  return roundUp ? Math.ceil(total) : Math.round(total);
}
```

```ts
// cart.ts
import { calcTotal, type LineItem } from "./pricing";

export function cartTotal(items: LineItem[], coupon?: { pct: number }): number {
  return calcTotal(items, coupon?.pct ?? 0, true, false);
}
```

```ts
// invoice.ts
import { calcTotal, type LineItem } from "./pricing";

export function invoiceTotal(items: LineItem[], exportOrder: boolean): number {
  // Export orders are tax-exempt by law (ICMS art. 3, II); invoices always round up.
  return calcTotal(items, 0, !exportOrder, true, 0.12);
}
```
