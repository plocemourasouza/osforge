Audit this repository: we inherited it last week and want to know what to fix first. Below are all of its source files except `package.json`, config, UI components, `lib/db.ts` (a single `PrismaClient`), `lib/pix.ts` (HMAC check of the Pix provider's signature) and `lib/auth.ts` (`requireUser()` / `requireAdmin()` redirect when there is no session or the role is wrong). Line numbers are shown on the left.

`README.md`:

```
1  # Atelier Wallet
2
3  Prepaid credit for a chain of 3 salons. Clients top up their wallet with Pix and pay their
4  appointments from the balance in the app. Admins see every wallet movement.
5
6  Stack: Next.js 15 (App Router), TypeScript, Prisma, Supabase Postgres (through the pooler),
7  Supabase Auth. Deployed on Vercel (serverless; concurrent requests run on separate instances).
8  Load: ~1,000 wallet payments a day, peaks on Saturday mornings; clients often pay from the
9  reception tablet and their phone at the same time. About 30,000 wallet movements a month.
```

`prisma/schema.prisma`:

```prisma
 1  model Wallet {
 2    id           String              @id @default(cuid())
 3    userId       String              @unique
 4    balance      Float               @default(0)
 5    transactions WalletTransaction[]
 6  }
 7
 8  model WalletTransaction {
 9    id        String   @id @default(cuid())
10    walletId  String
11    kind      String   // "TOPUP" | "PAYMENT"
12    amount    Float
13    bookingId String?
14    txid      String?  @unique // Pix transaction id, set for top-ups
15    createdAt DateTime @default(now())
16    wallet    Wallet   @relation(fields: [walletId], references: [id])
17
18    @@index([walletId, createdAt])
19  }
20
21  model Booking {
22    id        String   @id @default(cuid())
23    userId    String
24    serviceId String
25    startsAt  DateTime
26    paid      Boolean  @default(false)
27    service   Service  @relation(fields: [serviceId], references: [id])
28  }
29
30  model Service {
31    id       String    @id @default(cuid())
32    name     String
33    price    Float
34    bookings Booking[]
35  }
```

`app/(wallet)/pay/actions.ts`:

```ts
 1  "use server";
 2  import { z } from "zod";
 3  import { revalidatePath } from "next/cache";
 4  import { prisma } from "@/lib/db";
 5  import { requireUser } from "@/lib/auth";
 6
 7  const PayInput = z.object({ bookingId: z.string().cuid() });
 8
 9  export async function payWithWallet(_prev: unknown, formData: FormData) {
10    const user = await requireUser();
11    const { bookingId } = PayInput.parse(Object.fromEntries(formData));
12
13    const booking = await prisma.booking.findFirst({
14      where: { id: bookingId, userId: user.id, paid: false },
15      include: { service: true },
16    });
17    if (!booking) return { error: "Booking not found or already paid." };
18
19    const wallet = await prisma.wallet.findUniqueOrThrow({ where: { userId: user.id } });
20    const price = booking.service.price;
21    if (wallet.balance < price) return { error: "Insufficient balance." };
22
23    await prisma.wallet.update({
24      where: { id: wallet.id },
25      data: { balance: wallet.balance - price },
26    });
27    await prisma.walletTransaction.create({
28      data: { walletId: wallet.id, kind: "PAYMENT", amount: -price, bookingId },
29    });
30    await prisma.booking.update({ where: { id: bookingId }, data: { paid: true } });
31
32    revalidatePath("/wallet");
33    return { ok: true };
34  }
```

`app/api/webhooks/pix/route.ts`:

```ts
 1  import { NextResponse } from "next/server";
 2  import { Prisma } from "@prisma/client";
 3  import { z } from "zod";
 4  import { prisma } from "@/lib/db";
 5  import { verifyPixSignature } from "@/lib/pix";
 6
 7  const PixEvent = z.object({
 8    txid: z.string(),
 9    userId: z.string(),
10    amountCents: z.number().int().positive(),
11  });
12
13  export async function POST(req: Request) {
14    const raw = await req.text();
15    if (!verifyPixSignature(raw, req.headers.get("x-pix-signature"))) {
16      return NextResponse.json({ error: "invalid signature" }, { status: 401 });
17    }
18    const parsed = PixEvent.safeParse(JSON.parse(raw));
19    if (!parsed.success) return NextResponse.json({ error: "invalid payload" }, { status: 400 });
20    const event = parsed.data;
21    const amount = event.amountCents / 100;
22
23    try {
24      await prisma.$transaction([
25        prisma.walletTransaction.create({
26          data: { wallet: { connect: { userId: event.userId } }, kind: "TOPUP", amount, txid: event.txid },
27        }),
28        prisma.wallet.update({ where: { userId: event.userId }, data: { balance: { increment: amount } } }),
29      ]);
30    } catch (e) {
31      // Pix retries deliveries: a txid we already recorded is a duplicate, acknowledge it.
32      if (e instanceof Prisma.PrismaClientKnownRequestError && e.code === "P2002") {
33        return NextResponse.json({ ok: true, duplicate: true });
34      }
35      throw e;
36    }
37    return NextResponse.json({ ok: true });
38  }
```

`app/(admin)/movements/page.tsx`:

```tsx
 1  import { prisma } from "@/lib/db";
 2  import { requireAdmin } from "@/lib/auth";
 3  import { MovementsTable } from "@/components/admin/movements-table";
 4
 5  export default async function MovementsPage() {
 6    await requireAdmin();
 7    const movements = await prisma.walletTransaction.findMany({
 8      include: { wallet: true },
 9      orderBy: { createdAt: "desc" },
10    });
11    return <MovementsTable movements={movements} />;
12  }
```

`tests/pay.test.ts`:

```ts
 1  import { describe, expect, it } from "vitest";
 2  import { payWithWallet } from "@/app/(wallet)/pay/actions";
 3  import { seedWallet, seedBooking, signInAs, form } from "./helpers";
 4
 5  describe("payWithWallet", () => {
 6    it("pays a booking when the balance covers it", async () => {
 7      signInAs("u1");
 8      await seedWallet("u1", 100);
 9      const b = await seedBooking("u1", { price: 80 });
10      expect(await payWithWallet(null, form({ bookingId: b.id }))).toEqual({ ok: true });
11    });
12
13    it("refuses when the balance is too low", async () => {
14      signInAs("u1");
15      await seedWallet("u1", 50);
16      const b = await seedBooking("u1", { price: 80 });
17      expect(await payWithWallet(null, form({ bookingId: b.id }))).toEqual({ error: "Insufficient balance." });
18    });
19  });
```
