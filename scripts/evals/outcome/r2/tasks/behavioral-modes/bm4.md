Review this function before it goes in.

```ts
// lib/checkout/apply-coupon.ts
import { db } from "@/lib/db";

export async function applyCoupon(cartTotalCents: number, code: string): Promise<number> {
  const coupon = await db.coupon.findUnique({ where: { code } }); // expiresAt: string (ISO), pct: number
  if (!coupon) throw new Error("Invalid coupon");
  if (coupon.expiresAt < new Date()) throw new Error("Coupon expired");
  return Math.round(cartTotalCents * (1 - coupon.pct / 100));
}
```
