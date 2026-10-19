Review this pull request diff (Next.js App Router, TypeScript). The PR adds an endpoint so a user can delete one of their own saved payment methods.

```diff
--- /dev/null
+++ b/app/api/payment-methods/[id]/route.ts
@@ -0,0 +1,27 @@
+import { NextResponse } from "next/server";
+import { z } from "zod";
+import { getSession } from "@/lib/auth";
+import { db } from "@/lib/db";
+
+const Params = z.object({ id: z.string().uuid() });
+
+export async function DELETE(
+  _req: Request,
+  { params }: { params: Promise<{ id: string }> },
+) {
+  const session = await getSession();
+  if (!session) {
+    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
+  }
+
+  const parsed = Params.safeParse(await params);
+  if (!parsed.success) {
+    return NextResponse.json({ error: "Invalid id" }, { status: 400 });
+  }
+
+  await db.paymentMethod.delete({ where: { id: parsed.data.id } });
+
+  return new NextResponse(null, { status: 204 });
+}
```

Notes: `getSession()` returns `{ userId: string } | null` from an httpOnly session cookie. The `paymentMethod` model has `id` (uuid) and `userId` columns. The PR description says "users can delete their saved cards".
