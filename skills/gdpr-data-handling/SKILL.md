---
name: gdpr-data-handling
description: GDPR/LGPD compliance patterns for data handling. Trigger on consent management, data subject rights (access, deletion, portability), privacy policies, data retention, audit logging, or LGPD compliance requirements.
metadata:
  author: osforge
  version: '1.0'
---

# GDPR / LGPD Data Handling

## LGPD vs GDPR Quick Map

| Requirement | GDPR | LGPD (Brazil) | Implementation |
|---|---|---|---|
| Legal basis for processing | Art. 6 (6 bases) | Art. 7 (10 bases) | Consent + legitimate interest |
| Data subject rights | Arts. 15-22 | Arts. 17-18 | Self-service portal |
| DPO requirement | Conditional | Always (Encarregado) | Designate + publish contact |
| Breach notification | 72 hours | "Reasonable time" | Automated alerting |
| Cross-border transfers | Adequate + SCCs | Similar to GDPR | Check adequacy decisions |
| Fines | Up to 4% revenue | Up to 2% revenue (R$50M cap) | Compliance program |

## Consent Management
```typescript
// Schema
model Consent {
  id        String   @id @default(cuid())
  userId    String
  purpose   ConsentPurpose
  granted   Boolean
  grantedAt DateTime?
  revokedAt DateTime?
  ipAddress String?
  userAgent String?
  version   String   // Policy version consented to
  @@unique([userId, purpose])
  @@index([userId])
}

enum ConsentPurpose {
  ESSENTIAL        // Always allowed, no consent needed
  ANALYTICS        // Usage analytics
  MARKETING        // Email marketing, retargeting
  THIRD_PARTY      // Third-party integrations
}

// Server Action
'use server'
export async function updateConsent(purpose: ConsentPurpose, granted: boolean) {
  const { user } = await requireAuth()
  await prisma.consent.upsert({
    where: { userId_purpose: { userId: user.id, purpose } },
    update: { granted, [granted ? 'grantedAt' : 'revokedAt']: new Date() },
    create: { userId: user.id, purpose, granted, grantedAt: granted ? new Date() : null, version: CURRENT_POLICY_VERSION },
  })
}
```

## Data Subject Rights (Self-Service)

### Right to Access (Export)
```typescript
'use server'
export async function exportMyData() {
  const { user } = await requireAuth()
  const data = {
    profile: await prisma.user.findUnique({ where: { id: user.id } }),
    projects: await prisma.project.findMany({ where: { userId: user.id } }),
    consents: await prisma.consent.findMany({ where: { userId: user.id } }),
    activityLog: await prisma.auditLog.findMany({ where: { userId: user.id }, take: 1000 }),
  }
  // Return as downloadable JSON
  return sanitizePII(data) // Remove internal IDs, timestamps as needed
}

// Reference implementation — adapt the stripped keys to your schema.
// Removes internal/operational fields that the data subject does not need
// and that may leak system internals (GDPR data minimization).
function sanitizePII<T>(data: T): T {
  const INTERNAL_KEYS = new Set([
    'id', 'internalId', 'passwordHash', 'stripeCustomerId',
    'createdById', 'updatedAt', 'deletedAt', 'sessionToken',
  ])
  const strip = (value: unknown): unknown => {
    if (Array.isArray(value)) return value.map(strip)
    if (value && typeof value === 'object') {
      return Object.fromEntries(
        Object.entries(value as Record<string, unknown>)
          .filter(([key]) => !INTERNAL_KEYS.has(key))
          .map(([key, v]) => [key, strip(v)]),
      )
    }
    return value
  }
  return strip(data) as T
}
```

### Right to Deletion
```typescript
'use server'
export async function deleteMyAccount() {
  const { user } = await requireAuth()
  await prisma.$transaction([
    prisma.consent.deleteMany({ where: { userId: user.id } }),
    prisma.auditLog.updateMany({ where: { userId: user.id }, data: { userId: 'DELETED_USER' } }),
    prisma.project.deleteMany({ where: { userId: user.id } }),
    prisma.user.delete({ where: { id: user.id } }),
  ])
  // Also: revoke Supabase auth, clear Stripe customer, etc.
}
```

## Audit Logging
```typescript
// Middleware for all data access
async function auditLog(action: string, resource: string, userId: string, details?: Record<string, unknown>) {
  await prisma.auditLog.create({
    data: {
      action, // 'READ' | 'CREATE' | 'UPDATE' | 'DELETE' | 'EXPORT'
      resource, // 'user' | 'project' | 'payment'
      userId,
      details: details ? JSON.stringify(details) : null,
      ipAddress: headers().get('x-forwarded-for'),
      timestamp: new Date(),
    },
  })
}
```

## Data Retention Policy
```typescript
// Cron job: delete data past retention period
async function enforceRetention() {
  const policies = [
    { table: 'auditLog', field: 'timestamp', retention: 365 }, // 1 year
    { table: 'session', field: 'expiresAt', retention: 30 },   // 30 days
    { table: 'invitation', field: 'createdAt', retention: 7 }, // 7 days
  ]
  for (const p of policies) {
    const cutoff = new Date(Date.now() - p.retention * 86400000)
    await prisma[p.table].deleteMany({ where: { [p.field]: { lt: cutoff } } })
  }
}
```

## Checklist
- [ ] Privacy policy published and versioned
- [ ] Cookie consent banner (essential cookies exempt)
- [ ] Data export endpoint (JSON format)
- [ ] Account deletion with cascade
- [ ] Audit logging on all PII access
- [ ] Data retention cron job
- [ ] DPO/Encarregado contact published
- [ ] Breach notification process documented
