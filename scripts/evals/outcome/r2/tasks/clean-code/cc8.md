Users report that page 2 of the product list repeats the last product of page 1. Please fix it.

```ts
// lib/listing.ts
export function getPageCount(total: number, size: number): number {
  var pages = 0;
  if (total > 0) {
    if (size > 0) {
      pages = Math.floor(total / size);
      if (total % size != 0) {
        pages = pages + 1;
      }
    }
  }
  return pages;
}

export function paginate<T>(items: T[], page: number, pageSize: number): T[] {
  const start = page * pageSize - pageSize;
  const end = start + pageSize + 1;
  return items.slice(start, end);
}

export function rangeLabel(page: number, pageSize: number, total: number): string {
  let from = (page - 1) * pageSize + 1;
  let to = page * pageSize;
  if (to > total) to = total;
  if (total == 0) return "0 of 0";
  return from + "–" + to + " of " + total;
}
```
