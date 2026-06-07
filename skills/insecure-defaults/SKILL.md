---
name: insecure-defaults
description: Detect fail-open patterns and insecure default configurations. Trigger on security hardening, env variable audit, default config review, permission checks, CORS configuration, or pre-deployment security scan.
metadata:
  author: osforge
  version: '1.0'
  source: Trail of Bits methodology
---

# Insecure Defaults Detection

## What Are Insecure Defaults?
Configurations that allow applications to run in an insecure state when not explicitly configured. The app "works" but is vulnerable.

## Checklist by Category

### Environment Variables
```typescript
// ❌ INSECURE: Falls back to permissive value
const SECRET = process.env.JWT_SECRET || 'development-secret'
const ALLOWED_ORIGINS = process.env.CORS_ORIGINS || '*'
const DEBUG = process.env.DEBUG ?? true

// ✅ SECURE: Fail-closed — crash if not configured
const SECRET = process.env.JWT_SECRET
if (!SECRET) throw new Error('JWT_SECRET is required')

const ALLOWED_ORIGINS = process.env.CORS_ORIGINS
if (!ALLOWED_ORIGINS) throw new Error('CORS_ORIGINS is required')

const DEBUG = process.env.DEBUG === 'true' // false by default
```

### CORS Configuration
```typescript
// ❌ INSECURE defaults
app.use(cors()) // Allows ALL origins
app.use(cors({ origin: true })) // Reflects any origin
app.use(cors({ credentials: true, origin: '*' })) // Worst combo

// ✅ SECURE: Explicit allowlist
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') ?? [],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
}))
```

### Authentication Defaults
```typescript
// ❌ INSECURE patterns
const isAdmin = user?.role === 'admin' // undefined users pass
if (token) { grantAccess() } // Missing validation
session.maxAge = undefined // Never expires

// ✅ SECURE: Deny by default
const isAdmin = user?.role === 'admin' && user.verified === true
if (token && await verifyToken(token)) { grantAccess() }
session.maxAge = 3600 // 1 hour, explicit
```

### API Rate Limiting
```typescript
// ❌ INSECURE: No rate limiting (default)
app.post('/api/login', loginHandler)

// ✅ SECURE: Rate limit by default
import rateLimit from 'express-rate-limit'
app.post('/api/login', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: 'Too many attempts',
}), loginHandler)
```

### Database / Supabase
```sql
-- ❌ INSECURE: RLS disabled (Supabase default for new tables)
-- Tables are publicly readable/writable via PostgREST

-- ✅ SECURE: Always enable RLS
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
-- Then add explicit policies
```

### Next.js Specific
```typescript
// ❌ INSECURE: Server Action without auth check
'use server'
export async function deleteProject(id: string) {
  await prisma.project.delete({ where: { id } })
}

// ✅ SECURE: Auth + ownership check
'use server'
export async function deleteProject(id: string) {
  const { user } = await requireAuth()
  const project = await prisma.project.findUnique({ where: { id } })
  if (project?.userId !== user.id) throw new Error('FORBIDDEN')
  await prisma.project.delete({ where: { id } })
}
```

### Headers
```typescript
// next.config.ts — security headers
const securityHeaders = [
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'X-XSS-Protection', value: '1; mode=block' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
]
```

## Scan Pattern
When auditing a codebase, search for these patterns:
1. `|| '*'` or `?? '*'` in config — permissive fallbacks
2. `|| true` or `?? true` — debug/admin flags defaulting on
3. `cors()` without arguments — open CORS
4. Tables without `ENABLE ROW LEVEL SECURITY`
5. Server Actions without `requireAuth()`
6. `process.env.X || 'default'` where default is insecure
7. Missing rate limiting on auth endpoints
8. Missing CSRF protection on mutations

## Como Usar (comandos práticos de detecção)

Run these from the repo root to detect each pattern quickly:

```bash
# 1-2. Permissive fallbacks and flags defaulting on
grep -rnE "(\|\||\?\?)\s*['\"]\*['\"]" --include='*.{ts,tsx,js,jsx}' src/ app/
grep -rnE "(\|\||\?\?)\s*true" --include='*.{ts,tsx,js,jsx}' src/ app/

# 3. Open CORS (cors() with no args or origin: true / '*')
grep -rnE "cors\(\s*\)|origin:\s*(true|['\"]\*['\"])" --include='*.{ts,js}' src/ app/

# 4. Tables possibly missing RLS (list tables, then check ENABLE ROW LEVEL SECURITY)
grep -rniE "create table" --include='*.sql' . | grep -viE "row level security"
grep -rniL "ENABLE ROW LEVEL SECURITY" --include='*.sql' supabase/migrations/ 2>/dev/null

# 5. Server Actions without auth check ('use server' files lacking requireAuth)
grep -rl "'use server'" --include='*.{ts,tsx}' src/ app/ | xargs grep -L "requireAuth"

# 6. Insecure env fallbacks
grep -rnE "process\.env\.[A-Z_]+\s*(\|\||\?\?)\s*['\"]" --include='*.{ts,tsx,js,jsx}' src/ app/

# 7. Auth endpoints without rate limiting
grep -rnE "(login|signin|signup|reset-password|password)" --include='*.{ts,tsx}' src/app/api/ app/api/ 2>/dev/null | grep -viE "rateLimit|rate-limit"

# 8. Mutations possibly missing CSRF protection (POST/PUT/DELETE handlers)
grep -rnE "export\s+(async\s+)?function\s+(POST|PUT|DELETE|PATCH)" --include='route.ts' src/ app/ | grep -viE "csrf"
```

Review each hit manually — these are heuristics, not proofs. Zero hits does not mean secure; combine with the checklist above.
