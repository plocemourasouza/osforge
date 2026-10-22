Audit this repository before our first public release: what should we fix? Below are all of its source files except `package.json`, config, UI components, `lib/db.ts` (a single `PrismaClient`), `tests/helpers.ts` and `lib/auth.ts` (`requireUser()` / `requireStaff()` read the Supabase session on the server and redirect when it is missing or the role is wrong; `requireStaff()` returns the staff `Profile`). Line numbers are shown on the left.

`README.md`:

```
1  # Atelier Booking
2
3  Online booking for one salon in Porto Alegre (America/Sao_Paulo, UTC-03:00, no DST). Clients sign in
4  with Supabase Auth (magic link) and book a service with a stylist; the stylists see the day's agenda.
5  Payment happens at the salon.
6
7  Stack: Next.js 15 (App Router), TypeScript, Prisma (server-side only, direct connection), Supabase
8  Postgres and Auth, Zod, Vitest. Deployed on Vercel in one region (gru1). Load: ~40 bookings a day,
9  3 stylists, a few hundred clients. CI runs `tsc --noEmit`, `eslint` and `vitest` (with a test database).
```

`prisma/schema.prisma`:

```prisma
 1  enum Role {
 2    CLIENT
 3    STAFF
 4  }
 5
 6  enum BookingStatus {
 7    CONFIRMED
 8    CANCELLED
 9  }
10
11  model Profile {
12    id       String    @id @db.Uuid // = auth.users.id
13    name     String
14    role     Role      @default(CLIENT)
15    bookings Booking[] @relation("client")
16    agenda   Booking[] @relation("staff")
17  }
18
19  model Service {
20    id          String    @id @default(cuid())
21    name        String
22    durationMin Int
23    priceCents  Int
24    active      Boolean   @default(true)
25    bookings    Booking[]
26  }
27
28  model Booking {
29    id         String        @id @default(cuid())
30    clientId   String        @db.Uuid
31    staffId    String        @db.Uuid
32    serviceId  String
33    startsAt   DateTime      @db.Timestamptz
34    endsAt     DateTime      @db.Timestamptz
35    priceCents Int
36    status     BookingStatus @default(CONFIRMED)
37    client     Profile       @relation("client", fields: [clientId], references: [id])
38    staff      Profile       @relation("staff", fields: [staffId], references: [id])
39    service    Service       @relation(fields: [serviceId], references: [id])
40
41    @@index([staffId, startsAt])
42    @@index([clientId, startsAt])
43  }
```

`supabase/migrations/20260915000000_lock_postgrest.sql`:

```sql
1  -- Prisma owns the schema. The app reaches these tables only through Prisma on the server
2  -- (the table owner), so the PostgREST roles get nothing.
3  alter table "Profile" enable row level security;
4  alter table "Service" enable row level security;
5  alter table "Booking" enable row level security;
6  revoke all on "Profile", "Service", "Booking" from anon, authenticated;
```

`app/(booking)/book/actions.ts`:

```ts
 1  "use server";
 2  import { z } from "zod";
 3  import { Prisma } from "@prisma/client";
 4  import { revalidatePath } from "next/cache";
 5  import { prisma } from "@/lib/db";
 6  import { requireUser } from "@/lib/auth";
 7  import { rateLimit } from "@/lib/rate-limit";
 8  import { isWithinOpeningHours } from "@/lib/salon-time";
 9
10  const BookInput = z.object({
11    serviceId: z.string().cuid(),
12    staffId: z.string().uuid(),
13    startsAt: z.string().datetime({ offset: true }),
14  });
15
16  export type BookState = { error?: string; bookingId?: string };
17
18  export async function book(_prev: BookState, formData: FormData): Promise<BookState> {
19    const user = await requireUser();
20    if (!rateLimit(`book:${user.id}`, 5, 60_000)) return { error: "Too many attempts, try again in a minute." };
21
22    const parsed = BookInput.safeParse(Object.fromEntries(formData));
23    if (!parsed.success) return { error: "Invalid booking." };
24    const startsAt = new Date(parsed.data.startsAt);
25    if (startsAt.getTime() < Date.now()) return { error: "That time has passed." };
26
27    const service = await prisma.service.findFirst({ where: { id: parsed.data.serviceId, active: true } });
28    const staff = await prisma.profile.findFirst({ where: { id: parsed.data.staffId, role: "STAFF" } });
29    if (!service || !staff) return { error: "Invalid booking." };
30    if (!isWithinOpeningHours(startsAt, service.durationMin)) return { error: "Outside opening hours." };
31    const endsAt = new Date(startsAt.getTime() + service.durationMin * 60_000);
32
33    const taken = { error: "That time was just taken. Please pick another." };
34    try {
35      // Serializable: two clients racing for overlapping times cannot both pass the check.
36      const booking = await prisma.$transaction(
37        async (tx) => {
38          const clash = await tx.booking.findFirst({
39            where: { staffId: staff.id, status: "CONFIRMED", startsAt: { lt: endsAt }, endsAt: { gt: startsAt } },
40          });
41          if (clash) return null;
42          return tx.booking.create({
43            data: {
44              clientId: user.id,
45              staffId: staff.id,
46              serviceId: service.id,
47              startsAt,
48              endsAt,
49              priceCents: service.priceCents, // price fixed at booking time, from the server
50            },
51          });
52        },
53        { isolationLevel: Prisma.TransactionIsolationLevel.Serializable },
54      );
55      if (!booking) return taken;
56      revalidatePath("/bookings");
57      return { bookingId: booking.id };
58    } catch (e) {
59      // P2034 = serialization failure: a concurrent booking won the race.
60      if (e instanceof Prisma.PrismaClientKnownRequestError && e.code === "P2034") return taken;
61      throw e;
62    }
63  }
```

`app/(staff)/agenda/page.tsx`:

```tsx
 1  import { prisma } from "@/lib/db";
 2  import { requireStaff } from "@/lib/auth";
 3  import { salonDayRange, todayInSalon } from "@/lib/salon-time";
 4
 5  export default async function AgendaPage({ searchParams }: { searchParams: Promise<{ day?: string }> }) {
 6    const staff = await requireStaff();
 7    const { day } = await searchParams;
 8    const { from, to } = salonDayRange(/^\d{4}-\d{2}-\d{2}$/.test(day ?? "") ? day! : todayInSalon());
 9
10    const bookings = await prisma.booking.findMany({
11      where: { staffId: staff.id, status: "CONFIRMED", startsAt: { gte: from, lt: to } },
12      select: { id: true, startsAt: true, client: { select: { name: true } }, service: { select: { name: true } } },
13      orderBy: { startsAt: "asc" },
14      take: 100,
15    });
16
17    return (
18      <ul className="divide-y">
19        {bookings.map((b) => (
20          <li key={b.id} className="py-2 text-sm">
21            {b.startsAt.toLocaleTimeString("pt-BR", { timeZone: "America/Sao_Paulo", hour: "2-digit", minute: "2-digit" })}{" "}
22            {b.client.name}: {b.service.name}
23          </li>
24        ))}
25      </ul>
26    );
27  }
```

`lib/salon-time.ts`:

```ts
 1  const TZ = "America/Sao_Paulo";
 2
 3  /** "YYYY-MM-DD" of the current day in salon time. */
 4  export function todayInSalon(now = new Date()): string {
 5    return new Intl.DateTimeFormat("en-CA", { timeZone: TZ }).format(now);
 6  }
 7
 8  /** True when [start, start + minutes) is inside opening hours: Monday-Saturday 09:00-20:00 salon time. */
 9  export function isWithinOpeningHours(start: Date, minutes: number): boolean {
10    const wall = new Date(start.getTime() - 3 * 60 * 60 * 1000); // UTC-03:00 wall clock, read with getUTC*
11    const startMin = wall.getUTCHours() * 60 + wall.getUTCMinutes();
12    return wall.getUTCDay() !== 0 && startMin >= 9 * 60 && startMin + minutes <= 20 * 60;
13  }
14
15  /** Start and end (exclusive) of a salon day. Brazil has had no DST since 2019, so the offset is fixed. */
16  export function salonDayRange(day: string): { from: Date; to: Date } {
17    const from = new Date(`${day}T00:00:00-03:00`);
18    return { from, to: new Date(from.getTime() + 24 * 60 * 60 * 1000) };
19  }
```

`lib/rate-limit.ts`:

```ts
 1  // shortcut: per-instance in-memory limiter; fine for one region and ~40 bookings/day, where it only
 2  // stops accidental double submits; move to Upstash Redis if bots show up or we add a second region.
 3  const hits = new Map<string, number[]>();
 4
 5  export function rateLimit(key: string, max: number, windowMs: number): boolean {
 6    const now = Date.now();
 7    const recent = (hits.get(key) ?? []).filter((t) => now - t < windowMs);
 8    if (recent.length >= max) return false;
 9    recent.push(now);
10    hits.set(key, recent);
11    return true;
12  }
```

`tests/book.test.ts`:

```ts
 1  import { beforeEach, describe, expect, it } from "vitest";
 2  import { book } from "@/app/(booking)/book/actions";
 3  import { form, resetDb, seedService, seedStaff, signInAs } from "./helpers";
 4  import { isWithinOpeningHours, salonDayRange, todayInSalon } from "@/lib/salon-time";
 5
 6  describe("book", () => {
 7    beforeEach(resetDb);
 8
 9    it("books a free slot at the server's price", async () => {
10      signInAs("client-1");
11      const s = await seedService({ priceCents: 9000, durationMin: 60 });
12      const st = await seedStaff();
13      const r = await book({}, form({ serviceId: s.id, staffId: st.id, startsAt: "2030-01-10T14:00:00-03:00" }));
14      expect(r.bookingId).toBeDefined();
15    });
16
17    it("refuses an overlapping booking for the same stylist", async () => {
18      const s = await seedService({ priceCents: 9000, durationMin: 60 });
19      const st = await seedStaff();
20      signInAs("client-1");
21      await book({}, form({ serviceId: s.id, staffId: st.id, startsAt: "2030-01-10T14:00:00-03:00" }));
22      signInAs("client-2");
23      const r = await book({}, form({ serviceId: s.id, staffId: st.id, startsAt: "2030-01-10T14:30:00-03:00" }));
24      expect(r.error).toMatch(/just taken/);
25    });
26
27    it("refuses a time in the past", async () => {
28      signInAs("client-1");
29      const s = await seedService({ priceCents: 9000, durationMin: 60 });
30      const st = await seedStaff();
31      const r = await book({}, form({ serviceId: s.id, staffId: st.id, startsAt: "2020-01-10T14:00:00-03:00" }));
32      expect(r.error).toBeDefined();
33    });
34
35    it("computes the salon day in salon time", () => {
36      expect(todayInSalon(new Date("2026-10-23T01:30:00Z"))).toBe("2026-10-22");
37      expect(salonDayRange("2026-10-22").from.toISOString()).toBe("2026-10-22T03:00:00.000Z");
38    });
39
40    it("knows the opening hours", () => {
41      expect(isWithinOpeningHours(new Date("2026-10-22T19:00:00-03:00"), 60)).toBe(true);
42      expect(isWithinOpeningHours(new Date("2026-10-22T19:30:00-03:00"), 60)).toBe(false);
43      expect(isWithinOpeningHours(new Date("2026-10-25T10:00:00-03:00"), 60)).toBe(false); // Sunday
44    });
45  });
```
