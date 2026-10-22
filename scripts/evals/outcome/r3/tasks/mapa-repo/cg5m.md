Support ticket from the salon's shop (Next.js 15 App Router, TypeScript, Prisma on Supabase Postgres):

"I bought 3 hair ties at R$ 1,10. The cart and my card charge were R$ 3,30, but the receipt email
says R$ 3,33."

The receipt total does not match what we charge. Fix it. Show me the changes.

`prisma/schema.prisma` (excerpt): `model Product { id String @id @default(cuid()) name String price Decimal @db.Decimal(10, 2) ... }`

`lib/types.ts` (excerpt):

```ts
import type { Prisma } from "@prisma/client";

export type OrderWithItems = {
  id: string;
  items: { quantity: number; product: { name: string; price: Prisma.Decimal } }[];
};
```

`lib/receipt.ts`:

```ts
import type { OrderWithItems } from "@/lib/types";

export function buildReceipt(order: OrderWithItems) {
  const lines = order.items.map((item) => {
    // Number(price) * 100 sometimes comes out as 1998.9999..., so round up here
    const lineCents = Math.ceil(Number(item.product.price) * 100) * item.quantity;
    return { name: item.product.name, quantity: item.quantity, lineCents };
  });
  return { lines, totalCents: lines.reduce((t, l) => t + l.lineCents, 0) };
}
```

`lib/receipt.test.ts`:

```ts
import { expect, it } from "vitest";
import { Prisma } from "@prisma/client";
import { buildReceipt } from "./receipt";

it("totals the lines", () => {
  const order = { id: "o1", items: [{ quantity: 2, product: { name: "Comb", price: new Prisma.Decimal("12.50") } }] };
  expect(buildReceipt(order).totalCents).toBe(2500);
});
```
