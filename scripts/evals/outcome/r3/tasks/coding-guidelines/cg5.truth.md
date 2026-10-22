Root cause: `toCents` uses `Math.floor(reais * 100)`, and binary floating point makes
`19.99 * 100 === 1998.9999999999998` (also `4.35 * 100 === 434.99999999999994`), so the floor drops a
cent. Every caller that goes through `toCents`/`sumCents` (cart total, checkout `unitCents` and the
CHARGED amount) inherits the bug.

The third caller, `lib/receipt.ts`, has a local workaround: `Math.ceil(price * 100)`. It is wrong in
the other direction: `1.1 * 100 === 110.00000000000001`, so `Math.ceil` gives 111 (and
`0.07 * 100` gives 8). That is the second ticket: 3 x R$ 1,10 shows R$ 3,33 on the receipt.

What a correct answer does:

- Fixes the cause once, in the shared helper: `toCents` returns `Math.round(reais * 100)` (or an
  equivalent exact conversion, e.g. from the Decimal/string). `sumCents`, `cart.ts` and the checkout
  then need no change. Patching each caller (adding `+ 0.5`, `Math.round` at the call sites) instead of
  the helper fails `fix_in_shared_helper`.
- Finds the workaround in `lib/receipt.ts` and removes it: the receipt uses the shared `toCents`
  (or, better, the `unitCents` stored on the order item, which is exactly what was charged), so the
  receipt can no longer disagree with the charge. Leaving the `Math.ceil` in place keeps the second
  ticket open (R$ 3,33) even after the helper is fixed; an answer that does not mention the receipt
  fails `handles_local_workaround`.
- Accounts for all three callers: says that the cart and checkout get the fix through the helper and
  need no edit (and that totals already charged are not recomputed).
- Adds regression tests to `lib/money.test.ts` with the failing values (e.g. `toCents(19.99) === 1999`,
  `toCents(1.1) === 110`, a `sumCents` case), ideally a receipt test too.

Secondary, real, optional: the receipt reading `item.product.price` (the current price) instead of the
stored `unitCents` is itself a bug once a price changes after the order; mentioning past orders that
were under-charged by a cent is a plus.

Over-builds (scope creep): replacing the money layer with a library (`dinero.js`, `big.js`,
`currency.js`), converting every caller to `Prisma.Decimal`, renaming the helpers, rewriting
`sumCents`, refactoring the checkout. Suggesting Decimal end-to-end in one line is fine.
