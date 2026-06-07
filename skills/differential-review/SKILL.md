---
name: differential-review
description: Security-focused code review of diffs and PRs. Trigger on PR security review, git diff analysis, change impact assessment, or when reviewing commits that touch auth, payments, permissions, or data access patterns.
metadata:
  author: osforge
  version: '1.0'
  source: Trail of Bits differential-review
---

# Differential Review (Security-Focused PR Analysis)

## When to Use
- PRs touching auth, payments, permissions, or data access
- Changes to middleware, API routes, or Server Actions
- Database migration PRs (schema changes with security impact)
- Dependency updates (especially security-related packages)

## Review Process

### Step 1: Scope the Change
```bash
# See what files changed
git diff --stat main...HEAD

# Categorize by risk
git diff --name-only main...HEAD | while read f; do
  case "$f" in
    *middleware*|*auth*|*session*) echo "🔴 HIGH: $f" ;;
    *api/*|*actions/*|*server/*) echo "🟡 MEDIUM: $f" ;;
    *) echo "⚪ LOW: $f" ;;
  esac
done
```

### Step 2: Analyze High-Risk Changes
For each 🔴 HIGH file, check:

| Check | What to Look For |
|-------|------------------|
| Auth bypass | New paths that skip `requireAuth()` |
| Permission escalation | Role checks changed or removed |
| Data exposure | New fields in API responses (PII leak?) |
| Input validation | New user inputs without validation |
| SQL injection | Raw queries with string interpolation |
| CORS changes | Origin allowlist expanded |
| RLS changes | Policies weakened or disabled |
| Env changes | New secrets without documentation |

#### Concrete Examples (what each looks like in a diff)

**Auth bypass** — route handler loses its guard:
```diff
 export async function GET(req: Request) {
-  const session = await requireAuth()
   const data = await db.report.findMany()
```

**Permission escalation** — check removed without replacement:
```diff
-  if (user.role !== 'admin') throw new Error('FORBIDDEN')
   await deleteOrganization(orgId)  // now any member can delete the org
```

**Data exposure** — PII added to a public response:
```diff
   return NextResponse.json({
     id: user.id,
     name: user.name,
+    email: user.email,        // PII now in public API
+    stripeCustomerId: user.stripeCustomerId,
   })
```

**Input validation** — new param used without schema check:
```diff
+  const limit = Number(searchParams.get('limit'))  // NaN / negative / huge values unchecked
+  const rows = await db.user.findMany({ take: limit })
```

**SQL injection** — interpolation replaces parameterized query:
```diff
-  await prisma.$queryRaw`SELECT * FROM users WHERE name = ${name}`
+  await prisma.$queryRawUnsafe(`SELECT * FROM users WHERE name = '${name}'`)
```

**CORS weakening** — allowlist replaced by wildcard:
```diff
-  res.headers.set('Access-Control-Allow-Origin', 'https://app.example.com')
+  res.headers.set('Access-Control-Allow-Origin', '*')
```

**RLS weakening** — tenant filter dropped from policy:
```diff
-CREATE POLICY "org_read" ON projects FOR SELECT
-  USING (organization_id IN (SELECT organization_id FROM members WHERE user_id = auth.uid()));
+CREATE POLICY "org_read" ON projects FOR SELECT USING (true);
```

### Step 3: Context from Git History
```bash
# Who else touched these files recently?
git log --oneline -10 -- path/to/sensitive/file.ts

# Was this pattern changed before? Why?
git log --all -p -S 'requireAuth' -- path/to/file.ts

# Check if tests were added for security changes
git diff main...HEAD -- '*.test.ts' '*.spec.ts' | grep -c 'auth\|permission\|role'
```

### Step 4: Structured Output
```markdown
## Security Differential Review

### Scope
- Files changed: 12 (3 high-risk, 4 medium, 5 low)
- Auth-related: middleware.ts, lib/auth.ts
- Data-related: app/api/users/route.ts

### Findings
| # | Severity | File | Finding | Recommendation |
|---|----------|------|---------|----------------|
| 1 | 🔴 CRITICAL | middleware.ts | New `/api/webhook` path bypasses auth | Add signature verification |
| 2 | 🟡 MEDIUM | api/users/route.ts | Email exposed in GET response | Remove from public response |
| 3 | ⚪ LOW | prisma/schema.prisma | New table without RLS | Add RLS policy before merge |

### Verdict
⚠️ CHANGES REQUESTED — Fix #1 before merge
```

## Automated Checks (CI Integration)
```bash
# Check if auth-related files have corresponding tests
changed_auth=$(git diff --name-only main...HEAD | grep -E 'auth|middleware|permission')
for f in $changed_auth; do
  test_file="${f%.ts}.test.ts"
  if ! git diff --name-only main...HEAD | grep -q "$test_file"; then
    echo "⚠️ Missing test update for security file: $f"
  fi
done
```

## Red Flags (Auto-Block)
These patterns in a diff should ALWAYS be flagged:
- `// @ts-ignore` or `// @ts-expect-error` near auth code
- `as any` in permission checks
- `.skip` or removal of security tests
- `DISABLE_AUTH` or `BYPASS_RLS` env variables added
- `cors({ origin: '*' })` or `cors({ origin: true })`
