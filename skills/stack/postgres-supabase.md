# PostgreSQL & Supabase Optimization

**Trigger:** query, RLS, index, Supabase, PostgreSQL, slow query, N+1

---

## Core Rules
- `EXPLAIN ANALYZE` before approving complex queries
- `select` only needed fields (never `findMany()` without select)
- Avoid N+1 (use `include` with `select`)

## Indexing
- Multi-tenant: tenant_id first in composite indexes
- Partial indexes for active-only filters
- Always index foreign keys
- Use covering indexes for frequently accessed columns

```sql
-- Good: tenant_id first for multi-tenant
CREATE INDEX idx_orders_tenant_status ON orders(tenant_id, status);

-- Partial index for active records
CREATE INDEX idx_users_active ON users(email) WHERE deleted_at IS NULL;
```

## RLS (Row Level Security)
- All multi-tenant tables need RLS enabled
- Separate policies per operation (SELECT, INSERT, UPDATE, DELETE)
- Use `auth.jwt()` / `auth.uid()` — never trust client params

```sql
-- Enable RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Policy per operation
CREATE POLICY "Users can view own orders"
  ON orders FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own orders"
  ON orders FOR INSERT
  WITH CHECK (auth.uid() = user_id);
```

## Connections
- App: port 6543 (pooled via PgBouncer)
- Migrations: port 5432 (direct)

```typescript
// prisma/schema.prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")        // pooled: 6543
  directUrl = env("DIRECT_DATABASE_URL") // direct: 5432
}
```

## Raw SQL When
Use raw SQL for:
- Aggregations with complex GROUP BY
- JSON/JSONB operations
- Full-text search
- Pivot tables
- Window functions
- Recursive CTEs

Always use `$queryRaw` (never `$queryRawUnsafe`).

```typescript
// Safe parameterized query
const result = await prisma.$queryRaw`
  SELECT date_trunc('day', created_at) as day, COUNT(*)
  FROM orders
  WHERE tenant_id = ${tenantId}
  GROUP BY 1
  ORDER BY 1
`;
```

## Query Optimization Checklist
1. Check for missing indexes with `EXPLAIN ANALYZE`
2. Look for sequential scans on large tables
3. Verify join order is optimal
4. Check for unnecessary columns in SELECT
5. Ensure WHERE clauses use indexed columns
6. Avoid functions on indexed columns in WHERE
7. Use LIMIT for paginated queries
8. Consider materialized views for complex aggregations

## Supabase-Specific
- Use Supabase client for auth-aware queries
- Realtime subscriptions for live data
- Edge Functions for serverless logic
- Storage for file uploads with RLS
