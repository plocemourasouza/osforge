Hidden behaviour a naive cleanup breaks:
- H1 cross-call dedupe: `seen` is module-level, so an email imported from `crm.csv` is skipped when it
  appears again in `shop.csv` and `events.csv`. The nightly job calls `importUsers` three times in one
  process, so it relies on dedupe ACROSS files. Moving `seen` inside the function (the obvious
  "no module state" cleanup) silently changes what the nightly job upserts. A correct answer preserves
  it, or makes it explicit (e.g. a dedupe set passed in / a factory) with the nightly job updated, or
  clearly flags the behaviour and asks. Silently making it per-call fails.
- H2 API: `importUsers(path, cb)` with a synchronous callback is what callers use. Converting to
  `async`/Promise-only without keeping the callback form (or updating `nightly.js`) breaks callers.
  Note also that `nightly.js` relies on the callback running synchronously in loop order.
- H3 parsing: `parseInt(parts[2])` turns "34 " or "34y" into 34 and "" into null; replacing with
  `Number(...)` changes "34y" to NaN. Minor, but a strict answer keeps `parseInt` (ideally with radix 10)
  or `Number.parseInt`.
- H4 header skip (start at line 1), empty-line skip, email trimmed + lowercased before dedupe,
  `vip` true for "1" or "true".
Real cleanups expected: `const`/`let`, separate parse from IO, drop or replace the `console.log`
that writes an email address (PII) to logs, `===`. A note that `\r\n` files would leave `\r` in the
last field is a fair observation, not required.
