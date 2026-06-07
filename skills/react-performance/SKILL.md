---
name: react-performance
description: React and Next.js performance optimization rules from Vercel Engineering. Use when writing, reviewing, or refactoring React components, Next.js pages, data fetching, Server Components, Client Components, or bundle optimization. Triggers on performance issues, slow pages, large bundles, unnecessary re-renders, or waterfall fetching patterns.
---

# React & Next.js Performance Rules

57 rules from Vercel Engineering, organized by impact. Apply the highest-priority rules first.

## CRITICAL — Eliminating Waterfalls

**async-parallel**: Use `Promise.all()` for independent operations.
```typescript
// ❌ Sequential waterfalls
const user = await getUser(id)
const orders = await getOrders(id)
const notifications = await getNotifications(id)

// ✅ Parallel
const [user, orders, notifications] = await Promise.all([
  getUser(id), getOrders(id), getNotifications(id)
])
```

**async-defer-await**: Move `await` into branches where actually used.
```typescript
// ❌ Blocks even when not needed
const data = await fetchData()
if (condition) return cachedResult
return process(data)

// ✅ Defer await
const dataPromise = fetchData()
if (condition) return cachedResult
return process(await dataPromise)
```

**async-suspense-boundaries**: Use Suspense to stream content progressively.
```tsx
<Suspense fallback={<Skeleton />}>
  <SlowComponent />
</Suspense>
```

## CRITICAL — Bundle Size

**bundle-barrel-imports**: Import directly, never from barrel files.
```typescript
// ❌ Pulls entire barrel
import { Button } from '@/components'

// ✅ Direct import
import { Button } from '@/components/ui/button'
```

**bundle-dynamic-imports**: Use `next/dynamic` for heavy components.
```typescript
const Chart = dynamic(() => import('@/components/chart'), {
  loading: () => <Skeleton className="h-64" />,
  ssr: false,
})
```

**bundle-defer-third-party**: Load analytics/logging after hydration.
```typescript
useEffect(() => {
  import('analytics').then(m => m.init())
}, [])
```

## HIGH — Server-Side Performance

**server-auth-actions**: Authenticate Server Actions like API routes.
```typescript
export async function createPost(formData: FormData) {
  'use server'
  const session = await auth() // Always verify!
  if (!session) return { error: 'Unauthorized' }
}
```

**server-cache-react**: Use `React.cache()` for per-request deduplication.
```typescript
export const getUser = cache(async (id: string) => {
  return prisma.user.findUnique({ where: { id } })
})
```

**server-serialization**: Minimize data passed to client components.
```tsx
// ❌ Passes entire user object to client
<ClientComponent user={user} />

// ✅ Pass only what client needs
<ClientComponent name={user.name} avatar={user.avatar} />
```

**server-parallel-fetching**: Restructure components to parallelize fetches.
```tsx
// ❌ Sequential: parent fetches then child fetches
async function Page() {
  const user = await getUser() // blocks
  return <Dashboard user={user} /> // then Dashboard fetches orders
}

// ✅ Parallel: fetch at same level
async function Page() {
  const userPromise = getUser()
  const ordersPromise = getOrders()
  return <Dashboard userPromise={userPromise} ordersPromise={ordersPromise} />
}
```

## MEDIUM — Re-render Optimization

**rerender-derived-state**: Derive state during render, not in effects.
```typescript
// ❌ Unnecessary effect + state
const [filtered, setFiltered] = useState(items)
useEffect(() => {
  setFiltered(items.filter(i => i.active))
}, [items])

// ✅ Derive during render
const filtered = useMemo(() => items.filter(i => i.active), [items])
```

**rerender-functional-setstate**: Use functional setState for stable callbacks.
```typescript
// ❌ Recreates callback on every render
const increment = () => setCount(count + 1)

// ✅ Stable callback
const increment = useCallback(() => setCount(prev => prev + 1), [])
```

**rerender-memo**: Extract expensive work into memoized components.
```tsx
// Expensive child won't re-render when parent state changes
const ExpensiveList = memo(({ items }: Props) => {
  return items.map(item => <ExpensiveRow key={item.id} item={item} />)
})
```

## Diagnosing Before Optimizing

Always measure first — never optimize on a hunch.

### React DevTools Profiler
1. Open React DevTools → Profiler tab → click Record, interact with the slow UI, stop
2. Read the flame graph: wide bars = expensive renders; gray bars = did not re-render
3. Enable "Record why each component rendered" to see the cause (props change, state, parent)
4. Look for components re-rendering with identical props → candidates for `memo()` / stable callbacks

```typescript
// Programmatic measurement for a specific subtree
<Profiler id="ProductList" onRender={(id, phase, actualDuration) => {
  if (actualDuration > 16) console.warn(`${id} slow render: ${actualDuration}ms`)
}}>
  <ProductList />
</Profiler>
```

### Core Web Vitals
- **LCP** (< 2.5s): slow LCP usually means waterfall fetching or blocking bundles — apply the CRITICAL rules above
- **INP** (< 200ms): slow interactions point to expensive re-renders or heavy main-thread work
- **CLS** (< 0.1): reserve space for images/dynamic content (`next/image` handles this)
- Measure in the field with `useReportWebVitals` (next/web-vitals) or the `web-vitals` package; in the lab with Lighthouse

### Browser Flame Graphs
1. Chrome DevTools → Performance tab → Record the slow interaction
2. Wide blocks in the main-thread flame graph = long tasks (> 50ms); zoom in to find the function
3. Long yellow (scripting) blocks during load = too much JS — check bundle rules above
4. Use the Network panel waterfall to spot sequential request chains → fix with `Promise.all()` / parallel fetching

## Decision Quick Reference

| Situation | Action |
|-----------|--------|
| Multiple independent fetches | `Promise.all()` |
| Heavy component not needed at load | `next/dynamic` with `ssr: false` |
| Importing from shared index | Change to direct module import |
| Passing object to client component | Pass only needed fields |
| Computing from existing state | Derive with `useMemo`, not `useEffect` |
| Callback depends on state | Use functional `setState` |
| Child re-renders unnecessarily | Wrap with `memo()` |
| Analytics/logging | Load after hydration in `useEffect` |
