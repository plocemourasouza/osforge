---
name: context7-docs-first
description: "Ground all platform and library answers in current official documentation by using Context7 MCP tools before responding. TRIGGER when: user asks about Next.js, Supabase, Prisma, Stripe, Playwright, Bun, shadcn/ui, Vercel, or any version-sensitive library behavior. Also trigger when user says 'docs', 'latest', 'current version', 'how does X work now', or is integrating APIs that change between versions. Do NOT trigger for general programming concepts, algorithms, or topics unrelated to specific libraries."
metadata:
  author: osforge
  version: '1.0'
  requires: Context7 MCP server configured
---

# Context7 Docs-First

## Principle
Never rely on training data for library-specific behavior. Always consult current docs first, then respond. This eliminates hallucinated APIs, deprecated patterns, and version mismatches.

## Workflow

### Step 1: Identify the library
Determine the primary platform/library from the user's question or code context.

### Step 2: Resolve library ID
```
Call: mcp__context7__resolve-library-id
  libraryName: "supabase" (or "next.js", "prisma", "stripe", etc.)
```

### Step 3: Query docs with the user's question
```
Call: mcp__context7__query-docs
  libraryId: (from step 2, e.g., "/supabase/supabase")
  query: (the user's actual question or task)
  tokens: 5000
```

### Step 4: Respond using docs as source of truth
Provide implementation steps or code examples drawn from the docs. If docs are ambiguous or lack coverage, report the gap and ask for clarification.

## Library ID Quick Reference (OSForge Stack)

| Library | Context7 ID | When to use |
|---|---|---|
| Next.js | `/vercel/next.js` | App Router, middleware, Server Components, Server Actions |
| Supabase | `/supabase/supabase` | Auth, RLS, Realtime, Edge Functions, storage |
| Prisma | `/prisma/prisma` | Schema, migrations, Client API, relations |
| Stripe | `/stripe/stripe-node` | Checkout, webhooks, subscriptions, billing portal |
| Playwright | `/microsoft/playwright` | E2E testing, selectors, fixtures, config |
| shadcn/ui | `/shadcn-ui/ui` | Components, theming, installation |
| Tailwind CSS | `/tailwindlabs/tailwindcss` | Utilities, config, plugins |
| Bun | `/oven-sh/bun` | Runtime APIs, test runner, bundler |
| Zod | `/colinhacks/zod` | Schema validation, transforms, refinements |
| React Hook Form | `/react-hook-form/react-hook-form` | Form validation, integration with Zod |
| Vercel | `/vercel/vercel` | Deployment, env vars, edge config |
| TypeScript | `/microsoft/typescript` | Compiler options, type utilities |

## Rules

1. **Max 3 Context7 calls per question** — resolve + query is usually enough. Add a second query only if the first didn't cover the topic.
2. **Prefer official sources** — When Context7 returns multiple matches, pick the official docs over community content.
3. **Single primary platform** — When multiple libs are involved (e.g., "Supabase auth in Next.js"), pick the primary one and query that. Don't query both unless the answer requires it.
4. **Report gaps honestly** — If docs don't cover the question, say so. Don't fill gaps with training data without flagging it.
5. **Version awareness** — If user mentions a specific version, include it in the query. Context7 handles version matching automatically.
6. **Skip for general concepts** — Don't invoke Context7 for questions about algorithms, design patterns, or language fundamentals that don't depend on library versions.

## Integration with Other Skills

- **Skill 16 (Prisma Expert):** Before applying Prisma patterns, verify current API with Context7
- **Skill 17 (Next.js Supabase Auth):** Verify `@supabase/ssr` API hasn't changed
- **Skill 19 (Stripe Integration):** Verify webhook event types and checkout session API
- **Skill 27 (Claude API TypeScript):** Verify SDK methods and model IDs

## MCP Configuration Required

```jsonc
// .mcp.json or claude mcp add
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}

// Or with API key for higher rate limits:
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_CONTEXT7_API_KEY"]
    }
  }
}
```

## Auto-Invoke Rule (optional)
Add to CLAUDE.md or system prompt to auto-trigger:
```
Always use context7 when I need code generation, setup or configuration steps, 
or library/API documentation for Next.js, Supabase, Prisma, Stripe, Playwright, 
shadcn/ui, Bun, or Vercel. Automatically resolve library IDs and query docs 
without me explicitly asking.
```
