Two support tickets from the salon's shop (Next.js 15 App Router, TypeScript, Prisma on Supabase
Postgres):

- "I bought 1 Shampoo Reparador (R$ 19,99). The cart said R$ 19,98 and my card was charged R$ 19,98,
  but the receipt email says R$ 19,99."
- "I bought 3 hair ties at R$ 1,10. The cart and the charge were R$ 3,30, the receipt says R$ 3,33."

The cart total rounds wrong. Fix it. Show me the changes.

`prisma/schema.prisma` (excerpt): `model Product { id String @id @default(cuid()) name String price Decimal @db.Decimal(10, 2) ... }`

`lib/money.ts`:

```ts
/** Reais (a Product.price converted with Number()) to integer cents. */
export function toCents(reais: number): number {
  return Math.floor(reais * 100);
}

/** Total in cents of priced lines. */
export function sumCents(lines: { unitPrice: number; quantity: number }[]): number {
  return lines.reduce((total, l) => total + toCents(l.unitPrice) * l.quantity, 0);
}
```

`lib/money.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { sumCents, toCents } from "./money";

describe("money", () => {
  it("converts whole reais", () => expect(toCents(10)).toBe(1000));
  it("sums lines", () => expect(sumCents([{ unitPrice: 2.5, quantity: 2 }])).toBe(500));
});
```

`lib/cart.ts` (caller 1):

```ts
import { sumCents } from "@/lib/money";
import type { CartLineWithProduct } from "@/lib/types";

export function cartTotalCents(lines: CartLineWithProduct[]): number {
  return sumCents(lines.map((l) => ({ unitPrice: Number(l.product.price), quantity: l.quantity })));
}
```

`app/(shop)/checkout/actions.ts` (caller 2, excerpt):

```ts
"use server";
import { toCents } from "@/lib/money";
// ...
  const lines = cart.lines.map((l) => ({
    productId: l.productId,
    quantity: l.quantity,
    unitCents: toCents(Number(l.product.price)),
  }));
  const totalCents = lines.reduce((t, l) => t + l.unitCents * l.quantity, 0);
  const order = await createOrder(user.id, lines, totalCents);
  const charge = await payflow.charges.create({ amount: totalCents, currency: "BRL", orderId: order.id });
```

`lib/receipt.ts` (caller 3):

```ts
import type { OrderWithItems } from "@/lib/types";

export function buildReceipt(order: OrderWithItems) {
  const lines = order.items.map((item) => {
    // toCents drops a cent on some prices (R$ 19,99 -> 1998), so round up here
    const lineCents = Math.ceil(Number(item.product.price) * 100) * item.quantity;
    return { name: item.product.name, quantity: item.quantity, lineCents };
  });
  return { lines, totalCents: lines.reduce((t, l) => t + l.lineCents, 0) };
}
```
