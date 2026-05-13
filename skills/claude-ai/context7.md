# Context7 Docs-First

**Trigger:** Questions about Next.js, Supabase, Prisma, Stripe, Playwright, Bun, shadcn/ui, Vercel, or any version-sensitive library. Also trigger on "docs", "latest", "current version", or API integration tasks.

---

## Workflow

```
1. resolve-library-id → Get Context7 library ID
2. query-docs → Fetch relevant documentation
3. respond → Answer from source of truth
```

---

## Quick Reference Table

| Library | Context7 ID |
|---------|-------------|
| Next.js | `/vercel/next.js` |
| Supabase | `/supabase/supabase` |
| Prisma | `/prisma/prisma` |
| Stripe | `/stripe/stripe-node` |
| Playwright | `/microsoft/playwright` |
| shadcn/ui | `/shadcn-ui/ui` |
| Bun | `/oven-sh/bun` |
| Zod | `/colinhacks/zod` |
| React | `/facebook/react` |
| TypeScript | `/microsoft/TypeScript` |

---

## MCP Tools

```typescript
// Resolve library ID
await mcp.context7.resolveLibraryId({
  libraryName: "next.js"
})

// Query documentation
await mcp.context7.getLibraryDocs({
  context7CompatibleLibraryId: "/vercel/next.js",
  topic: "server actions",
  tokens: 5000
})
```

---

## Rules

1. **Max 3 calls per question** — avoid excessive API usage
2. **Prefer official sources** — Context7 pulls from official docs
3. **Report gaps honestly** — if docs don't cover the topic, say so
4. **Requires Context7 MCP server** — must be configured

---

## Configuration

```json
// ~/.claude/settings.json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    }
  }
}
```

---

## Usage Patterns

### Version-Specific Answers
```
User: "How do Server Actions work in Next.js 15?"
→ Query Context7 for /vercel/next.js with topic "server actions"
→ Respond with current documented behavior
```

### API Integration
```
User: "How do I set up Stripe webhooks?"
→ Query Context7 for /stripe/stripe-node with topic "webhooks"
→ Include signature verification from docs
```

### Breaking Changes
```
User: "What changed in Prisma 5?"
→ Query Context7 for /prisma/prisma with topic "migration guide"
→ List breaking changes from official changelog
```
