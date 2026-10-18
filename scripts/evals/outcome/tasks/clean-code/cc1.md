This is our shipping cost module in a TypeScript checkout service. It feels heavy for what it does. Please refactor it, show the final code, and tell me what changes at the call site.

```ts
// shipping.ts
export interface ShippingStrategy {
  calculate(weightKg: number): number;
}

export class DomesticShippingStrategy implements ShippingStrategy {
  calculate(weightKg: number): number {
    return 5 + weightKg * 1.2;
  }
}

export class InternationalShippingStrategy implements ShippingStrategy {
  calculate(weightKg: number): number {
    return 15 + weightKg * 3.5;
  }
}

export class ShippingStrategyFactory {
  static create(countryCode: string): ShippingStrategy {
    if (countryCode === "BR") {
      return new DomesticShippingStrategy();
    }
    return new InternationalShippingStrategy();
  }
}

export class ShippingCalculator {
  constructor(private readonly factory = ShippingStrategyFactory) {}

  calculate(countryCode: string, weightKg: number): number {
    const strategy = this.factory.create(countryCode);
    return strategy.calculate(weightKg);
  }
}
```

```ts
// checkout.ts (the only consumer)
import { ShippingCalculator } from "./shipping";

const shipping = new ShippingCalculator();

export function orderTotal(subtotal: number, countryCode: string, weightKg: number): number {
  return subtotal + shipping.calculate(countryCode, weightKg);
}
```
