## Task-specific criteria (task: PR diff with one seeded auth bypass)

Ground truth (seeded, 1):
- D1 IDOR / authorization bypass: the delete filters only by `id` and never checks ownership against
  `session.userId`; any logged-in user can delete any user's payment method.
Real secondary issues (not manufactured if raised): Prisma `delete` throws on a missing record ->
500 instead of 404; CSRF on a cookie-authenticated DELETE Route Handler; no audit log.

- `found_D1` (critical): identifies the missing ownership check (IDOR) with the mechanism.
- `severity_right`: D1 rated Critical/blocking. `na` if not found.
- `fix_right`: the proposed fix scopes the delete by `userId` (e.g. `deleteMany({where:{id,userId}})`
  or find-then-check) and returns 404/403 when nothing matches.
- `no_manufactured_high`: zero manufactured findings rated Critical/Important.
- `prioritized`: findings separated by severity, D1 first or clearly on top.
