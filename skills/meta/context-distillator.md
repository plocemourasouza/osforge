# Context Distillator

**Trigger:** "distill", "comprimir contexto", "compress", ou quando documento excede tamanho ideal para LLM.

---

## Purpose

Compressão lossless de documentos para consumo otimizado por LLMs. Preserva 100% da informação factual eliminando overhead textual.

**Não é sumarização (lossy) — é compressão lossless.**

---

## Target

40-60% do tamanho original mantendo 100% da informação.

---

## Compression Rules

### Remove Hedging
```markdown
// Before
"It might be worth considering that we could potentially implement..."

// After
"Implement..."
```

### Remove Filler
```markdown
// Before
"In order to achieve the desired outcome, we need to..."

// After
"To achieve this:"
```

### Condense Lists
```markdown
// Before
- First, we need to set up the database
- Second, we need to create the schema
- Third, we need to run migrations

// After
1. Setup database
2. Create schema
3. Run migrations
```

### Remove Repetition
```markdown
// Before
"The user authentication system handles user login. This login system
allows users to authenticate using their credentials."

// After
"Auth system handles login via credentials."
```

### Use Tables
```markdown
// Before
"For production, use PostgreSQL. For development, SQLite works fine.
For testing, use in-memory SQLite."

// After
| Env | Database |
|-----|----------|
| Prod | PostgreSQL |
| Dev | SQLite |
| Test | SQLite (memory) |
```

### Use Symbols
```markdown
// Before
"greater than or equal to"
"less than"
"approximately"

// After
"≥", "<", "~"
```

---

## Process

```
1. Read original document
2. Identify information units
3. Apply compression rules
4. Verify no information lost
5. Output compressed version
```

---

## Example

### Before (180 words)
```markdown
## Introduction

In this document, we will be discussing the implementation details
of our new authentication system. This authentication system is
designed to provide secure access to our application for all users.

The system will support multiple authentication methods, including
but not limited to email/password authentication, OAuth authentication
with Google and GitHub, and magic link authentication.

It is important to note that all authentication flows must be secure
and follow industry best practices. We will be using Supabase Auth
as our authentication provider because it offers all these features
out of the box and integrates well with our existing PostgreSQL database.
```

### After (45 words)
```markdown
## Auth System

Supports:
- Email/password
- OAuth (Google, GitHub)
- Magic links

Provider: Supabase Auth
- Built-in security
- PostgreSQL integration
```

**Compression: 75% reduction, 0% information loss**

---

## When to Use

- Document exceeds context window
- Loading multiple documents
- Optimizing for token cost
- Preparing knowledge bases
