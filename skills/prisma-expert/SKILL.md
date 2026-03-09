---
name: prisma-expert
description: Advanced Prisma ORM patterns for schema design, migrations, query optimization, and relations. Trigger on complex schema changes (>10 models), migration strategies, query performance issues, relation patterns (many-to-many, polymorphic), multi-tenant data isolation, or Prisma-specific debugging.
metadata:
  author: osforge
  version: '1.0'
---

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

## Prisma + Supabase Integration
- Use `directUrl` for migrations, `url` (pooled) for queries
- RLS policies apply at DB level, Prisma bypasses via service role
- Always validate tenant context in Server Actions before Prisma calls
- Use `@db.Uuid` for Supabase auth user references

## References
- [postgres-optimization](../postgres-optimization/SKILL.md) — DB-level optimization
- [security-best-practices](../security-best-practices/SKILL.md) — RLS + auth patterns
