Production is throwing this since yesterday's deploy, only for some users (support says "mostly brand-new accounts"):

```
TypeError: Cannot read properties of undefined (reading 'map')
    at OrdersTable (app/(app)/orders/orders-table.tsx:14:27)
    at renderWithHooks (react-dom.production.js:…)
```

```tsx
// app/(app)/orders/orders-table.tsx
"use client";
import useSWR from "swr";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export function OrdersTable() {
  const { data, isLoading } = useSWR<{ orders: Order[] }>("/api/orders", fetcher);
  if (isLoading || !data) return <Spinner />;

  return (
    <table>
      <tbody>
        {data.orders.map((o) => (
          <OrderRow key={o.id} order={o} />
        ))}
      </tbody>
    </table>
  );
}
```

```ts
// app/api/orders/route.ts  (changed in yesterday's deploy)
export async function GET() {
  const session = await requireSession();
  const orders = await listOrders(session.tenantId, session.userId);
  return NextResponse.json(orders.length ? { orders } : []);
}
```
