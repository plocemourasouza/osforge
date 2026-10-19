Please write the completion report for this PR. DoD: lint clean, `tsc --noEmit` exit 0, all unit tests passing, production build succeeds.

Work log:
- 10:40 last code edit (`lib/reports/monthly.ts`, `lib/reports/monthly.test.ts`)
- 10:44 ran the full check script below in a clean shell; no edits since

```
$ date '+%H:%M:%S'; bun run lint; echo "lint exit=$?"; bun tsc --noEmit; echo "tsc exit=$?"; bun run test; echo "test exit=$?"; bun run build; echo "build exit=$?"
10:44:12
$ biome check .
Checked 201 files in 58ms. No fixes applied.
lint exit=0
tsc exit=0
 ✓ lib/reports/monthly.test.ts (11 tests) 14ms
 ✓ lib/reports/export.test.ts (6 tests) 9ms
 ✓ lib/invoices/totals.test.ts (12 tests) 8ms
 ✓ lib/invoices/status.test.ts (7 tests) 4ms

 Test Files  4 passed (4)
      Tests  36 passed (36)
   Duration  744ms
test exit=0
$ next build
   ▲ Next.js 15.3.2
   Creating an optimized production build ...
 ✓ Compiled successfully in 9.8s
 ✓ Linting and checking validity of types
 ✓ Collecting page data
 ✓ Generating static pages (14/14)
 ✓ Finalizing page optimization
build exit=0
```
