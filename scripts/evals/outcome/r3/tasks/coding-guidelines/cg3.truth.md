What a correct answer does (the repository already has the helper; it beats the platform API):

- Imports `formatCurrency` from `@/lib/format` and calls it with the CENTS values:
  `formatCurrency(product.priceCents)` and `formatCurrency(product.compareAtCents)`. The helper divides
  by 100 itself, so `formatCurrency(product.priceCents / 100)` is a bug (R$ 0,50 for R$ 49,90).
- Removes the hard-coded `R$ ` prefix (the helper's output already contains "R$"); leaving it gives
  "R$ R$ 49,90".
- Formats both the price and the struck-through `compareAtCents`.
- Writes no new formatter: no new `Intl.NumberFormat`, `toLocaleString("pt-BR", ...)`, `toFixed(2)` plus
  string replace, or a new `formatBRL` helper next to the existing one. (`Intl.NumberFormat` is the right
  platform tool in general, but here the house helper exists and is what the rest of the app uses.)
- Keeps the change to `product-card.tsx` (a Server Component; no `"use client"` is needed).

Secondary, real, optional: `{product.compareAtCents && ...}` renders a literal `0` when the value is
`0`; switching to `!= null` (or `> 0`) is a fair, small fix. Not required.

Over-builds (scope creep): a price component with options, currency/locale configuration, i18n
setup, changing the schema to `Decimal`, touching other files.
