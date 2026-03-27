---
name: nextjs-supabase-auth
description: "Padrões de autenticação Next.js App Router + Supabase Auth. ACIONE quando: configurando middleware de auth, RBAC multi-org, gerenciamento de sessão, refresh de token, RLS por tenant, OAuth flows, debugging de Supabase Auth. Keywords: auth, login, session, middleware, RBAC, role, permission, supabase auth, protected route, JWT, OAuth, cookie."
model: sonnet
allowed-tools: Read, Bash, Glob, Grep
metadata:
  author: osforge
  version: '1.1'
---

## Contexto do projeto
!`[ -f middleware.ts ] && echo "middleware.ts encontrado" || echo "middleware.ts não existe — auth guard não está configurado"`
!`grep -r "createServerClient\|createBrowserClient" --include="*.ts" --include="*.tsx" -l 2>/dev/null | head -5 || echo "Nenhum client Supabase encontrado"`

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


## Gotchas

- **`getSession()` vs `getUser()`**: NUNCA usar `getSession()` para checar auth em Server Actions ou middleware — a session pode ser forjada pelo cliente. Sempre usar `supabase.auth.getUser()` que valida o JWT no servidor.
- **Cookies não setados no middleware**: se o middleware não propaga corretamente os cookies de refresh, o usuário é deslogado inesperadamente. O padrão correto é chamar `supabase.auth.getUser()` no middleware e retornar o `response` com os cookies atualizados — não apenas `NextResponse.next()`.
- **Service role key no cliente**: a `SUPABASE_SERVICE_ROLE_KEY` não deve jamais ir para o bundle do cliente (sem prefixo `NEXT_PUBLIC_`). Ela bypassa RLS e compromete toda a segurança multi-tenant.
- **RLS esquecida em tabela nova**: ao criar uma nova tabela no Supabase, RLS não está habilitado por padrão. Sempre rodar `ALTER TABLE nome ENABLE ROW LEVEL SECURITY` e criar políticas antes de qualquer deploy.
- **OAuth redirect URL em produção**: o `redirectTo` no `signInWithOAuth` deve ser o domínio de produção, não localhost. Usar `process.env.NEXT_PUBLIC_APP_URL` e garantir que está na allowlist do Supabase dashboard.
- **Matcher no middleware**: o `config.matcher` deve excluir `_next/static`, `_next/image`, `favicon.ico` e rotas de webhook (`/api/webhook`). Middleware rodando em static assets causa erros silenciosos.
- **PKCE flow**: sempre usar PKCE (padrão do Supabase SSR) — não trocar por implicit flow mesmo que pareça mais simples. Implicit flow é vulnerável a token leakage.
