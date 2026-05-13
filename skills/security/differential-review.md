# Differential Review

**Trigger:** PR security review, git diff analysis, security-focused code review

---

## Purpose

Security-focused code review of diffs and PRs. Focus on changes to auth, payments, permissions, and data access patterns.

---

## 4-Step Process

### Step 1: Scope Assessment

```bash
# Get files changed
git diff --name-only main...HEAD

# Categorize by risk
```

| Risk | File Patterns |
|------|---------------|
| 🔴 Critical | `**/auth/**`, `**/api/**`, `middleware.ts`, `**/payment/**` |
| 🟠 High | `**/admin/**`, `prisma/schema.prisma`, `**/webhook/**` |
| 🟡 Medium | `lib/**`, `utils/**`, `services/**` |
| 🟢 Low | `components/**`, `styles/**`, `tests/**` |

### Step 2: Analyze High-Risk Changes

For each critical/high file:

```bash
# View diff with context
git diff main...HEAD -- path/to/file.ts
```

Check for:
- Auth/authz changes
- New API endpoints
- Permission logic changes
- Data access pattern changes
- Input validation changes
- Error handling changes

### Step 3: Git History Context

```bash
# Who last modified this area?
git log --oneline -5 -- path/to/file.ts

# When was security last reviewed?
git log --grep="security" --oneline -- path/to/file.ts
```

### Step 4: Structured Output

```markdown
## Security Review: PR #123

### Scope
- Files changed: 12
- Critical files: 2
- High-risk files: 3

### Findings

#### 🔴 Critical: Missing Auth Check
- **File:** `app/api/admin/users/route.ts:15`
- **Change:** New DELETE endpoint added
- **Issue:** No authentication check
- **Recommendation:** Add `requireAuth()` and role check

#### 🟡 Medium: Verbose Error Message
- **File:** `app/api/auth/login/route.ts:42`
- **Change:** Error handling modified
- **Issue:** Returns specific error "User not found" vs "Invalid credentials"
- **Recommendation:** Use generic error messages

### Approved Changes
- `components/ui/button.tsx` — Styling only
- `tests/auth.test.ts` — Test additions

### Missing Security Tests
- [ ] Test for unauthorized access to new admin endpoint
- [ ] Test for rate limiting on login endpoint
```

---

## Red Flags

### Code Patterns

```typescript
// 🔴 @ts-ignore near auth code
// @ts-ignore
const user = await getUser()  // Why ignore types here?

// 🔴 `as any` in permissions
const role = user.role as any  // Bypassing type safety

// 🔴 Removed security tests
- it('should reject unauthorized users', () => {...})

// 🔴 Direct database access without auth
export async function POST(request: Request) {
  const { id } = await request.json()
  await prisma.user.delete({ where: { id } })  // No auth!
}
```

### Schema Changes

```prisma
// 🟠 New table without RLS consideration
model AdminSettings {
  id    String @id
  value String
}
// Does this need RLS? Who can access?

// 🔴 Removing auth field
model User {
  id       String @id
- password String
+ // password removed - why?
}
```

### API Changes

```typescript
// 🔴 New public endpoint
export async function GET(request: Request) {
  // Returns user data without auth
  return Response.json(await prisma.user.findMany())
}

// 🟠 Changed from POST to GET (CSRF implications)
- export async function POST(request: Request) {
+ export async function GET(request: Request) {
```

---

## CI Integration

```yaml
# .github/workflows/security-review.yml
name: Security Review
on:
  pull_request:
    paths:
      - 'app/api/**'
      - 'middleware.ts'
      - 'prisma/schema.prisma'
      - 'lib/auth/**'

jobs:
  security-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check for missing auth
        run: |
          # Find API routes without auth
          for file in $(git diff --name-only origin/main...HEAD | grep 'app/api'); do
            if ! grep -q "requireAuth\|getUser\|auth()" "$file"; then
              echo "⚠️ Missing auth check: $file"
            fi
          done
```

---

## Review Checklist

### Authentication
- [ ] All new endpoints have auth checks
- [ ] Auth checks use `getUser()` not `getSession()`
- [ ] No auth bypass paths introduced

### Authorization
- [ ] Resource ownership verified
- [ ] Role checks present where needed
- [ ] No privilege escalation paths

### Input Validation
- [ ] New inputs validated with Zod
- [ ] No SQL injection vectors
- [ ] No XSS vectors

### Data Exposure
- [ ] No sensitive data in responses
- [ ] Error messages don't leak info
- [ ] Logging doesn't include PII

### Tests
- [ ] Security tests for new endpoints
- [ ] Auth failure cases tested
- [ ] No security tests removed
