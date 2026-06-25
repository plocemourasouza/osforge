---
name: database-design
description: "Database design principles: database and ORM choice, schema, indexes, optimization, and migrations. Use when: a slow query or N+1 in production, choosing between PostgreSQL, Neon, Turso, and SQLite, choosing between Drizzle, Prisma, and Kysely, modeling the schema and relationships of a new feature, creating a composite index or interpreting EXPLAIN ANALYZE, planning a safe migration on a serverless database. Keywords: database, schema, index, ORM, Prisma, Drizzle, migration, N+1, PostgreSQL. Do NOT use for: trivial read queries, operational backup/restore, or database server administration."
metadata:
  author: antigravity-kit (adapted)
  version: "1.0.0"
  source: "antigravity-kit"
---

# Database Design

> **Learn to THINK, not copy SQL patterns.**

## 🎯 Selective Reading Rule

**Read ONLY files relevant to the request!** Check the content map, find what you need.

| File | Description | When to Read |
|------|-------------|--------------|
| `database-selection.md` | PostgreSQL vs Neon vs Turso vs SQLite | Choosing database |
| `orm-selection.md` | Drizzle vs Prisma vs Kysely | Choosing ORM |
| `schema-design.md` | Normalization, PKs, relationships | Designing schema |
| `indexing.md` | Index types, composite indexes | Performance tuning |
| `optimization.md` | N+1, EXPLAIN ANALYZE | Query optimization |
| `migrations.md` | Safe migrations, serverless DBs | Schema changes |

---

## ⚠️ Core Principle

- ASK user for database preferences when unclear
- Choose database/ORM based on CONTEXT
- Don't default to PostgreSQL for everything

---

## Decision Checklist

Before designing schema:

- [ ] Asked user about database preference?
- [ ] Chosen database for THIS context?
- [ ] Considered deployment environment?
- [ ] Planned index strategy?
- [ ] Defined relationship types?

---

## Anti-Patterns

❌ Default to PostgreSQL for simple apps (SQLite may suffice)
❌ Skip indexing
❌ Use SELECT * in production
❌ Store JSON when structured data is better
❌ Ignore N+1 queries

---

## See Also

- `references/database-selection.md` - Database comparison and selection
- `references/orm-selection.md` - ORM comparison and selection
- `references/schema-design.md` - Normalization and schema principles
- `references/indexing.md` - Indexing strategies
- `references/optimization.md` - Query optimization and N+1 problems
- `references/migrations.md` - Safe schema migrations
