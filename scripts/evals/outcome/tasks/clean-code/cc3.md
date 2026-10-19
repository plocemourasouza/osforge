Users report that the "Total stock" badge in our admin always shows 0, even when items clearly have stock. Here is the function behind it. Fix it and explain what was wrong.

```ts
import { db } from "./db"; // db.getItem(id: string): Promise<{ id: string; stock: number }>

export async function totalStock(ids: string[]): Promise<number> {
  let total = 0;
  ids.forEach(async (id) => {
    const item = await db.getItem(id);
    total += item.stock;
  });
  return total;
}
```
