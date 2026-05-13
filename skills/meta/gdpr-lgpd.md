# GDPR / LGPD Data Handling

**Trigger:** Consent management, data subject rights, privacy policies, data retention, audit logging, LGPD compliance.

---

## LGPD vs GDPR Mapping

| LGPD | GDPR | Requirement |
|------|------|-------------|
| Consentimento | Consent | Explicit, informed, revocable |
| Acesso | Access | Export user data on request |
| Eliminação | Erasure | Delete data on request |
| Portabilidade | Portability | Machine-readable export |
| Anonimização | Anonymization | Remove PII from analytics |

---

## Consent Management Schema

```prisma
model Consent {
  id        String   @id @default(cuid())
  userId    String
  purpose   String   // "marketing", "analytics", "necessary"
  granted   Boolean
  grantedAt DateTime?
  revokedAt DateTime?
  ipAddress String?
  userAgent String?

  user      User     @relation(fields: [userId], references: [id])

  @@index([userId, purpose])
}
```

---

## Data Subject Rights

### Right to Access (Export)
```typescript
export async function exportUserData(userId: string) {
  const user = await prisma.user.findUnique({
    where: { id: userId },
    include: {
      orders: true,
      consents: true,
      auditLogs: true,
    },
  })

  return {
    personal: {
      name: user.name,
      email: user.email,
      createdAt: user.createdAt,
    },
    orders: user.orders,
    consents: user.consents,
    exportedAt: new Date().toISOString(),
  }
}
```

### Right to Erasure (Delete)
```typescript
export async function deleteUserData(userId: string) {
  await prisma.$transaction([
    // Anonymize orders (keep for accounting)
    prisma.order.updateMany({
      where: { userId },
      data: {
        customerName: 'DELETED',
        customerEmail: 'deleted@example.com',
      },
    }),
    // Delete personal data
    prisma.consent.deleteMany({ where: { userId } }),
    prisma.session.deleteMany({ where: { userId } }),
    prisma.user.delete({ where: { id: userId } }),
  ])

  // Log deletion for audit
  await auditLog('user_deleted', { userId, deletedAt: new Date() })
}
```

---

## Audit Logging Middleware

```typescript
// middleware/audit.ts
export async function auditLog(
  action: string,
  data: Record<string, unknown>,
  context?: { userId?: string; ipAddress?: string }
) {
  await prisma.auditLog.create({
    data: {
      action,
      data: JSON.stringify(data),
      userId: context?.userId,
      ipAddress: context?.ipAddress,
      timestamp: new Date(),
    },
  })
}
```

---

## Data Retention

```typescript
// cron/data-retention.ts
export async function runDataRetention() {
  const retentionPeriod = 365 * 2 // 2 years

  // Delete old audit logs
  await prisma.auditLog.deleteMany({
    where: {
      timestamp: {
        lt: new Date(Date.now() - retentionPeriod * 24 * 60 * 60 * 1000),
      },
    },
  })

  // Anonymize old orders
  await prisma.order.updateMany({
    where: {
      createdAt: {
        lt: new Date(Date.now() - retentionPeriod * 24 * 60 * 60 * 1000),
      },
      customerEmail: { not: 'deleted@example.com' },
    },
    data: {
      customerName: 'ARCHIVED',
      customerEmail: 'archived@example.com',
    },
  })
}
```

---

## Requirements

1. **DPO/Encarregado designation** — Named person responsible for compliance
2. **Breach notification** — 72 hours to authority (GDPR), "reasonable time" (LGPD)
3. **Cookie consent banner** — Clear opt-in for non-essential cookies
4. **Privacy policy** — Clear, accessible, in user's language
