Mode: REVIEW. Seeded issues:
- D1 (high): `coupon.expiresAt` is an ISO string and is compared with a `Date` using `<`. In a
  relational comparison the Date becomes a number and the string becomes `NaN` (ISO strings are not
  numeric), so the comparison is always `false`: expired coupons are always accepted. (In TypeScript
  strict this comparison may also be a type error, depending on the declared type.) Fix: compare
  `new Date(coupon.expiresAt).getTime() < Date.now()` (or store a Date).
- D2 (medium): `pct` is not bounded — a coupon with `pct > 100` yields a negative total, `pct < 0`
  raises the price; validate 0 < pct <= 100 (at creation and/or here).
Real minor points (not manufactured): coupon code lookup case-sensitivity; usage limits / per-customer
redemption not checked (may be out of this function's scope); the error messages are fine.
Not defects: `Math.round` on cents is fine.
