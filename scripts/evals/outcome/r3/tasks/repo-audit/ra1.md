Audit this repository before we hand it to a new developer: what is wrong with it, and what breaks first? Below are all of its files except `package.json`, `middleware.ts`, Tailwind/TS config and the `components/ui` primitives. Line numbers are shown on the left.

`README.md`:

```
 1  # Atelier Agenda
 2
 3  Booking app for one hair salon in Passo Fundo (RS). Clients sign up with Supabase Auth and book
 4  appointments; the 3 stylists see the day's agenda and keep private notes about each client
 5  (allergies, scalp conditions, products that caused reactions).
 6
 7  Stack: Next.js 15 (App Router), TypeScript, Supabase (Postgres, Auth, supabase-js), Tailwind.
 8  Deployed on Vercel. About 200 active clients, ~40 bookings a day.
 9
10  `/staff/*` pages are protected by `middleware.ts` (not shown), which redirects anyone whose
11  `profiles.role` is not `staff`.
```

`.env.example`:

```dotenv
1  NEXT_PUBLIC_SUPABASE_URL=https://xyzcompany.supabase.co
2  NEXT_PUBLIC_SUPABASE_ANON_KEY=
3  NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY=
```

`lib/supabase/client.ts`:

```ts
1  import { createBrowserClient } from "@supabase/ssr";
2
3  export function createClient() {
4    return createBrowserClient(
5      process.env.NEXT_PUBLIC_SUPABASE_URL!,
6      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
7    );
8  }
```

`lib/supabase/admin.ts`:

```ts
1  import { createClient } from "@supabase/supabase-js";
2
3  // Staff need to see every client's bookings, but RLS only lets a user see their own.
4  export const supabaseAdmin = createClient(
5    process.env.NEXT_PUBLIC_SUPABASE_URL!,
6    process.env.NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY!,
7  );
```

`components/staff/agenda.tsx`:

```tsx
 1  "use client";
 2  import { useEffect, useState } from "react";
 3  import { supabaseAdmin } from "@/lib/supabase/admin";
 4
 5  type Row = { id: string; starts_at: string; client_name: string; service_name: string };
 6
 7  export function Agenda({ day }: { day: string }) {
 8    const [rows, setRows] = useState<Row[]>([]);
 9
10    useEffect(() => {
11      supabaseAdmin
12        .from("bookings_view")
13        .select("id, starts_at, client_name, service_name")
14        .gte("starts_at", `${day}T00:00:00-03:00`)
15        .lt("starts_at", `${day}T23:59:59-03:00`)
16        .order("starts_at")
17        .then(({ data }) => setRows(data ?? []));
18    }, [day]);
19
20    return (
21      <ul className="divide-y">
22        {rows.map((r) => (
23          <li key={r.id} className="py-2 text-sm">
24            {new Date(r.starts_at).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })}{" "}
25            {r.client_name} ({r.service_name})
26          </li>
27        ))}
28      </ul>
29    );
30  }
```

`components/staff/client-notes.tsx`:

```tsx
 1  "use client";
 2  import { useEffect, useState } from "react";
 3  import { createClient } from "@/lib/supabase/client";
 4
 5  type Note = { id: string; body: string; created_at: string };
 6
 7  export function ClientNotes({ clientId }: { clientId: string }) {
 8    const supabase = createClient();
 9    const [notes, setNotes] = useState<Note[]>([]);
10    const [draft, setDraft] = useState("");
11
12    useEffect(() => {
13      supabase
14        .from("client_notes")
15        .select("id, body, created_at")
16        .eq("client_id", clientId)
17        .order("created_at", { ascending: false })
18        .then(({ data }) => setNotes(data ?? []));
19    }, [clientId]);
20
21    async function add() {
22      const { data } = await supabase
23        .from("client_notes")
24        .insert({ client_id: clientId, body: draft })
25        .select("id, body, created_at")
26        .single();
27      if (data) setNotes([data, ...notes]);
28      setDraft("");
29    }
30
31    // TODO: move these labels to the i18n file when we add English
32    return (
33      <section>
34        <h2 className="font-medium">Notas</h2>
35        <textarea value={draft} onChange={(e) => setDraft(e.target.value)} className="w-full rounded border p-2" />
36        <button onClick={add} className="mt-1 rounded bg-primary px-3 py-1 text-sm text-primary-foreground">
37          Salvar nota
38        </button>
39        <ul className="mt-2 space-y-1 text-sm">
40          {notes.map((n) => (
41            <li key={n.id}>{n.body}</li>
42          ))}
43        </ul>
44      </section>
45    );
46  }
```

`supabase/migrations/20260901000000_init.sql`:

```sql
 1  create table public.profiles (
 2    id uuid primary key references auth.users on delete cascade,
 3    full_name text not null,
 4    role text not null default 'client' check (role in ('client', 'staff'))
 5  );
 6  alter table public.profiles enable row level security;
 7  create policy "own profile" on public.profiles for select using (auth.uid() = id);
 8
 9  create table public.services (
10    id uuid primary key default gen_random_uuid(),
11    name text not null,
12    duration_min int not null
13  );
14  alter table public.services enable row level security;
15  create policy "services are public" on public.services for select using (true);
16
17  create table public.bookings (
18    id uuid primary key default gen_random_uuid(),
19    client_id uuid not null references public.profiles (id),
20    service_id uuid not null references public.services (id),
21    starts_at timestamptz not null,
22    status text not null default 'confirmed'
23  );
24  alter table public.bookings enable row level security;
25  create policy "own bookings" on public.bookings for select using (auth.uid() = client_id);
26  create policy "book for self" on public.bookings for insert with check (auth.uid() = client_id);
27
28  create table public.client_notes (
29    id uuid primary key default gen_random_uuid(),
30    client_id uuid not null references public.profiles (id),
31    body text not null,
32    created_at timestamptz not null default now()
33  );
34
35  create view public.bookings_view with (security_invoker = true) as
36    select b.id, b.starts_at, p.full_name as client_name, s.name as service_name
37    from public.bookings b
38    join public.profiles p on p.id = b.client_id
39    join public.services s on s.id = b.service_id;
```
