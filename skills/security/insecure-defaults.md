# Insecure Defaults Detection

**Trigger:** security hardening, env audit, config review, pre-deployment security

---

## Purpose

Detect fail-open patterns and insecure default configurations. Based on Trail of Bits methodology.

---

## Fail-Open Patterns

### Environment Variable Defaults

```typescript
// BAD: Fail-open
const SECRET = process.env.SECRET || 'default-secret'
const ALLOWED_ORIGINS = process.env.CORS_ORIGINS || '*'
const DEBUG = process.env.DEBUG || true

// GOOD: Fail-secure
const SECRET = process.env.SECRET  // Crashes if missing
if (!SECRET) throw new Error('SECRET is required')

const ALLOWED_ORIGINS = process.env.CORS_ORIGINS
if (!ALLOWED_ORIGINS) throw new Error('CORS_ORIGINS is required')
```

### Search Patterns
```bash
# Find permissive defaults
grep -rn "|| '\*'" src/
grep -rn "|| true" src/
grep -rn "?? '\*'" src/
grep -rn "|| 'development'" src/
```

---

## Common Insecure Defaults

### CORS
```typescript
// BAD
app.use(cors())  // Allows all origins

// GOOD
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(','),
  credentials: true,
}))
```

### Rate Limiting
```typescript
// BAD: No rate limiting
export async function POST(request: Request) {
  // Handles request without limits
}

// GOOD: Rate limited
import { rateLimit } from '@/lib/rate-limit'

export async function POST(request: Request) {
  const identifier = getIP(request)
  const { success } = await rateLimit.check(identifier)
  if (!success) {
    return new Response('Too Many Requests', { status: 429 })
  }
  // Handle request
}
```

### RLS Missing
```sql
-- BAD: Table without RLS
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  total DECIMAL
);

-- GOOD: RLS enabled
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  total DECIMAL
);
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users see own orders" ON orders
  FOR SELECT USING (auth.uid() = user_id);
```

### Server Actions Without Auth
```typescript
// BAD: No auth check
export async function deleteUser(userId: string) {
  await prisma.user.delete({ where: { id: userId } })
}

// GOOD: Auth first
export async function deleteUser(userId: string) {
  const session = await auth()
  if (!session?.user) throw new Error('Unauthorized')
  if (session.user.id !== userId && session.user.role !== 'admin') {
    throw new Error('Forbidden')
  }
  await prisma.user.delete({ where: { id: userId } })
}
```

---

## Security Headers Check

```typescript
// next.config.js
const securityHeaders = [
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
]
```

Missing any of these? Flag it.

---

## Scan Checklist

### Environment
- [ ] No secrets with defaults
- [ ] All required env vars validated at startup
- [ ] Different configs for dev/staging/prod

### Authentication
- [ ] Auth check at entry of every Server Action
- [ ] Auth check at entry of every Route Handler
- [ ] Session validation uses `getUser()` not `getSession()`

### Authorization
- [ ] Resource ownership verified (not just auth)
- [ ] Role checks where applicable
- [ ] RLS enabled on multi-tenant tables

### Input Validation
- [ ] Zod schema on all external input
- [ ] File upload validation (type, size)
- [ ] URL validation for redirects

### Error Handling
- [ ] Generic errors to client
- [ ] Detailed errors to server logs
- [ ] No stack traces exposed

### Headers
- [ ] Security headers configured
- [ ] CORS restricted to known origins
- [ ] CSRF protection on Route Handlers

---

## Audit Report Format

```markdown
## Security Audit: Insecure Defaults

**Date:** YYYY-MM-DD
**Scope:** [files/modules audited]

### Critical Issues

#### 1. Permissive CORS Default
- **File:** `middleware.ts:12`
- **Issue:** CORS allows all origins
- **Risk:** Cross-site request attacks
- **Fix:** Restrict to known origins

### High Issues
[...]

### Medium Issues
[...]

### Passed Checks
- [x] Auth on Server Actions
- [x] RLS enabled
- [x] Security headers configured
```
