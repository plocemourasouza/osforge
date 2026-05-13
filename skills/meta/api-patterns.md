# API Patterns

**Trigger:** REST, GraphQL, tRPC, API design, endpoint design, rate limiting, API versioning.

---

## Selection Matrix

| Factor | REST | GraphQL | tRPC |
|--------|------|---------|------|
| **Team familiarity** | Universal | Learning curve | TypeScript required |
| **Client diversity** | Any client | Any client | TypeScript only |
| **Data flexibility** | Fixed shapes | Client chooses | Fixed shapes |
| **Caching** | HTTP caching | Complex | HTTP caching |
| **File uploads** | Native | Tricky | Native |
| **Real-time** | WebSocket | Subscriptions | WebSocket |

---

## REST Best Practices

### Resource Naming
```
GET    /users              # List users
GET    /users/:id          # Get user
POST   /users              # Create user
PATCH  /users/:id          # Update user
DELETE /users/:id          # Delete user

# Nested resources
GET    /users/:id/orders   # User's orders
POST   /users/:id/orders   # Create order for user
```

### Response Format
```typescript
// Success
{
  "data": { ... },
  "meta": {
    "page": 1,
    "perPage": 20,
    "total": 100
  }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      { "field": "email", "message": "Must be valid email" }
    ]
  }
}
```

---

## Versioning Strategies

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| **URL path** | `/v1/users` | Clear, cacheable | URL clutter |
| **Header** | `Accept-Version: 1` | Clean URLs | Hidden |
| **Query** | `?version=1` | Easy to test | Pollutes params |

**Recommendation:** URL path for public APIs, header for internal.

---

## Pagination

### Cursor-based (recommended)
```typescript
GET /users?cursor=abc123&limit=20

{
  "data": [...],
  "meta": {
    "nextCursor": "def456",
    "hasMore": true
  }
}
```

### Offset-based (simple but problematic)
```typescript
GET /users?page=2&perPage=20

// Problem: inconsistent results if data changes
```

---

## Rate Limiting

```typescript
// Headers to return
{
  "X-RateLimit-Limit": "100",
  "X-RateLimit-Remaining": "95",
  "X-RateLimit-Reset": "1640000000"
}

// When exceeded
HTTP 429 Too Many Requests
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Try again in 60 seconds",
    "retryAfter": 60
  }
}
```

---

## Authentication

### Bearer Token (JWT)
```typescript
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### API Key
```typescript
X-API-Key: sk_live_abc123
```

### Never in Query String
```typescript
// BAD - logged in server logs
GET /users?api_key=sk_live_abc123

// GOOD - in header
GET /users
X-API-Key: sk_live_abc123
```

---

## Next.js API Routes

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
})

export async function POST(request: NextRequest) {
  const body = await request.json()
  const result = createUserSchema.safeParse(body)

  if (!result.success) {
    return NextResponse.json(
      { error: { code: 'VALIDATION_ERROR', details: result.error.issues } },
      { status: 400 }
    )
  }

  const user = await prisma.user.create({ data: result.data })
  return NextResponse.json({ data: user }, { status: 201 })
}
```
