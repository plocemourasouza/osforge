Bug report from the salon's shop (Next.js 15 App Router, TypeScript, Prisma on Supabase Postgres):
"On the products page the prices look wrong for Brazilian customers: it shows `R$ 49.9` and
`R$ 1234.5` instead of `R$ 49,90` and `R$ 1.234,50`." Fix it. Show me the change.

`prisma/schema.prisma` (excerpt):

```prisma
model Product {
  id             String  @id @default(cuid())
  name           String
  imageUrl       String
  priceCents     Int
  compareAtCents Int?    // the old price, shown struck through during a sale
  active         Boolean @default(true)
}
```

`components/shop/product-card.tsx`:

```tsx
import Image from "next/image";
import Link from "next/link";
import type { Product } from "@prisma/client";

export function ProductCard({ product }: { product: Product }) {
  return (
    <Link href={`/products/${product.id}`} className="group block rounded-lg border p-3">
      <Image src={product.imageUrl} alt={product.name} width={320} height={320} className="rounded-md" />
      <h3 className="mt-2 text-sm font-medium group-hover:underline">{product.name}</h3>
      <p className="mt-1 text-sm">
        <span className="font-semibold">R$ {product.priceCents / 100}</span>
        {product.compareAtCents && (
          <span className="ml-2 text-muted-foreground line-through">R$ {product.compareAtCents / 100}</span>
        )}
      </p>
    </Link>
  );
}
```
