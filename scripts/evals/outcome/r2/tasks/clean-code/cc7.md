Please review this PR before I merge it. Context: TypeScript strict, Next.js 15 App Router. PR description: "Add endpoint to update a customer's marketing preferences."

```diff
diff --git a/app/api/customers/[id]/preferences/route.ts b/app/api/customers/[id]/preferences/route.ts
new file mode 100644
--- /dev/null
+++ b/app/api/customers/[id]/preferences/route.ts
@@ -0,0 +1,29 @@
+import { NextResponse } from "next/server";
+import { getSession } from "@/lib/auth";
+import updatePreferences from "@/lib/customers/preferences";
+
+export async function PATCH(req: Request, { params }: { params: Promise<{ id: string }> }) {
+  const session = await getSession();
+  if (!session) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
+  const { id } = await params;
+  const body: any = await req.json();
+
+  try {
+    const customer = await updatePreferences(session.tenantId, id, body);
+    console.log(`preferences updated for ${customer.email}`);
+    return NextResponse.json(customer);
+  } catch (e) {
+    return NextResponse.json({ ok: true });
+  }
+}
diff --git a/lib/customers/preferences.ts b/lib/customers/preferences.ts
new file mode 100644
--- /dev/null
+++ b/lib/customers/preferences.ts
@@ -0,0 +1,24 @@
+import { prisma } from "@/lib/db";
+
+export interface PreferencesInput {
+  newsletter: boolean;
+  sms: boolean;
+}
+
+export default async function updatePreferences(
+  tenantId: string,
+  customerId: string,
+  input: PreferencesInput,
+  options: { auditLog?: boolean; retries?: number } = { auditLog: true, retries: 3 },
+) {
+  return prisma.customer.update({
+    where: { id: customerId, tenantId },
+    data: { newsletter: input.newsletter, sms: input.sms },
+  });
+}
```
