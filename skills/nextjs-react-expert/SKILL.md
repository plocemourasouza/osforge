---
name: nextjs-react-expert
description: 'React and Next.js performance optimization from Vercel Engineering. Use when building React components, optimizing performance, eliminating waterfalls, reducing bundle size, reviewing code for performance issues, or implementing server/client-side optimizations. Specific symptoms: TTI > 3s, First Load JS bundle > 200KB, LCP > 2.5s, slow page loads from sequential fetches, excessive re-renders, hydration errors.'
metadata:
  author: vercel (adapted)
  version: "2.0.0"
  source: "vercel-labs/agent-skills react-best-practices"
---

# Next.js & React Performance Expert

> **From Vercel Engineering** - 57 optimization rules prioritized by impact
> **Philosophy:** Eliminate waterfalls first, optimize bundles second, then micro-optimize.

---

## How to use

Rules are ordered by impact: waterfalls and bundle size first, then server, client fetching,
re-renders, rendering, JavaScript, advanced patterns. For a review, work top-down and stop where
the remaining rules cannot matter for this code. Apply a rule from its one-line summary below
when it is enough; open the matching reference file for the code example and the exceptions.
Measure before optimizing — a rule whose problem is not present is not a finding.

## Quick Reference

### 1. Eliminating Waterfalls (CRITICAL)

- `async-defer-await` - Move await into branches where actually used
- `async-parallel` - Use Promise.all() for independent operations
- `async-dependencies` - Use better-all for partial dependencies
- `async-api-routes` - Start promises early, await late in API routes
- `async-suspense-boundaries` - Use Suspense to stream content

### 2. Bundle Size Optimization (CRITICAL)

- `bundle-barrel-imports` - Import directly, avoid barrel files
- `bundle-dynamic-imports` - Use next/dynamic for heavy components
- `bundle-defer-third-party` - Load analytics/logging after hydration
- `bundle-conditional` - Load modules only when feature is activated
- `bundle-preload` - Preload on hover/focus for perceived speed

### 3. Server-Side Performance (HIGH)

- `server-auth-actions` - Authenticate server actions like API routes
- `server-cache-react` - Use React.cache() for per-request deduplication
- `server-cache-lru` - Use LRU cache for cross-request caching
- `server-dedup-props` - Avoid duplicate serialization in RSC props
- `server-serialization` - Minimize data passed to client components
- `server-parallel-fetching` - Restructure components to parallelize fetches
- `server-after-nonblocking` - Use after() for non-blocking operations

### 4. Client-Side Data Fetching (MEDIUM-HIGH)

- `client-swr-dedup` - Use SWR for automatic request deduplication
- `client-event-listeners` - Deduplicate global event listeners
- `client-passive-event-listeners` - Use passive listeners for scroll
- `client-localstorage-schema` - Version and minimize localStorage data

### 5. Re-render Optimization (MEDIUM)

- `rerender-defer-reads` - Don't subscribe to state only used in callbacks
- `rerender-memo` - Extract expensive work into memoized components
- `rerender-memo-with-default-value` - Hoist default non-primitive props
- `rerender-dependencies` - Use primitive dependencies in effects
- `rerender-derived-state` - Subscribe to derived booleans, not raw values
- `rerender-derived-state-no-effect` - Derive state during render, not effects
- `rerender-functional-setstate` - Use functional setState for stable callbacks
- `rerender-lazy-state-init` - Pass function to useState for expensive values
- `rerender-simple-expression-in-memo` - Avoid memo for simple primitives
- `rerender-move-effect-to-event` - Put interaction logic in event handlers
- `rerender-transitions` - Use startTransition for non-urgent updates
- `rerender-use-ref-transient-values` - Use refs for transient frequent values

### 6. Rendering Performance (MEDIUM)

- `rendering-animate-svg-wrapper` - Animate div wrapper, not SVG element
- `rendering-content-visibility` - Use content-visibility for long lists
- `rendering-hoist-jsx` - Extract static JSX outside components
- `rendering-svg-precision` - Reduce SVG coordinate precision
- `rendering-hydration-no-flicker` - Use inline script for client-only data
- `rendering-hydration-suppress-warning` - Suppress expected mismatches
- `rendering-activity` - Use Activity component for show/hide
- `rendering-conditional-render` - Use ternary, not && for conditionals
- `rendering-usetransition-loading` - Prefer useTransition for loading state

### 7. JavaScript Performance (LOW-MEDIUM)

- `js-batch-dom-css` - Group CSS changes via classes or cssText
- `js-index-maps` - Build Map for repeated lookups
- `js-cache-property-access` - Cache object properties in loops
- `js-cache-function-results` - Cache function results in module-level Map
- `js-cache-storage` - Cache localStorage/sessionStorage reads
- `js-combine-iterations` - Combine multiple filter/map into one loop
- `js-length-check-first` - Check array length before expensive comparison
- `js-early-exit` - Return early from functions
- `js-hoist-regexp` - Hoist RegExp creation outside loops
- `js-min-max-loop` - Use loop for min/max instead of sort
- `js-set-map-lookups` - Use Set/Map for O(1) lookups
- `js-tosorted-immutable` - Use toSorted() for immutability

### 8. Advanced Patterns (LOW)

- `advanced-event-handler-refs` - Store event handlers in refs
- `advanced-init-once` - Initialize app once per app load
- `advanced-use-latest` - useLatest for stable callback refs

## Reference files

| File                                    | Impact             | Rules    | When to Read                                                    |
| --------------------------------------- | ------------------ | -------- | --------------------------------------------------------------- |
| `references/1-async-eliminating-waterfalls.md`     | CRITICAL    | 5 rules  | Slow page loads, sequential API calls, data fetching waterfalls |
| `references/2-bundle-bundle-size-optimization.md`  | CRITICAL    | 5 rules  | Large bundle size, slow Time to Interactive, First Load issues  |
| `references/3-server-server-side-performance.md`   | HIGH        | 7 rules  | Slow SSR, API route optimization, server-side waterfalls        |
| `references/4-client-client-side-data-fetching.md` | MEDIUM-HIGH | 4 rules  | Client data management, SWR patterns, deduplication             |
| `references/5-rerender-re-render-optimization.md`  | MEDIUM      | 12 rules | Excessive re-renders, React performance, memoization            |
| `references/6-rendering-rendering-performance.md`  | MEDIUM      | 9 rules  | Rendering bottlenecks, virtualization, image optimization       |
| `references/7-js-javascript-performance.md`        | LOW-MEDIUM  | 12 rules | Micro-optimizations, caching, loop performance                  |
| `references/8-advanced-advanced-patterns.md`       | VARIABLE    | 3 rules  | Advanced React patterns, useLatest, init-once                   |
| `references/9-cache-components.md`                | CRITICAL    | 4 sections | Next.js 16+ only: `use cache`, `cacheLife`, PPR, `cacheTag` |

### Next.js 16+ cache components

`references/9-cache-components.md` covers `use cache`, `cacheLife`, `cacheTag` and PPR — read it
for any Next.js 16+ project before reaching for traditional revalidation.

**Source:** Vercel Engineering — `vercel-labs/agent-skills` `react-best-practices` (MIT); the
Quick Reference above is taken from it verbatim.

**Exhaustiveness bar** — a performance pass is done when every Quick Reference rule of the CRITICAL and HIGH categories carries a verdict (applies / does not apply / fixed, with file:line) for the touched code, and lower categories were checked wherever the code is on a hot path.
