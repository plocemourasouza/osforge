---
name: better-auth
description: "Better Auth — framework-agnostic TypeScript auth (sessions, email/password, OAuth, plugins) in Next.js App Router. Use when: setting up Better Auth, session management, OAuth/social login, email+password, RBAC/organizations via plugins, or migrating to Better Auth. Keywords: Better Auth, better-auth, auth setup, session, OAuth, social login, RBAC, multi-tenant auth. Do NOT use for: Supabase Auth (nextjs-supabase-auth), pure authz of a resource (security-best-practices), payment auth."
model: sonnet
allowed-tools: Read, Grep, Glob, Edit
metadata:
  version: "1.0.0"
  note: "Better Auth is recent — model/Context7 coverage may lag. This skill carries the discipline; for the current API use Context7 (context7-docs-first) / better-auth.com."
---

# Better Auth (Next.js App Router)

**Iron Law:** `VALIDATE THE SESSION SERVER-SIDE AT EVERY PROTECTED ENTRY — NEVER TRUST A CLIENT-HELD SESSION`

> **Current API:** Better Auth's API and plugin set evolve fast. For exact config, handlers, and plugin options, **use Context7** (`context7-docs-first`) or `better-auth.com` — this skill is the discipline.

## When NOT to use
- Supabase as the auth provider → use `nextjs-supabase-auth`
- Authorizing access to a specific resource (ownership checks) → `security-best-practices`
- Generic Next.js routing/middleware unrelated to auth → `nextjs-react-expert`

## Process
### 1. Server instance + adapter
Configure the auth instance with your DB adapter (Prisma/Postgres) and required env secrets (server-only). Mount the route handler.
**Done when:** the auth handler responds and a session row is created on sign-in.

### 2. Session check at the boundary
Read/validate the session on the **server** (Server Component / Route Handler / middleware) at every protected entry. The client may *reflect* session state, but authorization decisions happen server-side.
**Done when:** a protected route returns 401/redirect with no/invalid session, proven by a test.

### 3. Providers & plugins
Add email+password and/or OAuth providers; add plugins (organization/RBAC, 2FA) only as needed — each plugin is surface area. Map roles to your authorization checks.
**Done when:** sign-in works for each enabled provider and roles gate the right routes.

### 4. Multi-tenant / RLS alignment
If multi-tenant, ensure the session's tenant is enforced in queries (and in Postgres RLS where used). Auth ≠ authorization — verify ownership per request.
**Done when:** a user of tenant A cannot read tenant B data, proven by a test.

## Anti-patterns
| WRONG | RIGHT |
|---|---|
| Gating only in client components | Server-side session check at the entry |
| Treating "authenticated" as "authorized" | Verify resource ownership/role per request |
| Secrets in client/env shipped to browser | Server-only secrets |
| Adding every plugin "just in case" | Add plugins only when a need is real |

## References
- Current API, plugins, config → **Context7** (`context7-docs-first`) / `better-auth.com`
- Supabase alternative → `skills/nextjs-supabase-auth`
- Authorization & input safety → `skills/security-best-practices`
