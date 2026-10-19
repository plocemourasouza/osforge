Review this diff (Next.js 15 Server Action, Prisma, Stripe; multi-tenant — every table has `tenantId`).

```diff
diff --git a/app/(app)/invoices/[id]/actions.ts b/app/(app)/invoices/[id]/actions.ts
@@ -1,6 +1,36 @@
 "use server";
 import { revalidatePath } from "next/cache";
+import { z } from "zod";
 import { prisma } from "@/lib/db";
 import { stripe } from "@/lib/stripe";
 import { getSession } from "@/lib/auth";
+
+const RefundInput = z.object({
+  invoiceId: z.string().cuid(),
+  amount: z.coerce.number().positive(), // amount in reais, from the refund form (e.g. "49.90")
+});
+
+export async function refundInvoice(formData: FormData) {
+  const session = await getSession();
+  if (!session) throw new Error("unauthorized");
+  const { invoiceId, amount } = RefundInput.parse(Object.fromEntries(formData));
+
+  const invoice = await prisma.invoice.findUniqueOrThrow({ where: { id: invoiceId } });
+  if (amount * 100 > invoice.paidCents - invoice.refundedCents) {
+    throw new Error("Refund exceeds the paid amount");
+  }
+
+  await stripe.refunds.create({
+    payment_intent: invoice.paymentIntentId,
+    amount: amount,
+  });
+
+  await prisma.invoice.update({
+    where: { id: invoiceId },
+    data: { refundedCents: { increment: Math.round(amount * 100) } },
+  });
+
+  revalidatePath(`/invoices/${invoiceId}`);
+}
```
