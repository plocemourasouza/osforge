# Deployment Procedures

**Trigger:** Deployment, release process, rollback, blue-green, canary deployment.

---

## Deployment Strategies

| Strategy | Risk | Rollback | Use Case |
|----------|------|----------|----------|
| **Direct** | High | Manual | Dev/staging |
| **Blue-Green** | Low | Instant | Production |
| **Canary** | Low | Gradual | High traffic |
| **Rolling** | Medium | Manual | Kubernetes |

---

## Safe Deployment Workflow

```
1. Pre-deploy checks
   └── Tests pass
   └── Types pass
   └── Lint pass
   └── Build succeeds

2. Deploy to staging
   └── Smoke tests
   └── Integration tests

3. Deploy to production
   └── Feature flags (if applicable)
   └── Canary (small percentage)
   └── Full rollout

4. Post-deploy verification
   └── Health checks
   └── Error monitoring
   └── Metrics dashboards
```

---

## Vercel Deployment

```bash
# Preview deployment (PR)
vercel

# Production deployment
vercel --prod

# Rollback to previous
vercel rollback
```

### Environment Variables
```bash
# Set production env var
vercel env add STRIPE_SECRET_KEY production

# Pull env vars locally
vercel env pull .env.local
```

---

## Rollback Procedures

### Vercel
```bash
# List deployments
vercel ls

# Rollback to specific deployment
vercel alias set <deployment-url> <production-domain>

# Or use dashboard
# Deployments → ... → Promote to Production
```

### Git-based
```bash
# Revert last commit
git revert HEAD
git push

# Redeploy previous version
git checkout <commit-hash>
git push --force-with-lease
```

---

## Health Checks

```typescript
// app/api/health/route.ts
export async function GET() {
  try {
    // Check database
    await prisma.$queryRaw`SELECT 1`

    // Check external services
    const supabase = await supabaseClient.auth.getSession()

    return Response.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      checks: {
        database: 'ok',
        auth: 'ok',
      }
    })
  } catch (error) {
    return Response.json({
      status: 'unhealthy',
      error: error.message,
    }, { status: 503 })
  }
}
```

---

## Verification Steps

### Pre-deploy
- [ ] All tests pass
- [ ] TypeScript compiles
- [ ] No lint errors
- [ ] Build succeeds locally
- [ ] Environment variables set

### Post-deploy
- [ ] Health endpoint returns 200
- [ ] Critical user flows work
- [ ] No new errors in monitoring
- [ ] Metrics look normal
- [ ] Logs show no anomalies

---

## Feature Flags

```typescript
// lib/flags.ts
export const flags = {
  newCheckout: process.env.NEXT_PUBLIC_FLAG_NEW_CHECKOUT === 'true',
  betaFeatures: process.env.NEXT_PUBLIC_FLAG_BETA === 'true',
}

// Usage
if (flags.newCheckout) {
  return <NewCheckout />
}
return <OldCheckout />
```
