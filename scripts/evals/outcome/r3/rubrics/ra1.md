## Task-specific criteria (task: audit a Next.js + Supabase mini-repo; service-role key in client code, a table without RLS, a harmless TODO)

- `found_service_role` (critical): identifies that the service-role key is exposed to the browser
  (`NEXT_PUBLIC_` variable used by `lib/supabase/admin.ts`, imported by a client component).
- `found_rls` (critical): identifies that `client_notes` has no row-level security, so its (sensitive)
  data is readable/writable with the public anon key.
- `key_rotation`: says the already-exposed key must be rotated, not only moved to the server.
- `todo_not_high`: the i18n TODO is not rated must-fix/high (ignoring it or listing it as nice-to-have both pass).
- `ranked_right`: the two security issues are the top findings (must fix), above every other finding.
- `actionable`: findings carry file:line (or file and the exact code) and a concrete fix.
- `no_manufactured_high` (critical): zero manufactured findings rated must-fix/critical/high.
