Our salon's online shop (Next.js 15 App Router, TypeScript, Prisma on Supabase Postgres, deployed on
Vercel with the Node.js 20 runtime) identifies orders by their Prisma `cuid()`, e.g.
`cm7x2k9qz0003l808abcd1234`. Support asks for a short public order code that customers can read
over the phone: 8 characters, uppercase, no characters that are easy to confuse when read aloud,
unique, shown on the confirmation page and in the receipt email instead of the cuid. Keep the
cuid as the primary key. Show me the changes.

`package.json` (dependencies):

```json
{
  "dependencies": {
    "@prisma/client": "6.4.1",
    "@react-email/components": "0.0.33",
    "next": "15.2.4",
    "react": "19.0.0",
    "react-dom": "19.0.0",
    "resend": "4.1.2",
    "zod": "3.24.2"
  },
  "devDependencies": { "prisma": "6.4.1", "typescript": "5.7.3", "vitest": "3.0.5" }
}
```

`prisma/schema.prisma` (excerpt; the table already has ~18,000 orders):

```prisma
model Order {
  id          String      @id @default(cuid())
  userId      String
  status      OrderStatus @default(PENDING)
  totalCents  Int
  createdAt   DateTime    @default(now())
  items       OrderItem[]
  user        User        @relation(fields: [userId], references: [id])

  @@index([userId, createdAt])
}
```

`lib/orders.ts`:

```ts
import { prisma } from "@/lib/db";
import type { CartLine } from "@/lib/cart";

export async function createOrder(userId: string, lines: CartLine[], totalCents: number) {
  return prisma.order.create({
    data: {
      userId,
      totalCents,
      items: {
        create: lines.map((l) => ({
          productId: l.productId,
          quantity: l.quantity,
          unitCents: l.unitCents,
        })),
      },
    },
  });
}
```

`app/(shop)/orders/[id]/confirmation/page.tsx`:

```tsx
import { notFound } from "next/navigation";
import { prisma } from "@/lib/db";
import { requireUser } from "@/lib/auth";

export default async function ConfirmationPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const user = await requireUser();
  const order = await prisma.order.findFirst({ where: { id, userId: user.id } });
  if (!order) notFound();

  return (
    <main className="mx-auto max-w-lg p-6">
      <h1 className="text-xl font-semibold">Thank you!</h1>
      <p>Your order number is <strong>{order.id}</strong>.</p>
    </main>
  );
}
```

`emails/order-receipt.tsx` (excerpt):

```tsx
export function OrderReceipt({ order }: { order: { id: string; totalCents: number } }) {
  return (
    <Html>
      <Text>Order {order.id}</Text>
      {/* ... */}
    </Html>
  );
}
```
