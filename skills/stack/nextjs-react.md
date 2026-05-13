# Next.js + React Performance

**Trigger:** React, Next.js, performance, waterfalls, bundle, SSR, SSG, Server Components

---

## CRITICAL — Waterfalls
- `Promise.all()` for independent fetches
- Move `await` into branches where actually used
- Suspense boundaries for progressive streaming

## CRITICAL — Bundle
- Direct imports (never barrel files)
- `next/dynamic` for heavy components with `ssr: false`
- Analytics/logging after hydration in `useEffect`

## HIGH — Server-Side
- Auth in all Server Actions
- `React.cache()` for per-request deduplication
- Minimize data serialized to client components

## MEDIUM — Re-renders
- Derive state with `useMemo`, not `useEffect` + `useState`
- Functional `setState` for stable callbacks
- `memo()` for expensive children

---

## 57 Optimization Rules (Vercel Engineering)

### Data Fetching
1. Fetch data in Server Components, not Client Components
2. Use `Promise.all()` for parallel independent fetches
3. Implement Suspense boundaries for streaming
4. Use `React.cache()` for request deduplication
5. Avoid fetching in `useEffect` — prefer Server Components or Route Handlers

### Bundle Optimization
6. Import only what you need: `import { Button } from '@/components/ui/button'`
7. Never use barrel files (`index.ts` re-exports)
8. Use `next/dynamic` for code splitting heavy components
9. Set `ssr: false` for client-only heavy libraries (charts, maps)
10. Lazy load below-fold content

### Server Components
11. Default to Server Components
12. Use `"use client"` only when needed (hooks, browser APIs, events)
13. Keep Client Components as leaf nodes
14. Never wrap Server Components inside Client Components
15. Pass Server Component as children to Client Components when needed

### Images
16. Always use `next/image`
17. Set `priority` for above-fold images
18. Use `sizes` prop for responsive images
19. Prefer WebP/AVIF formats
20. Set explicit `width` and `height` to prevent CLS

### Fonts
21. Use `next/font` for zero FOUT
22. Subset fonts to used characters
23. Preload critical fonts
24. Use `font-display: swap` fallback

### JavaScript Reduction
25. Minimize client-side JavaScript
26. Defer non-critical scripts
27. Remove unused dependencies
28. Use tree-shakeable libraries
29. Analyze bundle with `@next/bundle-analyzer`

### Caching
30. Implement proper cache headers
31. Use `revalidate` for ISR
32. Leverage edge caching
33. Use `unstable_cache` for data caching
34. Implement stale-while-revalidate patterns

### Core Web Vitals
35. LCP: Optimize largest contentful paint element
36. INP: Keep interactions under 200ms
37. CLS: Reserve space for dynamic content
38. Use `loading="lazy"` for below-fold images
39. Preconnect to required origins

### State Management
40. Lift state only when necessary
41. Use URL state for shareable state
42. Prefer Server Actions for mutations
43. Avoid client-side state for server data
44. Use optimistic updates for better UX

### Rendering Strategies
45. Use SSG for static content
46. Use ISR for semi-dynamic content
47. Use SSR for personalized content
48. Use CSR only for highly interactive widgets
49. Implement partial prerendering when available

### API Routes
50. Use Route Handlers for API endpoints
51. Implement proper error handling
52. Return minimal response payloads
53. Use streaming for large responses
54. Implement rate limiting

### Build Optimization
55. Enable strict mode in production
56. Use production builds for testing
57. Monitor bundle size in CI
