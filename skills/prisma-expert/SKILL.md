---
name: prisma-expert
description: "Advanced Prisma ORM patterns. Use when: schema changes with >3 models, migration strategies, slow queries or N+1, many-to-many or polymorphic relations, multi-tenant isolation, Prisma debugging. Keywords: prisma, schema, migration, query, relation, database, orm, model, seed, index, RLS."
model: sonnet
allowed-tools: Read, Bash, Glob, Grep
hooks:
  PreToolUse:
    - matcher: Bash
      hooks:
        - type: prompt
          prompt: "If the command contains 'prisma migrate deploy' in an environment other than local dev, confirm with the user before executing."
metadata:
  author: osforge
  version: '1.1'
---

## Project context
!`[ -f prisma/schema.prisma ] && echo "Schema found: $(wc -l < prisma/schema.prisma) lines, $(grep -c '^model' prisma/schema.prisma) models" || echo "prisma/schema.prisma not found"`
!`[ -f .env ] && grep -c 'DATABASE_URL' .env > /dev/null 2>&1 && echo "DATABASE_URL configured" || echo "DATABASE_URL not found in .env"`

# Prisma Expert

## Schema Design Patterns

### Multi-Tenant Isolation
```prisma
model Organization {
  id        String   @id @default(cuid())
  slug      String   @unique
  members   Member[]
  // ALL tenant-scoped models reference org
}

model Project {
  id             String       @id @default(cuid())
  organizationId String
  organization   Organization @relation(fields: [organizationId], references: [id])
  // Always filter by organizationId in queries
  @@index([organizationId])
}
```

### Polymorphic Relations (Union Pattern)
```prisma
model Notification {
  id          String   @id @default(cuid())
  type        NotificationType
  // Use JSON for polymorphic payload
  payload     Json
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  @@index([userId, type])
}

enum NotificationType {
  COMMENT
  MENTION
  SYSTEM
}
```

### Soft Delete
```prisma
model Record {
  id        String    @id @default(cuid())
  deletedAt DateTime?
  // Middleware filters deletedAt globally
  @@index([deletedAt])
}
```

## Migration Strategies

### Safe Production Migrations
1. **Additive only** — add columns/tables, never remove in same deploy
2. **Two-phase drops** — mark deprecated → deploy without usage → drop in next release
3. **Default values** — always provide defaults for new required columns
4. **Index concurrently** — for large tables, use raw SQL with `CREATE INDEX CONCURRENTLY`

```bash
# Generate migration without applying
bunx prisma migrate dev --create-only --name add_tenant_field

# Review generated SQL before applying
cat prisma/migrations/*_add_tenant_field/migration.sql

# Apply after review
bunx prisma migrate dev
```

### Migration Checklist
- [ ] New columns have defaults or are optional
- [ ] No column renames (add new → migrate data → drop old)
- [ ] Indexes added for new foreign keys
- [ ] RLS policies updated if Supabase
- [ ] Seed data updated

## Query Optimization

### N+1 Prevention
```typescript
// ❌ N+1 problem
const users = await prisma.user.findMany()
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { authorId: user.id } })
}

// ✅ Eager loading
const users = await prisma.user.findMany({
  include: { posts: { where: { published: true }, take: 10 } }
})

// ✅ For complex cases, use raw query
const result = await prisma.$queryRaw`
  SELECT u.*, COUNT(p.id) as post_count
  FROM "User" u
  LEFT JOIN "Post" p ON p."authorId" = u.id
  GROUP BY u.id
  HAVING COUNT(p.id) > 5
`
```

### Pagination (Cursor-based)
```typescript
// ✅ Cursor pagination (performant for large datasets)
const posts = await prisma.post.findMany({
  take: 20,
  skip: 1, // Skip cursor itself
  cursor: { id: lastPostId },
  orderBy: { createdAt: 'desc' },
})

// ❌ Offset pagination (slow on large tables)
const posts = await prisma.post.findMany({
  skip: page * 20,
  take: 20,
})
```

### Transaction Patterns
```typescript
// Interactive transaction with timeout
const result = await prisma.$transaction(async (tx) => {
  const account = await tx.account.update({
    where: { id: fromId },
    data: { balance: { decrement: amount } },
  })
  if (account.balance < 0) throw new Error('INSUFFICIENT_FUNDS')
  
  await tx.account.update({
    where: { id: toId },
    data: { balance: { increment: amount } },
  })
  return account
}, { timeout: 5000, isolationLevel: 'Serializable' })
```

## Debugging with Prisma Logs

### Enable query logging
```typescript
// See all generated SQL queries (essential for detecting N+1)
const prisma = new PrismaClient({
  log: ['query', 'warn', 'error'],
})
```

### Profiling with event listeners
```typescript
// Capture the duration of each query to identify slow ones
const prisma = new PrismaClient({
  log: [{ emit: 'event', level: 'query' }],
})

prisma.$on('query', (e) => {
  if (e.duration > 100) {
    console.warn(`SLOW QUERY (${e.duration}ms): ${e.query}`, e.params)
  }
})
```

### Diagnostic tips
- **N+1**: if the log shows the same query repeated in a loop, an `include`/`select` with the relation is missing
- **`DEBUG="prisma:*"`**: environment variable for detailed internal logs (engine, connection pool)
- **EXPLAIN ANALYZE**: copy the query from the log and run `prisma.$queryRaw` with `EXPLAIN ANALYZE` to see the execution plan
- Disable `log: ['query']` in production — it adds overhead and can leak sensitive data in the params

## Prisma + Supabase Integration
- Use `directUrl` for migrations, `url` (pooled) for queries
- RLS policies apply at DB level, Prisma bypasses via service role
- Always validate tenant context in Server Actions before Prisma calls
- Use `@db.Uuid` for Supabase auth user references

## References
- [postgres-optimization](../postgres-optimization/SKILL.md) — DB-level optimization
- [security-best-practices](../security-best-practices/SKILL.md) — RLS + auth patterns

## Gotchas

- **`migrate dev` vs `migrate deploy`**: `migrate dev` generates a migration + applies it. `migrate deploy` only applies (for CI/prod). Never run `migrate dev` in production — it can reset data.
- **Renaming a column causes DROP + ADD**: Prisma does not detect renames — it generates `DROP COLUMN` + `ADD COLUMN`, wiping the data. To rename: (1) add a new column, (2) migrate data via a script, (3) drop the old one in a separate release.
- **`include` vs `select` in the same query**: do not mix `include` and `select` at the same level — Prisma does not allow it. Choose one: `select` for granular control, `include` for complete relations.
- **RLS does not apply via service role**: when using Supabase with `service_role`, Prisma bypasses RLS completely. Always validate `organizationId` at the Server Action level before any Prisma query.
- **Offset pagination on large tables**: `skip: page * 20` becomes progressively slower as the table grows. For tables with >10K records, always use cursor-based pagination with `cursor: { id: lastId }`.
- **`$queryRaw` requires a template literal**: `prisma.$queryRaw(sql)` is vulnerable to SQL injection. Always use a tagged template literal: `` prisma.$queryRaw`SELECT * FROM "User" WHERE id = ${id}` ``.
- **Migrations without `--create-only` in prod**: always generate the migration with `--create-only`, review the generated SQL, and only then apply it. Never let Prisma apply a migration automatically in production.
