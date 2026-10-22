## Task-specific criteria (task: format BRL prices on the product card; `lib/format.ts` already has `formatCurrency(cents)`)

- `reuses_existing_helper` (critical): the card calls the existing `formatCurrency` from `@/lib/format`
  with the value it expects (cents, i.e. `product.priceCents`); a new formatter, or passing reais
  (`priceCents / 100`) into it, fails.
- `all_prices_formatted`: both the price and the struck-through `compareAtCents` are formatted, and the
  hard-coded `R$ ` prefix is removed (no "R$ R$").
- `no_new_formatter`: no new `Intl.NumberFormat`, `toLocaleString`, `toFixed`-based or other currency
  formatting code is introduced anywhere.
- `surgical`: only the price markup in `product-card.tsx` changes (an optional `!= null` guard is fine).
- `proportionate`: no unrequested features or abstractions; the explanation is short relative to the change.
