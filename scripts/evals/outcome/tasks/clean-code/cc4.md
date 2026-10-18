Please clean up this file: it has accumulated noise over time. Return the cleaned file and a short list of what you removed. Behavior must not change. `formatAmount` and `parseWebhookAmount` are imported elsewhere in the codebase; nothing else from this file is.

```ts
// money.ts
import { format } from "date-fns";
import Decimal from "decimal.js";

// This is the currency code type
type CurrencyCode = "BRL" | "USD" | "EUR";

// DEBUG flag
const DEBUG = false;

// function to format amount
export function formatAmount(cents: number, currency: CurrencyCode): string {
  // divide cents by 100
  const value = cents / 100;
  // check debug
  if (DEBUG) {
    console.log("formatting", cents, currency);
  }
  // return formatted
  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(value);
}

// old implementation, keep for reference
// export function formatAmountOld(cents: number) {
//   return "$" + (cents / 100).toFixed(2);
// }

function roundHalfEven(value: number): number {
  return new Decimal(value).toDecimalPlaces(0, Decimal.ROUND_HALF_EVEN).toNumber();
}

export function parseWebhookAmount(raw: number | string): number {
  // The payment provider's v2 webhooks sometimes send the amount as a string with a
  // trailing currency suffix ("1999 BRL"); v1 always sends a number. Both are in cents.
  if (typeof raw === "number") {
    return raw;
  }
  // parse the int
  const parsed = parseInt(raw, 10);
  if (Number.isNaN(parsed)) {
    throw new Error(`Invalid webhook amount: ${raw}`);
    return 0;
  }
  return parsed;
}

// helper to get today's date
function today(): string {
  return format(new Date(), "yyyy-MM-dd");
}
```
