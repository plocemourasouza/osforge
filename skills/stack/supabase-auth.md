# Next.js + Supabase Auth

**Trigger:** auth, RBAC, session, OAuth, middleware, login, logout, JWT

---

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
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) => {
            request.cookies.set(name, value)
            response.cookies.set(name, value, options)
          })
        },
      },
    }
  )

  // IMPORTANT: Use getUser(), not getSession()
  const { data: { user } } = await supabase.auth.getUser()

  // Protect routes
  if (!user && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return response
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
}
```

---

## Server-Side Auth Helper

```typescript
// lib/auth.ts
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

export async function getSupabaseServer() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options)
          )
        },
      },
    }
  )
}

export async function requireAuth() {
  const supabase = await getSupabaseServer()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  return user
}
```

---

## Multi-Org RBAC

```typescript
// types/auth.ts
type Role = 'owner' | 'admin' | 'member' | 'viewer'

type OrgMembership = {
  orgId: string
  role: Role
}

// lib/rbac.ts
const roleHierarchy: Record<Role, number> = {
  owner: 4,
  admin: 3,
  member: 2,
  viewer: 1,
}

export function hasPermission(userRole: Role, requiredRole: Role): boolean {
  return roleHierarchy[userRole] >= roleHierarchy[requiredRole]
}

export async function requireOrgRole(orgId: string, requiredRole: Role) {
  const user = await requireAuth()
  const supabase = await getSupabaseServer()

  const { data: membership } = await supabase
    .from('org_memberships')
    .select('role')
    .eq('user_id', user.id)
    .eq('org_id', orgId)
    .single()

  if (!membership || !hasPermission(membership.role, requiredRole)) {
    throw new Error('Unauthorized')
  }

  return { user, role: membership.role }
}
```

---

## RLS Policies for Tenant Isolation

```sql
-- Enable RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Users can only see orders from their org
CREATE POLICY "Org members can view orders"
  ON orders FOR SELECT
  USING (
    org_id IN (
      SELECT org_id FROM org_memberships
      WHERE user_id = auth.uid()
    )
  );

-- Only admins+ can insert
CREATE POLICY "Admins can insert orders"
  ON orders FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM org_memberships
      WHERE user_id = auth.uid()
        AND org_id = orders.org_id
        AND role IN ('owner', 'admin')
    )
  );
```

---

## Token Refresh (SSR Cookies)

Tokens are automatically refreshed via SSR cookies. Never use localStorage.

```typescript
// The middleware handles token refresh automatically
// Just ensure you call getUser() to trigger refresh check
```

---

## OAuth with PKCE Flow

```typescript
// app/login/page.tsx
'use client'

import { createBrowserClient } from '@supabase/ssr'

export function LoginPage() {
  const supabase = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )

  const handleGoogleLogin = async () => {
    await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    })
  }

  return <button onClick={handleGoogleLogin}>Sign in with Google</button>
}
```

```typescript
// app/auth/callback/route.ts
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url)
  const code = searchParams.get('code')
  const next = searchParams.get('next') ?? '/dashboard'

  if (code) {
    const cookieStore = await cookies()
    const supabase = createServerClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        cookies: {
          getAll() { return cookieStore.getAll() },
          setAll(cookiesToSet) {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          },
        },
      }
    )

    const { error } = await supabase.auth.exchangeCodeForSession(code)
    if (!error) {
      return NextResponse.redirect(`${origin}${next}`)
    }
  }

  return NextResponse.redirect(`${origin}/auth/error`)
}
```

---

## Golden Rule

**Always use `getUser()`, not `getSession()` for auth checks.**

`getSession()` reads from cookies without validation. `getUser()` validates the JWT with Supabase servers.
