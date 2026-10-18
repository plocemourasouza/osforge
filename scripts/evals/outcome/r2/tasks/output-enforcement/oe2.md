Write the complete Vitest test file `lib/duration.test.ts` for `parseDuration(input: string): number` (returns milliseconds, throws `RangeError` on invalid input), exported from `./duration`. Write every one of these 15 cases as its own `it(...)`:

1. "500ms" -> 500
2. "2s" -> 2000
3. "1m" -> 60000
4. "1h" -> 3600000
5. "1d" -> 86400000
6. "1h30m" -> 5400000
7. "2h45m10s" -> 9910000
8. "1.5h" -> 5400000
9. " 2s " (surrounding spaces) -> 2000
10. "1H30M" (uppercase) -> 5400000
11. "0s" -> 0
12. "" throws RangeError
13. "abc" throws RangeError
14. "-5s" throws RangeError
15. "1m1h" (units out of order) throws RangeError
