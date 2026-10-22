Review this pull request for our salon booking app (Next.js 15 App Router, TypeScript, Prisma on
Supabase Postgres). PR description: "Staff dashboard: endpoint with today's appointments, polled
by the reception tablet every 30 s."

```diff
diff --git a/app/api/staff/today/route.ts b/app/api/staff/today/route.ts
new file mode 100644
@@ -0,0 +1,44 @@
+import { NextResponse } from "next/server";
+import { prisma } from "@/lib/db";
+import { getStaffSession } from "@/lib/auth";
+
+type TodayItem = { id: string; startsAt: Date; customer: string; service: string; staff: string };
+
+// shortcut: per-instance in-memory cache with a 60 s TTL; fine for our single salon (~40 bookings/day,
+// one reception tablet); move to unstable_cache with tag revalidation when we open the second salon.
+const cache = new Map<string, { at: number; items: TodayItem[] }>();
+const TTL_MS = 60_000;
+
+export async function GET() {
+  const session = await getStaffSession();
+  if (!session) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
+
+  const today = new Date().toISOString().slice(0, 10); // "YYYY-MM-DD"
+  const key = `${session.salonId}:${today}`;
+  const hit = cache.get(key);
+  if (hit && Date.now() - hit.at < TTL_MS) return NextResponse.json(hit.items);
+
+  const from = new Date(`${today}T00:00:00`);
+  const to = new Date(`${today}T23:59:59.999`);
+  const bookings = await prisma.booking.findMany({
+    where: { salonId: session.salonId, startsAt: { gte: from, lte: to }, status: "CONFIRMED" },
+    include: { customer: true, service: true, staff: true },
+    orderBy: { startsAt: "asc" },
+  });
+
+  const items = bookings.map((b) => ({
+    id: b.id,
+    startsAt: b.startsAt,
+    customer: b.customer.name,
+    service: b.service.name,
+    staff: b.staff.name,
+  }));
+  cache.set(key, { at: Date.now(), items });
+  return NextResponse.json(items);
+}
```

`README.md` (excerpt):

> One salon in Porto Alegre (America/Sao_Paulo, UTC-03:00, no daylight saving time), open
> 09:00-22:00 Monday to Saturday, ~40 bookings a day, 3 stylists, one reception tablet. Deployed on
> Vercel; functions run in UTC. `Booking.startsAt` is `timestamptz`.
