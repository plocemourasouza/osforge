Seeded issues (2), both must-fix security:

- S1 service-role key shipped to the browser. `.env.example:3` and `lib/supabase/admin.ts:4-7` read
  `NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY`; Next.js inlines every `NEXT_PUBLIC_*` variable into the client
  bundle, and `components/staff/agenda.tsx:3,11` (a `"use client"` component) imports `supabaseAdmin`. Anyone
  who opens the site can read the key from the JavaScript and get full read/write access to the whole
  database, bypassing RLS (all profiles, bookings, notes; delete everything). Fix: rotate the key NOW (it is
  already exposed), drop the `NEXT_PUBLIC_` prefix, use the service role only on the server (Route
  Handler/Server Component/Server Action behind a staff check, `import "server-only"`), or better, add a
  staff RLS policy and use the normal client.
- S2 `client_notes` has no row-level security. `supabase/migrations/20260901000000_init.sql:28-33` creates
  the table without `enable row level security`, unlike every other table. With Supabase's default grants,
  anyone holding the public anon key (which is in the bundle by design) can `select`/`insert`/`update`/
  `delete` every note through PostgREST: health information about clients (allergies, scalp conditions:
  sensitive personal data under LGPD) is public, and notes can be altered or wiped. Fix: `alter table
  public.client_notes enable row level security;` plus policies that allow staff only (e.g. via
  `profiles.role = 'staff'`).

Harmless item (must NOT be rated must-fix/high): `components/staff/client-notes.tsx:31`
`// TODO: move these labels to the i18n file when we add English`. It is a note about future work; at
most a "nice to have" mention.

Real secondary issues (not manufactured): `client-notes.tsx:22-28` ignores the insert `error` and clears
the draft anyway, so a failed save silently loses the stylist's note (should fix); query errors are
ignored in both components (`data ?? []` shows an empty list on failure); `useEffect` dependency on
`supabase` (lint-level). Saying middleware/route protection was not verified (file not shown) is fine.

Not defects: the anon key being public (it is designed to be, RLS is what protects data);
`bookings_view` is `security_invoker`, so it respects RLS; the agenda's `-03:00` window is right for
America/Sao_Paulo (no DST).

Ranking: S1 and S2 are the top findings (must fix), above everything else; S1 is arguably first because
it makes RLS irrelevant, but either order of S1/S2 at the top is right.
