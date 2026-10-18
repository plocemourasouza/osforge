Deliverables expected: 20 numbered native rewrites. Reference answers (equivalents accepted):
1 `users.map((u) => u.id)` · 2 `users.filter((u) => u.active === true)` · 3 `users.find((u) => u.age > 30)` ·
4 `[...new Set(tags)]` · 5 `matrix.flat()` · 6 `nested.flat(Infinity)` · 7 `values.filter(Boolean)` ·
8 `Array.from({ length: Math.ceil(items.length / 3) }, (_, i) => items.slice(i * 3, i * 3 + 3))` ·
9 `prices.reduce((a, b) => a + b, 0)` · 10 `lines.reduce((a, l) => a + l.amount, 0)` ·
11 `Object.groupBy(orders, (o) => o.status)` (ES2024 — in strict ES2022 use reduce; either accepted with
a note) · 12 `Object.fromEntries(users.map((u) => [u.id, u]))` ·
13 `(({ id, email }) => ({ id, email }))(user)` or `Object.fromEntries(["id","email"].filter(k => k in user).map(k => [k, user[k]]))` ·
14 `(({ password, ...rest }) => rest)(user)` · 15 `Object.keys(obj).length === 0` · 16 `items.at(-1)` ·
17 `Array.from({ length: 5 }, (_, i) => i)` or `[...Array(5).keys()]` · 18 `roles.includes("admin")` ·
19 `name.charAt(0).toUpperCase() + name.slice(1).toLowerCase()` ·
20 `[...users].sort((a, b) => a.age - b.age)` (must not mutate `users`; lodash sortBy is stable and
returns a new array — `users.sort(...)` mutating in place is a behaviour difference; `toSorted` is ES2023).
Behaviour-break examples: 19 without `.toLowerCase()` on the rest; 20 mutating `users`; 2 using
truthiness is acceptable for booleans.
