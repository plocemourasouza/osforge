We're removing lodash. Rewrite each of these 20 calls to native ES2022 (no helper library), keeping the same behaviour for the inputs shown. Give me all 20, numbered, one line of code each (plus a short note only where behaviour differs at an edge case).

1. `_.map(users, "id")`
2. `_.filter(users, { active: true })`
3. `_.find(users, (u) => u.age > 30)`
4. `_.uniq(tags)`
5. `_.flatten(matrix)`
6. `_.flattenDeep(nested)`
7. `_.compact(values)`
8. `_.chunk(items, 3)`
9. `_.sum(prices)`
10. `_.sumBy(lines, "amount")`
11. `_.groupBy(orders, "status")`
12. `_.keyBy(users, "id")`
13. `_.pick(user, ["id", "email"])`
14. `_.omit(user, ["password"])`
15. `_.isEmpty(obj)` (obj is always a plain object)
16. `_.last(items)`
17. `_.range(5)`
18. `_.includes(roles, "admin")`
19. `_.capitalize(name)` ("hELLO" -> "Hello")
20. `_.sortBy(users, "age")`
