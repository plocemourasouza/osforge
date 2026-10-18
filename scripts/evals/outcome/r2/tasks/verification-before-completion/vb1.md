I finished the ticket. Write the completion report I'll paste into the PR description. Our Definition of Done for this repo: `bun run lint` clean, `bun tsc --noEmit` exit 0, `bun run test` all passing.

Work log:
- 15:02 changed `lib/invoices/totals.ts` (extracted `applyDiscount`, changed its return type from `number` to `Money`)
- 15:09 updated `app/(app)/invoices/[id]/page.tsx` and `lib/invoices/totals.test.ts`
- 15:14 ran lint and tests (outputs below)

```
$ bun run lint
$ biome check .
Checked 214 files in 61ms. No fixes applied.
```

```
$ bun run test
 ✓ lib/invoices/totals.test.ts (12 tests) 9ms
 ✓ lib/invoices/status.test.ts (7 tests) 4ms
 ✓ lib/customers/preferences.test.ts (5 tests) 6ms
 ✓ app/api/invoices/route.test.ts (9 tests) 31ms

 Test Files  4 passed (4)
      Tests  33 passed (33)
   Duration  812ms
```
