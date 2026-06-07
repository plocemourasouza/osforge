---
name: database-design
description: "Princípios de design de banco de dados: escolha de banco e ORM, schema, índices, otimização e migrations. ACIONE quando: query lenta ou N+1 em produção, escolher entre PostgreSQL, Neon, Turso e SQLite, escolher entre Drizzle, Prisma e Kysely, modelar schema e relacionamentos de nova feature, criar índice composto ou interpretar EXPLAIN ANALYZE, planejar migration segura em banco serverless. Keywords: database, banco de dados, schema, index, ORM, Prisma, Drizzle, migration, N+1, PostgreSQL. Não acione para: queries triviais de leitura, backup/restore operacional ou administração de servidor de banco."
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
