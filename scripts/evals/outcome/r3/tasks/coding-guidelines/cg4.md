Our payment provider's webhook route (Next.js 15 App Router route handler, TypeScript, Prisma on
Supabase Postgres) has two problems in production:

1. When the provider started sending a new event type (`charge.dispute_opened`) the route crashed
   with `TypeError: Cannot read properties of undefined (reading 'id')`, the provider kept retrying,
   and our logs filled up.
2. Yesterday a malformed `charge.paid` event (an `amount` of `0` and no `currency`) marked order
   `cm7x...` as PAID.

Add proper validation of the webhook payload. Show me the new version of the route.

`package.json` (dependencies, excerpt): `"next": "15.2.4"`, `"@prisma/client": "6.4.1"`,
`"zod": "3.24.2"`.

`app/api/webhooks/payflow/route.ts`:

```ts
import { createHmac, timingSafeEqual } from "node:crypto";
import { NextResponse } from "next/server";
import { prisma } from "@/lib/db";

export const runtime = "nodejs";

function validSignature(raw: string, header: string | null): boolean {
  if (!header) return false;
  const expected = createHmac("sha256", process.env.PAYFLOW_WEBHOOK_SECRET!).update(raw).digest("hex");
  const a = Buffer.from(expected, "hex");
  const b = Buffer.from(header, "hex");
  return a.length === b.length && timingSafeEqual(a, b);
}

export async function POST(req: Request) {
  const raw = await req.text();
  if (!validSignature(raw, req.headers.get("x-payflow-signature"))) {
    return NextResponse.json({ error: "invalid signature" }, { status: 401 });
  }

  const event = JSON.parse(raw);
  const orderId = event.data.metadata.orderId;

  if (event.type === "charge.paid") {
    await prisma.order.update({
      where: { id: orderId },
      data: { status: "PAID", paidAt: new Date(), chargeId: event.data.id },
    });
  } else if (event.type === "charge.refunded") {
    await prisma.order.update({ where: { id: orderId }, data: { status: "REFUNDED" } });
  }

  return NextResponse.json({ received: true });
}
```

Provider docs, event shape for the two events we handle:

```json
{
  "id": "evt_01J...",
  "type": "charge.paid",
  "data": {
    "id": "ch_01J...",
    "amount": 4990,
    "currency": "BRL",
    "metadata": { "orderId": "cm7x2k9qz0003l808abcd1234" }
  }
}
```

`amount` is an integer in cents. The provider retries any non-2xx response for 3 days.

`app/api/slots/route.ts` (another route, for reference):

```ts
import { z } from "zod";
import { NextResponse } from "next/server";
import { listSlotsForDay } from "@/lib/slots";
import { prisma } from "@/lib/db";

const Query = z.object({ serviceId: z.string().cuid(), day: z.string().regex(/^\d{4}-\d{2}-\d{2}$/) });

export async function GET(req: Request) {
  const parsed = Query.safeParse(Object.fromEntries(new URL(req.url).searchParams));
  if (!parsed.success) return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
  const service = await prisma.service.findUnique({ where: { id: parsed.data.serviceId } });
  if (!service) return NextResponse.json({ error: "not found" }, { status: 404 });
  return NextResponse.json(await listSlotsForDay(service, parsed.data.day));
}
```

The `Order` model has `id String @id`, `status OrderStatus`, `totalCents Int`, `paidAt DateTime?`,
`chargeId String?`.
