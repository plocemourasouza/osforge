## Task-specific criteria (task: format BRL prices on the product card; `formatCurrency` exists in `lib/format.ts` but its file is not in the prompt)

- `reuses_existing_helper` (critical): the card uses the existing `formatCurrency` imported from
  `@/lib/...` (the exact file name is not graded), passing cents (or passing a value AND stating the unit assumption to verify); inline
  `Intl.NumberFormat`/`toLocaleString` or a new helper fails, even when the answer could not have known
  about `formatCurrency`.
- `all_prices_formatted`: both the price and the struck-through `compareAtCents` are formatted, and the
  hard-coded `R$ ` prefix is removed (no "R$ R$").
- `no_new_formatter`: no new currency-formatting helper or module is created (an inline
  `Intl.NumberFormat` in the card counts as a new formatter here).
- `surgical`: only the price markup in `product-card.tsx` changes.
- `proportionate`: no unrequested features or abstractions; the explanation is short relative to the change.
