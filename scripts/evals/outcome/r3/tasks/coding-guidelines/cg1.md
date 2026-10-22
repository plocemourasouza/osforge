Our salon booking app (Next.js 15 App Router, React 19, TypeScript, Tailwind, Prisma on Supabase
Postgres) only lets clients book "the next free slot". Clients want to pick the day. Add a date
picker to the booking form: the client picks a day from today up to 60 days ahead, and the booking
is made in the first free slot of that day. The chosen day must reach the `createBooking` Server
Action as `date` (`YYYY-MM-DD`). Show me the code changes.

`package.json` (dependencies):

```json
{
  "dependencies": {
    "@prisma/client": "6.4.1",
    "@supabase/ssr": "0.5.2",
    "@supabase/supabase-js": "2.48.1",
    "clsx": "2.1.1",
    "lucide-react": "0.475.0",
    "next": "15.2.4",
    "react": "19.0.0",
    "react-dom": "19.0.0",
    "tailwind-merge": "3.0.1",
    "zod": "3.24.2"
  }
}
```

`components/booking/booking-form.tsx`:

```tsx
"use client";
import { useActionState } from "react";
import { createBooking, type BookingState } from "@/app/(booking)/book/actions";

type Service = { id: string; name: string; durationMin: number };

export function BookingForm({ services }: { services: Service[] }) {
  const [state, action, pending] = useActionState<BookingState, FormData>(createBooking, {});

  return (
    <form action={action} className="space-y-4">
      <div className="space-y-1">
        <label htmlFor="serviceId" className="text-sm font-medium">Service</label>
        <select
          id="serviceId"
          name="serviceId"
          required
          className="h-10 w-full rounded-md border border-input bg-background px-3 text-sm"
        >
          {services.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name} ({s.durationMin} min)
            </option>
          ))}
        </select>
      </div>
      <button
        type="submit"
        disabled={pending}
        className="h-10 rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground disabled:opacity-50"
      >
        {pending ? "Booking..." : "Book the next free slot"}
      </button>
      {state.error && <p className="text-sm text-destructive">{state.error}</p>}
      {state.bookedAt && <p className="text-sm">Booked for {new Date(state.bookedAt).toLocaleString("pt-BR")}</p>}
    </form>
  );
}
```

`components/ui/input.tsx`:

```tsx
import * as React from "react";
import { cn } from "@/lib/utils";

export const Input = React.forwardRef<HTMLInputElement, React.ComponentProps<"input">>(
  ({ className, type, ...props }, ref) => (
    <input
      ref={ref}
      type={type}
      className={cn(
        "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
        "disabled:cursor-not-allowed disabled:opacity-50 aria-[invalid=true]:border-destructive",
        className,
      )}
      {...props}
    />
  ),
);
Input.displayName = "Input";
```

`components/account/profile-form.tsx` (excerpt, how the other forms use it):

```tsx
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
// ...
      <div className="space-y-1">
        <Label htmlFor="phone">Phone</Label>
        <Input id="phone" name="phone" type="tel" autoComplete="tel" required />
      </div>
```

`app/(booking)/book/actions.ts`:

```ts
"use server";
import { z } from "zod";
import { prisma } from "@/lib/db";
import { requireUser } from "@/lib/auth";
import { listSlotsForDay, nextFreeSlot } from "@/lib/slots";

const BookingInput = z.object({ serviceId: z.string().cuid() });

export type BookingState = { error?: string; bookedAt?: string };

export async function createBooking(_prev: BookingState, formData: FormData): Promise<BookingState> {
  const user = await requireUser();
  const parsed = BookingInput.safeParse(Object.fromEntries(formData));
  if (!parsed.success) return { error: "Pick a service." };

  const service = await prisma.service.findUniqueOrThrow({ where: { id: parsed.data.serviceId } });
  const slot = await nextFreeSlot(service);
  if (!slot) return { error: "No free slot in the next 60 days." };

  const booking = await prisma.booking.create({
    data: { userId: user.id, serviceId: service.id, startsAt: slot.start },
  });
  return { bookedAt: booking.startsAt.toISOString() };
}
```

`lib/slots.ts` (signatures; the staff calendar already uses `listSlotsForDay`):

```ts
export type Slot = { start: Date; end: Date };

/** Free slots for `service` on `day` ("YYYY-MM-DD", salon time, America/Sao_Paulo), in order. */
export async function listSlotsForDay(service: Service, day: string): Promise<Slot[]>;

/** First free slot for `service` from now, looking 60 days ahead; null when none. */
export async function nextFreeSlot(service: Service): Promise<Slot | null>;
```
