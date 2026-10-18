Review this diff (TypeScript strict, Vitest).

```diff
diff --git a/lib/invoices/status.ts b/lib/invoices/status.ts
@@ -1,3 +1,18 @@
 import type { Invoice } from "@/lib/invoices/types";
+
+const DAY_MS = 24 * 60 * 60 * 1000;
+
+/** An invoice is overdue when it is unpaid and its due date is strictly before `now`. */
+export function isOverdue(invoice: Pick<Invoice, "dueDate" | "paidAt">, now: Date): boolean {
+  return invoice.paidAt === null && invoice.dueDate.getTime() < now.getTime();
+}
+
+/** Whole days overdue (0 when not overdue). */
+export function daysOverdue(invoice: Pick<Invoice, "dueDate" | "paidAt">, now: Date): number {
+  if (!isOverdue(invoice, now)) return 0;
+  return Math.floor((now.getTime() - invoice.dueDate.getTime()) / DAY_MS);
+}
diff --git a/lib/invoices/status.test.ts b/lib/invoices/status.test.ts
@@ -1,2 +1,33 @@
 import { describe, expect, it } from "vitest";
+import { daysOverdue, isOverdue } from "./status";
+
+const due = new Date("2026-03-10T00:00:00Z");
+
+describe("isOverdue", () => {
+  it("is false before the due date", () => {
+    expect(isOverdue({ dueDate: due, paidAt: null }, new Date("2026-03-09T23:59:59Z"))).toBe(false);
+  });
+  it("is false exactly at the due date", () => {
+    expect(isOverdue({ dueDate: due, paidAt: null }, due)).toBe(false);
+  });
+  it("is true after the due date when unpaid", () => {
+    expect(isOverdue({ dueDate: due, paidAt: null }, new Date("2026-03-10T00:00:01Z"))).toBe(true);
+  });
+  it("is false when paid, even after the due date", () => {
+    expect(isOverdue({ dueDate: due, paidAt: new Date("2026-03-12T00:00:00Z") }, new Date("2026-03-20T00:00:00Z"))).toBe(false);
+  });
+});
+
+describe("daysOverdue", () => {
+  it("is 0 when not overdue", () => {
+    expect(daysOverdue({ dueDate: due, paidAt: null }, due)).toBe(0);
+  });
+  it("counts whole days", () => {
+    expect(daysOverdue({ dueDate: due, paidAt: null }, new Date("2026-03-13T12:00:00Z"))).toBe(3);
+  });
+});
```

`Invoice` has `dueDate: Date` and `paidAt: Date | null`.
