Review this pull request for our salon's online shop (Next.js 15 App Router, TypeScript, Prisma on
Supabase Postgres). PR description: "Reserve stock when the customer starts checkout, so we stop
selling products we don't have. Reservations expire after 15 min (cron job, separate PR)."

```diff
diff --git a/app/(shop)/checkout/reserve.ts b/app/(shop)/checkout/reserve.ts
new file mode 100644
@@ -0,0 +1,41 @@
+"use server";
+import { z } from "zod";
+import { prisma } from "@/lib/db";
+import { requireUser } from "@/lib/auth";
+
+const ReserveInput = z.object({
+  productId: z.string().cuid(),
+  quantity: z.coerce.number().int().min(1).max(10),
+});
+
+export type ReserveState = { error?: string; reservationId?: string };
+
+export async function reserveStock(_prev: ReserveState, formData: FormData): Promise<ReserveState> {
+  const user = await requireUser();
+  const parsed = ReserveInput.safeParse(Object.fromEntries(formData));
+  if (!parsed.success) return { error: "Invalid quantity." };
+  const { productId, quantity } = parsed.data;
+
+  const product = await prisma.product.findUnique({ where: { id: productId } });
+  if (!product || !product.active) return { error: "Product not available." };
+  if (product.stock < quantity) return { error: `Only ${product.stock} left.` };
+
+  await prisma.product.update({
+    where: { id: productId },
+    data: { stock: product.stock - quantity },
+  });
+
+  const reservation = await prisma.reservation.create({
+    data: {
+      userId: user.id,
+      productId,
+      quantity,
+      expiresAt: new Date(Date.now() + 15 * 60_000),
+    },
+  });
+
+  return { reservationId: reservation.id };
+}
diff --git a/prisma/schema.prisma b/prisma/schema.prisma
@@ -40,6 +40,16 @@ model Product {
   stock          Int     @default(0)
   active         Boolean @default(true)
+  reservations   Reservation[]
 }
+
+model Reservation {
+  id        String   @id @default(cuid())
+  userId    String
+  productId String
+  quantity  Int
+  expiresAt DateTime
+  product   Product  @relation(fields: [productId], references: [id])
+
+  @@index([expiresAt])
+}
```

`README.md` (excerpt):

> **Deploy.** Vercel (serverless functions, autoscaling; each request may hit a different instance),
> Supabase Postgres through the pooler. **Traffic.** Normal days: a few hundred orders. Every first
> Monday of the month we run a "drop" of limited products (20-50 units each); last drop had ~2,000
> people on the product page at 10:00 and sold out in 4 minutes.

`lib/db.ts` exports a single `PrismaClient`. There are no database triggers or constraints on
`Product.stock` beyond the column type.
