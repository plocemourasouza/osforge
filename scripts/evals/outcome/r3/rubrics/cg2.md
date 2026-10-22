## Task-specific criteria (task: short public order code; Node 20, no id package installed)

- `uses_platform_id` (critical): the code is generated from Node's built-in `crypto` (`randomInt`,
  `getRandomValues`, `randomBytes` or `randomUUID`); `Math.random()` or a time/sequence-based code fails.
- `no_new_dependency` (critical): no new npm package (nanoid, uuid, shortid, hashids/sqids, ...) is
  added or recommended as the solution.
- `readable_alphabet`: the alphabet excludes look-alike characters (at least 0/O and 1/I/L) and is uppercase.
- `unique_enforced`: `publicId` is `@unique` in the Prisma schema (database-enforced uniqueness).
- `collision_handled`: a unique-constraint violation on create is retried with a fresh code (or an
  equivalent mechanism); "collisions are negligible" alone fails.
- `existing_rows`: the answer handles the existing orders (nullable + backfill, SQL default, or an
  explicit fallback to the cuid for old orders).
- `proportionate`: no unrequested features or abstractions; the explanation is short relative to the change.
