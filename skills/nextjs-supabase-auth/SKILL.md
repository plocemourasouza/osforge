---
name: nextjs-supabase-auth
description: "Next.js App Router + Supabase Auth authentication patterns. Use when: configuring auth middleware, multi-org RBAC, session management, token refresh, per-tenant RLS, OAuth flows, debugging Supabase Auth. Keywords: auth, login, session, middleware, RBAC, role, permission, supabase auth, protected route, JWT, OAuth, cookie."
model: sonnet
allowed-tools: Read, Bash, Glob, Grep
metadata:
  author: osforge
  version: '1.1'
---

## Project context
!`[ -f middleware.ts ] && echo "middleware.ts found" || echo "middleware.ts does not exist — auth guard is not configured"`
!`grep -r "createServerClient\|createBrowserClient" --include="*.ts" --include="*.tsx" -l 2>/dev/null | head -5 || echo "No Supabase client found"`

# Next.js + Supabase Auth Patterns

## Middleware Auth Guard
```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({ request })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => request.cookies.getAll(),
        setAll: (cookiesToSet) => {
          cookiesToSet.forEach(({ name, value, options }) => {
            response.cookies.set(name, value, options)
          })
        },
      },
    }
  )

  const { data: { user } } = await supabase.auth.getUser()

  // Protect authenticated routes
  if (!user && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Redirect logged-in users away from auth pages
  if (user && ['/login', '/signup'].includes(request.nextUrl.pathname)) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  return response
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|api/webhook).*)'],
}
```

## Server-Side Auth Helper
```typescript
// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => cookieStore.getAll(),
        setAll: (cookiesToSet) => {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options))
        },
      },
    }
  )
}

// Usage in Server Actions
export async function requireAuth() {
  const supabase = await createClient()
  const { data: { user }, error } = await supabase.auth.getUser()
  if (!user) throw new Error('UNAUTHORIZED')
  return { supabase, user }
}
```

## Multi-Org RBAC Pattern
```typescript
// Tenant context per request
export async function requireOrgAccess(orgSlug: string) {
  const { supabase, user } = await requireAuth()
  
  const { data: membership } = await supabase
    .from('members')
    .select('role, organization:organizations(id, slug)')
    .eq('user_id', user.id)
    .eq('organizations.slug', orgSlug)
    .single()

  if (!membership) throw new Error('FORBIDDEN')
  
  return { supabase, user, org: membership.organization, role: membership.role }
}

// Role checks
type OrgRole = 'owner' | 'admin' | 'member' | 'viewer'
const ROLE_HIERARCHY: Record<OrgRole, number> = { owner: 4, admin: 3, member: 2, viewer: 1 }

export function requireRole(userRole: OrgRole, minRole: OrgRole) {
  if (ROLE_HIERARCHY[userRole] < ROLE_HIERARCHY[minRole]) {
    throw new Error('INSUFFICIENT_PERMISSIONS')
  }
}
```

## RLS Policies for Multi-Tenant
```sql
-- Users can only see their org's data
CREATE POLICY "org_isolation" ON projects
  FOR ALL USING (
    organization_id IN (
      SELECT organization_id FROM members
      WHERE user_id = auth.uid()
    )
  );

-- Role-based write access
CREATE POLICY "admin_write" ON projects
  FOR INSERT WITH CHECK (
    EXISTS (
      SELECT 1 FROM members
      WHERE user_id = auth.uid()
      AND organization_id = projects.organization_id
      AND role IN ('owner', 'admin')
    )
  );
```

## Token Refresh Strategy
- Supabase SSR client auto-refreshes tokens via middleware cookies
- NEVER store tokens in localStorage (XSS risk)
- Set `PKCE` flow for OAuth (default in Supabase)
- Handle expired sessions gracefully: redirect to `/login?expired=true`

## OAuth Configuration
```typescript
// Server Action for OAuth
'use server'
export async function signInWithProvider(provider: 'google' | 'github') {
  const supabase = await createClient()
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider,
    options: {
      redirectTo: `${process.env.NEXT_PUBLIC_APP_URL}/auth/callback`,
    },
  })
  if (error) throw error
  redirect(data.url)
}
```

## Debug Checklist

When auth doesn't work, check in this order:

1. **Supabase logs** — Dashboard → Logs → Auth. Look for `invalid_grant`, `refresh_token_not_found` errors, email rate limits.
2. **Network inspector** — check requests to `/auth/v1/token`. Status 400/401 indicates an invalid token; verify that `sb-*` cookies are being sent and updated in the response.
3. **Cookies in the browser** — DevTools → Application → Cookies. `sb-<project-ref>-auth-token` cookies must exist. Missing = middleware is not propagating `setAll`.

Common symptoms and likely cause:

| Symptom | Likely cause | Where to look |
|---------|----------------|------------|
| Redirect loop (login ↔ dashboard) | Middleware redirects but cookies don't persist; or matcher covers the login route itself | Network inspector (cookies in response), `config.matcher` |
| Expired token / randomly logged out | Middleware doesn't call `getUser()` or doesn't return the `response` with refresh cookies | middleware.ts, `sb-*` cookies in the browser |
| Silent RLS (query returns `[]` with no error) | RLS enabled with no policy for the case, or query runs with the anon key without a session | Supabase logs (Postgres), test the query in the SQL Editor with `auth.uid()` |
| OAuth returns to login with no session | `redirectTo` outside the allowlist or callback doesn't exchange the code | Supabase Dashboard → Auth → URL Configuration, `/auth/callback` route |
| Works locally, breaks in production | `NEXT_PUBLIC_APP_URL` pointing to localhost; domain outside the allowlist | Production env vars, Supabase URL allowlist |

## Security Checklist
- [ ] Middleware protects all `/dashboard/*` routes
- [ ] `getUser()` (not `getSession()`) for auth checks — session can be spoofed
- [ ] RLS enabled on ALL tenant-scoped tables
- [ ] Service role key ONLY in Server Actions, never client
- [ ] OAuth callback validates state parameter
- [ ] Email confirmation required before access


## Gotchas

- **`getSession()` vs `getUser()`**: NEVER use `getSession()` to check auth in Server Actions or middleware — the session can be forged by the client. Always use `supabase.auth.getUser()`, which validates the JWT on the server.
- **Cookies not set in middleware**: if the middleware doesn't correctly propagate the refresh cookies, the user is logged out unexpectedly. The correct pattern is to call `supabase.auth.getUser()` in the middleware and return the `response` with the updated cookies — not just `NextResponse.next()`.
- **Service role key on the client**: `SUPABASE_SERVICE_ROLE_KEY` must never reach the client bundle (without the `NEXT_PUBLIC_` prefix). It bypasses RLS and compromises the entire multi-tenant security.
- **RLS forgotten on a new table**: when creating a new table in Supabase, RLS is not enabled by default. Always run `ALTER TABLE name ENABLE ROW LEVEL SECURITY` and create policies before any deploy.
- **OAuth redirect URL in production**: the `redirectTo` in `signInWithOAuth` must be the production domain, not localhost. Use `process.env.NEXT_PUBLIC_APP_URL` and make sure it's in the Supabase dashboard allowlist.
- **Middleware matcher**: `config.matcher` must exclude `_next/static`, `_next/image`, `favicon.ico`, and webhook routes (`/api/webhook`). Middleware running on static assets causes silent errors.
- **PKCE flow**: always use PKCE (the Supabase SSR default) — don't switch to the implicit flow even if it seems simpler. The implicit flow is vulnerable to token leakage.
