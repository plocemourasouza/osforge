---
name: nextjs-supabase-auth
description: Authentication patterns for Next.js App Router + Supabase Auth. Trigger on auth middleware, multi-org RBAC, session management, token refresh, RLS-by-tenant, OAuth flows, or Supabase Auth debugging in Next.js context.
metadata:
  author: osforge
  version: '1.0'
---

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

## Security Checklist
- [ ] Middleware protects all `/dashboard/*` routes
- [ ] `getUser()` (not `getSession()`) for auth checks — session can be spoofed
- [ ] RLS enabled on ALL tenant-scoped tables
- [ ] Service role key ONLY in Server Actions, never client
- [ ] OAuth callback validates state parameter
- [ ] Email confirmation required before access
