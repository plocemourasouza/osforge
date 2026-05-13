# Database Design

**Trigger:** Database design, schema design, database selection, ORM choice, indexing strategy, migrations.

---

## Database Selection

| Database | Best For | Considerations |
|----------|----------|----------------|
| **PostgreSQL** | General purpose, complex queries | Gold standard, Supabase default |
| **Neon** | Serverless PostgreSQL | Auto-scaling, branching |
| **Turso** | Edge SQLite | Low latency, embedded |
| **SQLite** | Local/embedded | Simple, no server |
| **MongoDB** | Document store | Flexible schema |

**Recommendation:** PostgreSQL via Supabase for OSForge stack.

---

## Schema Design Principles

### Normalization
```sql
-- BAD: Denormalized
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_name TEXT,
  customer_email TEXT,
  product_name TEXT,
  product_price DECIMAL
);

-- GOOD: Normalized
CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL
);

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  price DECIMAL NOT NULL
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customers(id),
  product_id INT REFERENCES products(id),
  quantity INT NOT NULL
);
```

### Multi-tenant Isolation
```prisma
model Organization {
  id    String @id @default(cuid())
  name  String
  users User[]
}

model User {
  id             String       @id @default(cuid())
  organizationId String
  organization   Organization @relation(fields: [organizationId], references: [id])

  @@index([organizationId])
}
```

---

## Indexing Strategy

### When to Index
- Columns in WHERE clauses
- Columns in JOIN conditions
- Columns in ORDER BY
- Foreign keys (always)

### Composite Indexes
```sql
-- Multi-tenant: tenant_id FIRST
CREATE INDEX idx_orders_tenant_created
ON orders (tenant_id, created_at DESC);

-- Query order matters
-- This index helps: WHERE tenant_id = ? AND created_at > ?
-- This index doesn't help: WHERE created_at > ?
```

### Partial Indexes
```sql
-- Only index active records
CREATE INDEX idx_users_active_email
ON users (email)
WHERE status = 'active';
```

---

## ORM Selection

| ORM | Language | Features |
|-----|----------|----------|
| **Prisma** | TypeScript | Type-safe, migrations, studio |
| **Drizzle** | TypeScript | SQL-like, lightweight |
| **Kysely** | TypeScript | Type-safe query builder |
| **SQLAlchemy** | Python | Full-featured, async |

**Recommendation:** Prisma for OSForge stack.

---

## Safe Migrations

### Additive Only (Production)
```prisma
// SAFE: Add new column with default
model User {
  id    String @id
  name  String
  email String  // NEW - has default or nullable
}

// UNSAFE: Rename column (breaks existing code)
// UNSAFE: Change type (data loss)
// UNSAFE: Remove column (breaks queries)
```

### Two-Phase Drops
```
Phase 1: Stop using column in code
Phase 2: Deploy code without column usage
Phase 3: Drop column in migration
```

---

## Query Optimization

### EXPLAIN ANALYZE
```sql
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 123
ORDER BY created_at DESC
LIMIT 10;
```

### N+1 Prevention
```typescript
// BAD: N+1
const users = await prisma.user.findMany()
for (const user of users) {
  const orders = await prisma.order.findMany({
    where: { userId: user.id }
  })
}

// GOOD: Single query
const users = await prisma.user.findMany({
  include: { orders: true }
})
```
