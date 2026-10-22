Review this pull request for our salon booking app (Next.js 15 App Router, React 19, TypeScript,
Prisma on Supabase Postgres). PR description: "Clients can cancel their own booking online up to
24 h before it starts. Inside 24 h they must call the salon (policy unchanged)."

```diff
diff --git a/app/(account)/bookings/actions.ts b/app/(account)/bookings/actions.ts
@@ -1,9 +1,36 @@
 "use server";
 import { revalidatePath } from "next/cache";
+import { z } from "zod";
 import { prisma } from "@/lib/db";
 import { requireUser } from "@/lib/auth";

+const CANCEL_WINDOW_MS = 24 * 60 * 60 * 1000;
+const CancelInput = z.object({ bookingId: z.string().cuid() });
+
+export type CancelState = { ok?: boolean; error?: string };
+
+export async function cancelBooking(_prev: CancelState, formData: FormData): Promise<CancelState> {
+  const user = await requireUser();
+  const parsed = CancelInput.safeParse(Object.fromEntries(formData));
+  if (!parsed.success) return { error: "Invalid booking." };
+
+  // One conditional update: ownership, status and the 24 h window are checked by the database,
+  // so two clicks (or two tabs) cannot both cancel, and nobody can cancel someone else's booking.
+  const { count } = await prisma.booking.updateMany({
+    where: {
+      id: parsed.data.bookingId,
+      userId: user.id,
+      status: "CONFIRMED",
+      startsAt: { gt: new Date(Date.now() + CANCEL_WINDOW_MS) },
+    },
+    data: { status: "CANCELLED", cancelledAt: new Date() },
+  });
+  if (count === 0) {
+    return { error: "This booking can't be cancelled online. Less than 24 h to go? Please call the salon." };
+  }
+
+  revalidatePath("/bookings");
+  return { ok: true };
+}
diff --git a/components/account/cancel-booking-button.tsx b/components/account/cancel-booking-button.tsx
new file mode 100644
@@ -0,0 +1,27 @@
+"use client";
+import { useActionState } from "react";
+import { cancelBooking, type CancelState } from "@/app/(account)/bookings/actions";
+import { Button } from "@/components/ui/button";
+
+export function CancelBookingButton({ bookingId }: { bookingId: string }) {
+  const [state, action, pending] = useActionState<CancelState, FormData>(cancelBooking, {});
+  if (state.ok) return <p className="text-sm text-muted-foreground">Booking cancelled.</p>;
+
+  return (
+    <form
+      action={action}
+      onSubmit={(e) => {
+        if (!confirm("Cancel this booking?")) e.preventDefault();
+      }}
+    >
+      <input type="hidden" name="bookingId" value={bookingId} />
+      <Button type="submit" variant="outline" size="sm" disabled={pending}>
+        {pending ? "Cancelling..." : "Cancel booking"}
+      </Button>
+      {state.error && (
+        <p role="alert" className="mt-1 text-sm text-destructive">{state.error}</p>
+      )}
+    </form>
+  );
+}
diff --git a/app/(account)/bookings/actions.test.ts b/app/(account)/bookings/actions.test.ts
new file mode 100644
@@ -0,0 +1,52 @@
+import { beforeEach, describe, expect, it, vi } from "vitest";
+import { prisma } from "@/lib/db";
+import { cancelBooking } from "./actions";
+import { createTestBooking, signInAs } from "@/test/factories";
+
+vi.mock("next/cache", () => ({ revalidatePath: vi.fn() }));
+
+const form = (bookingId: string) => {
+  const fd = new FormData();
+  fd.set("bookingId", bookingId);
+  return fd;
+};
+
+describe("cancelBooking", () => {
+  beforeEach(() => signInAs("user_a"));
+
+  it("cancels an own booking more than 24 h ahead", async () => {
+    const b = await createTestBooking({ userId: "user_a", startsInHours: 48 });
+    expect(await cancelBooking({}, form(b.id))).toEqual({ ok: true });
+    expect((await prisma.booking.findUniqueOrThrow({ where: { id: b.id } })).status).toBe("CANCELLED");
+  });
+
+  it("refuses inside 24 h", async () => {
+    const b = await createTestBooking({ userId: "user_a", startsInHours: 23 });
+    expect((await cancelBooking({}, form(b.id))).error).toBeDefined();
+    expect((await prisma.booking.findUniqueOrThrow({ where: { id: b.id } })).status).toBe("CONFIRMED");
+  });
+
+  it("refuses someone else's booking", async () => {
+    const b = await createTestBooking({ userId: "user_b", startsInHours: 48 });
+    expect((await cancelBooking({}, form(b.id))).error).toBeDefined();
+    expect((await prisma.booking.findUniqueOrThrow({ where: { id: b.id } })).status).toBe("CONFIRMED");
+  });
+
+  it("is idempotent: a second cancel does nothing", async () => {
+    const b = await createTestBooking({ userId: "user_a", startsInHours: 48 });
+    await cancelBooking({}, form(b.id));
+    expect((await cancelBooking({}, form(b.id))).error).toBeDefined();
+  });
+
+  it("rejects a malformed id", async () => {
+    expect(await cancelBooking({}, form("not-an-id"))).toEqual({ error: "Invalid booking." });
+  });
+});
```

Context: `Booking` has `id String @id @default(cuid())`, `userId String`, `startsAt DateTime`
(`timestamptz`), `status BookingStatus` (`CONFIRMED | CANCELLED | DONE | NO_SHOW`), `cancelledAt DateTime?`.
`requireUser()` redirects to `/login` when there is no session. Bookings are paid at the salon (no
online payment, nothing to refund). The freed slot becomes bookable again because slot search ignores
`CANCELLED` bookings (unchanged code). `@/test/factories` and the test database already exist and are
used by the other action tests.
