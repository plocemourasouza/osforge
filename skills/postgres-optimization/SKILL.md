---
name: postgres-optimization
description: PostgreSQL and Supabase optimization best practices for queries, indexes, RLS policies, and connection management. Use when writing complex queries, creating migrations, optimizing slow queries, configuring RLS, managing indexes, or troubleshooting database performance. Triggers on Prisma raw queries, Supabase setup, slow page loads caused by database, N+1 query patterns, and migration creation.
---

# PostgreSQL & Supabase Optimization

## Quando NÃO usar esta skill

Delegue a um especialista de banco de dados (DBA / database-design) em vez de usar esta skill quando:
- O problema é de **modelagem/arquitetura de dados** (normalização, particionamento, sharding) — não de otimização de queries existentes
- Envolve **tuning de infraestrutura** (postgresql.conf, vacuum/autovacuum, réplicas, failover)
- Requer **migração de dados em larga escala** ou mudança de engine/provider
- A causa raiz é de aplicação (caching, arquitetura de API), não do banco

## Query Performance

### Always Use EXPLAIN ANALYZE
Before approving any complex query:
```sql
EXPLAIN ANALYZE
SELECT ... FROM ... WHERE ... ORDER BY ...;
```
Look for: Seq Scan on large tables (needs index), Nested Loop with high row counts (N+1), Sort with high cost (needs index on ORDER BY column).

### Select Only What You Need
```typescript
// ❌ Fetches all columns
const users = await prisma.user.findMany()

// ✅ Only needed fields
const users = await prisma.user.findMany({
  select: { id: true, name: true, email: true }
})
```

### Avoid N+1 Queries
```typescript
// ❌ N+1: one query per user for orders
const users = await prisma.user.findMany()
for (const user of users) {
  user.orders = await prisma.order.findMany({ where: { userId: user.id } })
}

// ✅ Single query with relation
const users = await prisma.user.findMany({
  include: { orders: { select: { id: true, total: true } } }
})
```

## Indexing Strategy

### Multi-Tenant Index Pattern
For tables filtered by organization, always put tenant_id first:
```sql
-- ✅ Composite index with tenant first
CREATE INDEX idx_orders_org_created
ON orders (organization_id, created_at DESC);

-- Covers: WHERE organization_id = ? ORDER BY created_at DESC
```

### Partial Indexes
When queries consistently filter a subset:
```sql
-- Only index active records (smaller, faster)
CREATE INDEX idx_users_active_email
ON users (email) WHERE deleted_at IS NULL;
```

### Common Index Patterns
```sql
-- Foreign keys (always index)
CREATE INDEX idx_orders_user_id ON orders (user_id);

-- Frequently filtered + sorted
CREATE INDEX idx_orders_status_date ON orders (status, created_at DESC);

-- Full-text search
CREATE INDEX idx_docs_search ON documents USING GIN (search_vector);

-- JSON field queries
CREATE INDEX idx_settings_theme ON users USING GIN (preferences);
```

## RLS Policies (Supabase)

### Every Multi-Tenant Table Needs RLS
```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Users see only their organization's data
CREATE POLICY "org_isolation" ON orders
  FOR ALL
  USING (organization_id = (auth.jwt() ->> 'org_id')::uuid);

-- Granular: separate read/write
CREATE POLICY "org_read" ON orders
  FOR SELECT USING (organization_id = current_org_id());

CREATE POLICY "org_insert" ON orders
  FOR INSERT WITH CHECK (organization_id = current_org_id());
```

### RLS Verification Checklist
- [ ] All tables with user data have RLS enabled
- [ ] Policies exist for SELECT, INSERT, UPDATE, DELETE separately
- [ ] Policies use `auth.jwt()` or `auth.uid()` — never trust client params
- [ ] Test with different roles (anon, authenticated, service_role)

## Connection Management

### Supabase Connection Pooling
```
# Application (pooled via PgBouncer)
DATABASE_URL="postgresql://...@db.xxx.supabase.co:6543/postgres?pgbouncer=true"

# Migrations (direct connection)
DIRECT_URL="postgresql://...@db.xxx.supabase.co:5432/postgres"
```

```prisma
// schema.prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")
}
```

### Prisma Singleton (Dev)
```typescript
const globalForPrisma = globalThis as unknown as { prisma: PrismaClient | undefined }
export const prisma = globalForPrisma.prisma ?? new PrismaClient()
if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

## Transactions
```typescript
// Atomic multi-write operations
await prisma.$transaction(async (tx) => {
  const order = await tx.order.create({ data: orderData })
  await tx.orderItem.createMany({ data: items.map(i => ({ ...i, orderId: order.id })) })
  await tx.inventory.updateMany({ ... })
  return order
})
```

## When to Use Raw SQL

Use Prisma for standard CRUD. Use raw SQL for:
- Aggregations with multiple GROUP BY
- JSON/JSONB operations
- Full-text search with `ts_rank`
- Pivot tables / cross-tabulation
- Complex window functions
- Recursive CTEs

Always use `$queryRaw` with template literals (never `$queryRawUnsafe`).
