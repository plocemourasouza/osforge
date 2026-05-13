# Prisma Expert

**Trigger:** schema, migration, Prisma, ORM, database model, relation

---

## Multi-Tenant Schema Isolation

```prisma
model Tenant {
  id        String   @id @default(cuid())
  name      String
  users     User[]
  orders    Order[]
  createdAt DateTime @default(now())
}

model User {
  id       String @id @default(cuid())
  tenantId String
  tenant   Tenant @relation(fields: [tenantId], references: [id])
  email    String

  @@unique([tenantId, email]) // Unique per tenant
  @@index([tenantId])         // Always index tenant_id
}
```

---

## Relation Patterns

### Polymorphic Relations (Union Pattern)
```prisma
model Comment {
  id          String  @id @default(cuid())
  content     String
  // Union discriminator
  targetType  String  // "post" | "product" | "order"
  targetId    String

  @@index([targetType, targetId])
}
```

### Self-Referential
```prisma
model Category {
  id       String     @id @default(cuid())
  name     String
  parentId String?
  parent   Category?  @relation("CategoryTree", fields: [parentId], references: [id])
  children Category[] @relation("CategoryTree")
}
```

---

## Soft Delete Pattern

```prisma
model User {
  id        String    @id @default(cuid())
  email     String    @unique
  deletedAt DateTime?

  @@index([deletedAt])
}
```

```typescript
// Middleware for automatic filtering
prisma.$use(async (params, next) => {
  if (params.model === 'User' && params.action === 'findMany') {
    params.args.where = { ...params.args.where, deletedAt: null }
  }
  return next(params)
})
```

---

## Safe Production Migrations

### Rule: Additive-Only
- ADD columns with defaults or nullable
- NEVER drop columns directly
- NEVER rename columns directly

### Two-Phase Drop
```bash
# Phase 1: Mark as deprecated, stop using in code
# Phase 2: After deploy confirmed, drop in next migration
```

### Migration Checklist
1. Review generated SQL before applying
2. Test on staging with production data copy
3. Have rollback plan ready
4. Run during low-traffic window
5. Monitor after deployment

---

## N+1 Prevention

```typescript
// BAD: N+1
const users = await prisma.user.findMany()
for (const user of users) {
  const orders = await prisma.order.findMany({ where: { userId: user.id } })
}

// GOOD: Eager loading with select
const users = await prisma.user.findMany({
  select: {
    id: true,
    email: true,
    orders: {
      select: {
        id: true,
        total: true,
      },
    },
  },
})
```

---

## Cursor-Based Pagination

```typescript
async function getOrders(cursor?: string, take = 20) {
  return prisma.order.findMany({
    take: take + 1, // Fetch one extra to check hasMore
    cursor: cursor ? { id: cursor } : undefined,
    skip: cursor ? 1 : 0,
    orderBy: { createdAt: 'desc' },
    select: {
      id: true,
      total: true,
      createdAt: true,
    },
  })
}
```

---

## Interactive Transactions

```typescript
await prisma.$transaction(async (tx) => {
  const account = await tx.account.update({
    where: { id: accountId },
    data: { balance: { decrement: amount } },
  })

  if (account.balance < 0) {
    throw new Error('Insufficient funds')
  }

  await tx.transfer.create({
    data: { fromId: accountId, toId: targetId, amount },
  })
}, {
  isolationLevel: 'Serializable', // Strongest isolation
  timeout: 10000,
})
```

---

## Prisma + Supabase Integration

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")        // Pooled: port 6543
  directUrl = env("DIRECT_DATABASE_URL") // Direct: port 5432
}
```

```env
# .env
DATABASE_URL="postgresql://user:pass@db.xxx.supabase.co:6543/postgres?pgbouncer=true"
DIRECT_DATABASE_URL="postgresql://user:pass@db.xxx.supabase.co:5432/postgres"
```
