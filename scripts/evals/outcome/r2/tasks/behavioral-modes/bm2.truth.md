Mode: DEBUG. Root cause: yesterday's change to `GET /api/orders` returns a different shape when the
user has no orders: an empty array `[]` instead of `{ orders: [] }`. Brand-new accounts have no
orders, so `data` is `[]` (truthy, so the loading guard passes) and `data.orders` is `undefined`;
`.map` on it throws at line 14.
Correct fix: at the source — always return `{ orders }` (i.e. `NextResponse.json({ orders })`).
Optional hardening in the client is fine as a secondary measure, but `data?.orders?.map` alone only
hides the symptom and leaves an inconsistent API contract. Prevention: a response schema / typed
contract test for the empty case. The answer should not ask for more information: the trace and code
are sufficient.
