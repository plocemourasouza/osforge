This is task cg3 with the helper's file left OUT of the prompt. The repository (not shown to the
assistant) has `lib/format.ts` exporting:

```ts
/** Formats an amount in cents as Brazilian reais, e.g. 4990 -> "R$ 49,90". */
export function formatCurrency(cents: number): string; // Intl.NumberFormat("pt-BR", BRL) of cents / 100
export function formatDateTime(value: Date | string): string;
export function formatPhone(value: string): string;
```

and the cart and checkout already use `formatCurrency`. Nothing in the prompt names it: the assistant
can only know it exists if its context lists it (arm C's repository map has the line
`lib/: getSession, cartTotalCents, prisma, formatCurrency, toCents, ...`: one name per file, because `lib/`
has more than 8 files), and then it knows the name and the folder, not the file or the signature.

What a correct answer does:

- Imports `formatCurrency` from `@/lib/format` and uses it for the price and the struck-through
  `compareAtCents`, removing the hard-coded `R$ ` prefix. Because the signature is not visible, an
  excellent answer passes cents (consistent with the `...Cents` naming in the schema) AND says it is
  assuming the helper takes cents / that the unit should be checked. Passing `priceCents / 100` without
  any caveat is a unit bug against the real helper.
- An answer whose context did not reveal the helper and that formats with `Intl.NumberFormat("pt-BR",
  { style: "currency", currency: "BRL" })` produces correct output but does NOT reuse the existing helper
  (it fails `reuses_existing_helper`); the criterion grades the outcome, not the excuse.
- Writes no new currency-formatting helper or module.
- Keeps the change inside `product-card.tsx`.

Over-builds (scope creep): a price component with options, locale/currency configuration, i18n setup,
schema changes.

The map names folders, not files: an import from a guessed module inside the right folder
(e.g. `@/lib/utils` instead of `@/lib/format`) still counts as reuse; the exact path is not graded.
