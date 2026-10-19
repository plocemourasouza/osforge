The fix is an options object (or equivalent named parameters) for `calcTotal`, with both callers
rewritten so that every input produces the same number as before.

Behaviour that must survive (the ripple):
- `cart.ts`: tax applied (default rate 0.17), normal rounding (`Math.round`), discount = coupon pct or 0.
- `invoice.ts`: tax applied only when NOT an export order (`includeTax: !exportOrder`), tax rate 0.12
  (not the 0.17 default), round up (`Math.ceil`), no discount. Losing the 0.12, dropping the negation,
  or flipping roundUp is a behaviour break.
- The order of operations (discount, then tax, then rounding) is unchanged.
- The "why" comment in `invoice.ts` (legal reason for the exemption) is worth keeping; it explains
  something the code cannot.
- `pricing.test.ts` calls the old positional signature in 6 places: those calls break. A correct
  answer says so and tells the user to update them (or shows the pattern), or keeps a compatible
  overload/adapter on purpose.

Over-builds that are not needed: a class, a strategy/factory per region, a builder, a separate
`TaxPolicy` abstraction, new config options. A small `type`/`interface` for the options object is fine.
