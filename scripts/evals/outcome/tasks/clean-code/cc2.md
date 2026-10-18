Please review this function from our order-processing service. Tell me what is wrong with it from a code-quality standpoint, then show how you would restructure it. Keep its observable behavior identical (same return values, same thrown errors, same calls to `notify`).

```ts
type Item = { sku: string; qty: number; unitPrice: number; category: "food" | "electronics" | "other" };
type Customer = { id: string; tier: "basic" | "gold" | "platinum"; country: string; blocked: boolean };
type Order = { id: string; customer: Customer | null; items: Item[]; coupon?: string; status: string };

declare function notify(customerId: string, message: string): void;

export function processOrder(order: Order): { total: number; status: string } {
  let total = 0;
  if (order) {
    if (order.customer) {
      if (!order.customer.blocked) {
        if (order.items && order.items.length > 0) {
          for (let i = 0; i < order.items.length; i++) {
            const it = order.items[i];
            if (it.qty > 0) {
              if (it.category === "food") {
                if (order.customer.country === "BR") {
                  total += it.qty * it.unitPrice * 1.07;
                } else {
                  total += it.qty * it.unitPrice * 1.12;
                }
              } else if (it.category === "electronics") {
                if (order.customer.country === "BR") {
                  total += it.qty * it.unitPrice * 1.18;
                } else {
                  total += it.qty * it.unitPrice * 1.2;
                }
              } else {
                if (order.customer.country === "BR") {
                  total += it.qty * it.unitPrice * 1.1;
                } else {
                  total += it.qty * it.unitPrice * 1.15;
                }
              }
            }
          }
          if (order.customer.tier === "gold") {
            if (total > 500) {
              total = total * 0.95;
            }
          } else if (order.customer.tier === "platinum") {
            if (total > 500) {
              total = total * 0.9;
            } else {
              total = total * 0.95;
            }
          }
          if (order.coupon) {
            if (order.coupon === "WELCOME10") {
              if (total > 100) {
                total = total - 10;
              }
            } else if (order.coupon === "FREESHIP") {
              // shipping handled elsewhere
            } else {
              order.status = "invalid_coupon";
              notify(order.customer.id, "Coupon " + order.coupon + " is invalid");
              return { total: 0, status: order.status };
            }
          }
          total = Math.round(total * 100) / 100;
          if (total > 10000) {
            order.status = "needs_review";
            notify(order.customer.id, "Your order " + order.id + " is under review");
          } else {
            order.status = "confirmed";
            notify(order.customer.id, "Your order " + order.id + " is confirmed");
          }
          return { total: total, status: order.status };
        } else {
          order.status = "empty";
          return { total: 0, status: order.status };
        }
      } else {
        order.status = "blocked";
        notify(order.customer.id, "Your account is blocked");
        return { total: 0, status: order.status };
      }
    } else {
      throw new Error("Order has no customer");
    }
  } else {
    throw new Error("No order");
  }
}
```
