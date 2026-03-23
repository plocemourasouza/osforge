---
name: nextjs-saas
description: Next.js SaaS template principles (2026 Standards). React 19, Server Actions, Auth.js v6.
---

# Next.js SaaS Template (Updated 2026)

## Tech Stack

| Component | Technology | Version / Notes |
|-----------|------------|-----------------|
| Framework | Next.js | v16+ (App Router, React Compiler) |
| Runtime | Node.js | v24 (Krypton LTS) |
| Auth | Auth.js | v6 (formerly NextAuth) |
| Payments | Stripe API | Latest |
| Database | PostgreSQL | Prisma v6 (Serverless Driver) |
| Email | Resend | React Email |
| UI | Tailwind CSS | v4 (Oxide Engine, no config file) |

---

## Directory Structure

```
project-name/
├── prisma/
│   └── schema.prisma    # Database Schema
├── src/
│   ├── actions/         # NEW: Server Actions (Replaces API Routes for data mutation)
│   │   ├── auth-actions.ts
│   │   ├── billing-actions.ts
│   │   └── user-actions.ts
│   ├── app/
│   │   ├── (auth)/      # Route Group: Login, register
│   │   ├── (dashboard)/ # Route Group: Protected routes (App Layout)
│   │   ├── (marketing)/ # Route Group: Landing, pricing (Marketing Layout)
│   │   └── api/         # Only used for Webhooks or Edge cases
│   │       └── webhooks/stripe/
│   ├── components/
│   │   ├── emails/      # React Email templates
│   │   ├── forms/       # Client components using useActionState (React 19)
│   │   └── ui/          # Shadcn UI
│   ├── lib/
│   │   ├── auth.ts      # Auth.js v6 config
│   │   ├── db.ts        # Prisma Singleton
│   │   └── stripe.ts    # Stripe Singleton
│   └── styles/
│       └── globals.css  # Tailwind v4 imports (CSS only)
└── package.json
```

---

## SaaS Features

| Feature | Implementation |
|---------|---------------|
| Auth | Auth.js v6 + Passkeys + OAuth |
| Data Mutation | Server Actions (No API routes) |
| Subscriptions | Stripe Checkout & Customer Portal |
| Webhooks | Asynchronous Stripe event handling |
| Email | Transactional via Resend |
| Validation | Zod (Server-side validation) |

---

## Best Practices

- Shared configs in packages/config
- Shared types in packages/types
- Internal packages with `workspace:*`
- Use Turbo remote caching for CI
