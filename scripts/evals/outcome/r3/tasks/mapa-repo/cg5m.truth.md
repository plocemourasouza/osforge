This is the cg5 family (a caller with a local money workaround) with the shared helper's file left
OUT of the prompt. The repository (not shown to the assistant) has `lib/money.ts`, which the cart and
the checkout already use to compute the CHARGED amount:

```ts
/** Reais (a Product.price converted with Number()) to integer cents. */
export function toCents(reais: number): number { return Math.round(reais * 100); }
/** Total in cents of priced lines. */
export function sumCents(lines: { unitPrice: number; quantity: number }[]): number; // sum of toCents(unitPrice) * quantity
export function fromCents(cents: number): number; // cents / 100
```

Nothing in the prompt names these: the assistant can only know they exist if its context lists them
(arm C's repository map has the line `lib/: getSession, cartTotalCents, prisma, formatCurrency, toCents, ...`:
one name per file, so only `toCents` is visible, not `sumCents`), and then it knows the name and the
folder, not the file or the signature.

Root cause in the receipt: `1.1 * 100 === 110.00000000000001`, so `Math.ceil` gives 111 per hair tie
(3 x 111 = 333). The checkout uses `toCents` (round), so it charged 330.

What a correct answer does:

- Makes the receipt compute cents the way the charge does, by reusing the shared helper:
  `import { toCents } from "@/lib/money"` (per line `toCents(Number(item.product.price)) * item.quantity`)
  or `sumCents(order.items.map(...))`. Because the signatures are not visible, an excellent answer states
  the signature it assumes or says to check it. Using the helper is what guarantees the receipt and the
  charge cannot diverge again.
- Removes the `Math.ceil` workaround; the result for 3 x R$ 1,10 is 330 and for R$ 19,99 is 1999.
- An answer whose context did not reveal the helper and that writes `Math.round(Number(price) * 100)`
  inline fixes this ticket but duplicates the rule the checkout uses (fails `reuses_existing_helper`);
  the criterion grades the outcome, not the excuse. Writing a new `toCents`-like helper in `lib/receipt.ts`
  or a new module also fails `no_new_money_helper`.
- Adds a regression test (3 x 1.10 -> 330, and/or 19.99 -> 1999) to `lib/receipt.test.ts`.

Over-builds (scope creep): a money library (`dinero.js`, `big.js`), a Decimal-everywhere refactor,
changing the checkout, a new money module.

The map names folders, not files: an import from a guessed module inside the right folder
(e.g. `@/lib/utils` instead of `@/lib/format`) still counts as reuse; the exact path is not graded.
