Review this pull request for our salon booking app (Next.js 15 App Router, TypeScript, Prisma on
Supabase Postgres, Supabase Auth). PR description: "Rename `Customer.phone` to `phoneNumber` and
store it in E.164 (`+5511987654321`) so we can send WhatsApp messages."

```diff
diff --git a/prisma/schema.prisma b/prisma/schema.prisma
@@ -21,7 +21,7 @@ model Customer {
   id          String    @id @default(cuid())
   userId      String    @unique @map("user_id")
   name        String
-  phone       String?
+  phoneNumber String?   @map("phone_number")
   email       String
   bookings    Booking[]

   @@map("customers")
 }
diff --git a/prisma/migrations/20261020120000_phone_number/migration.sql b/prisma/migrations/20261020120000_phone_number/migration.sql
new file mode 100644
@@ -0,0 +1,3 @@
+ALTER TABLE "customers" RENAME COLUMN "phone" TO "phone_number";
+UPDATE "customers" SET "phone_number" = '+55' || regexp_replace("phone_number", '\D', '', 'g')
+  WHERE "phone_number" IS NOT NULL AND "phone_number" NOT LIKE '+%';
diff --git a/app/(account)/profile/actions.ts b/app/(account)/profile/actions.ts
@@ -6,7 +6,10 @@ import { requireUser } from "@/lib/auth";
 const ProfileInput = z.object({
   name: z.string().trim().min(2).max(80),
-  phone: z.string().trim().max(20).optional(),
+  phoneNumber: z
+    .string()
+    .trim()
+    .transform((v) => "+55" + v.replace(/\D/g, "").replace(/^55/, ""))
+    .pipe(z.string().regex(/^\+55\d{10,11}$/, "Enter a Brazilian phone with area code"))
+    .optional(),
 });

 export async function updateProfile(_prev: ProfileState, formData: FormData): Promise<ProfileState> {
@@ -15,7 +18,7 @@ export async function updateProfile(_prev: ProfileState, formData: FormData): Pr
   if (!parsed.success) return { errors: parsed.error.flatten().fieldErrors };
   await prisma.customer.update({
     where: { userId: user.id },
-    data: { name: parsed.data.name, phone: parsed.data.phone },
+    data: { name: parsed.data.name, phoneNumber: parsed.data.phoneNumber },
   });
   revalidatePath("/profile");
   return { ok: true };
diff --git a/components/account/profile-form.tsx b/components/account/profile-form.tsx
@@ -24,8 +24,8 @@ export function ProfileForm({ customer }: { customer: Customer }) {
       <div className="space-y-1">
-        <Label htmlFor="phone">Phone</Label>
-        <Input id="phone" name="phone" type="tel" defaultValue={customer.phone ?? ""} />
+        <Label htmlFor="phoneNumber">Phone (with area code)</Label>
+        <Input id="phoneNumber" name="phoneNumber" type="tel" defaultValue={customer.phoneNumber ?? ""} />
         <FormMessage errors={state.errors?.phoneNumber} />
       </div>
```

Other files in the repository that read customers (unchanged by this PR, for context):

`app/(admin)/customers/page.tsx`:

```tsx
import { prisma } from "@/lib/db";
import { requireStaff } from "@/lib/auth";

export default async function CustomersPage() {
  await requireStaff();
  const customers = await prisma.customer.findMany({
    select: { id: true, name: true, email: true, _count: { select: { bookings: true } } },
    orderBy: { name: "asc" },
    take: 200,
  });
  return <CustomerTable customers={customers} />;
}
```

`supabase/functions/send-reminders/index.ts` (Supabase Edge Function, run every hour by `pg_cron`):

```ts
import { createClient } from "jsr:@supabase/supabase-js@2";
import { sendWhatsApp } from "../_shared/whatsapp.ts";

Deno.serve(async () => {
  const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const from = new Date(Date.now() + 23 * 3600_000).toISOString();
  const to = new Date(Date.now() + 24 * 3600_000).toISOString();

  const { data: bookings } = await supabase
    .from("bookings")
    .select("id, starts_at, customers(name, phone)")
    .gte("starts_at", from)
    .lt("starts_at", to)
    .eq("status", "CONFIRMED");

  for (const b of bookings ?? []) {
    if (!b.customers?.phone) continue;
    await sendWhatsApp(b.customers.phone, `Hi ${b.customers.name}, see you tomorrow at ${b.starts_at}!`);
  }
  return new Response("ok");
});
```

The CI runs `tsc --noEmit` and `vitest` for the Next.js app; the edge functions are deployed
separately with `supabase functions deploy` and have no tests.
