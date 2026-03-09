---
name: stripe-integration
description: Stripe payment processing for SaaS applications. Trigger on checkout implementation, subscription billing, webhook handling, pricing page, payment forms, refund logic, or Stripe-specific debugging.
metadata:
  author: osforge
  version: '1.0'
---

# Stripe Integration (Next.js SaaS)

## Architecture
```
Client (Checkout) → Stripe Hosted/Elements → Webhook → Server Action → DB Update
NEVER handle raw card data. Always use Stripe Checkout or Elements.
```

## Setup
```typescript
// lib/stripe.ts
import Stripe from 'stripe'

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
  typescript: true,
})
```

## Checkout Session (Subscriptions)
```typescript
// app/api/checkout/route.ts
import { stripe } from '@/lib/stripe'
import { requireAuth } from '@/lib/supabase/server'

export async function POST(req: Request) {
  const { user } = await requireAuth()
  const { priceId } = await req.json()

  const session = await stripe.checkout.sessions.create({
    customer_email: user.email,
    mode: 'subscription',
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/billing?success=true`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    metadata: { userId: user.id },
    subscription_data: {
      metadata: { userId: user.id },
    },
  })

  return Response.json({ url: session.url })
}
```

## Webhook Handler
```typescript
// app/api/webhook/stripe/route.ts
import { stripe } from '@/lib/stripe'
import { headers } from 'next/headers'

export async function POST(req: Request) {
  const body = await req.text()
  const sig = (await headers()).get('stripe-signature')!

  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET!)
  } catch {
    return new Response('Invalid signature', { status: 400 })
  }

  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session
      await handleCheckoutComplete(session)
      break
    }
    case 'customer.subscription.updated':
    case 'customer.subscription.deleted': {
      const subscription = event.data.object as Stripe.Subscription
      await syncSubscriptionStatus(subscription)
      break
    }
    case 'invoice.payment_failed': {
      const invoice = event.data.object as Stripe.Invoice
      await handlePaymentFailed(invoice)
      break
    }
  }

  return new Response('OK', { status: 200 })
}
```

## Subscription Sync
```typescript
async function syncSubscriptionStatus(subscription: Stripe.Subscription) {
  const userId = subscription.metadata.userId
  await prisma.subscription.upsert({
    where: { stripeSubscriptionId: subscription.id },
    update: {
      status: subscription.status,
      currentPeriodEnd: new Date(subscription.current_period_end * 1000),
      cancelAtPeriodEnd: subscription.cancel_at_period_end,
    },
    create: {
      userId,
      stripeSubscriptionId: subscription.id,
      stripeCustomerId: subscription.customer as string,
      status: subscription.status,
      priceId: subscription.items.data[0].price.id,
      currentPeriodEnd: new Date(subscription.current_period_end * 1000),
    },
  })
}
```

## Customer Portal
```typescript
'use server'
export async function createPortalSession() {
  const { user } = await requireAuth()
  const sub = await prisma.subscription.findUnique({ where: { userId: user.id } })
  if (!sub?.stripeCustomerId) throw new Error('NO_SUBSCRIPTION')

  const session = await stripe.billingPortal.sessions.create({
    customer: sub.stripeCustomerId,
    return_url: `${process.env.NEXT_PUBLIC_APP_URL}/billing`,
  })
  redirect(session.url)
}
```

## Security Rules
- Webhook signature verification is MANDATORY — never skip
- NEVER trust client-side price data — always use server-side priceId lookup
- Store Stripe customer ID in DB, link to user
- Use `metadata` to link Stripe objects back to your user/org
- Test with Stripe CLI: `stripe listen --forward-to localhost:3000/api/webhook/stripe`
- Idempotency: webhooks can fire multiple times — upsert, don't insert
