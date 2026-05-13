# Stripe Integration

**Trigger:** payment, subscription, checkout, webhook, billing, pricing

---

## Core Rules

1. **NEVER handle raw card data** — Use Stripe Checkout or Elements
2. **Always verify webhook signatures** — Never trust unverified payloads
3. **Use metadata to link Stripe ↔ user** — Store user_id in metadata
4. **Idempotent webhook processing** — Handle duplicate events gracefully

---

## Checkout Session (Subscriptions)

```typescript
// app/api/checkout/route.ts
import { NextResponse } from 'next/server'
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function POST(request: Request) {
  const { priceId, userId } = await request.json()

  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing`,
    metadata: { userId }, // Link to your user
    subscription_data: {
      metadata: { userId },
    },
  })

  return NextResponse.json({ url: session.url })
}
```

---

## Webhook Handler

```typescript
// app/api/webhooks/stripe/route.ts
import { headers } from 'next/headers'
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)
const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!

export async function POST(request: Request) {
  const body = await request.text()
  const headersList = await headers()
  const signature = headersList.get('stripe-signature')!

  let event: Stripe.Event

  try {
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret)
  } catch (err) {
    console.error('Webhook signature verification failed')
    return new Response('Invalid signature', { status: 400 })
  }

  // Idempotency: Check if already processed
  const processed = await checkEventProcessed(event.id)
  if (processed) {
    return new Response('Already processed', { status: 200 })
  }

  try {
    switch (event.type) {
      case 'checkout.session.completed':
        await handleCheckoutComplete(event.data.object)
        break
      case 'customer.subscription.updated':
        await handleSubscriptionUpdate(event.data.object)
        break
      case 'customer.subscription.deleted':
        await handleSubscriptionCanceled(event.data.object)
        break
      case 'invoice.payment_failed':
        await handlePaymentFailed(event.data.object)
        break
    }

    await markEventProcessed(event.id)
    return new Response('OK', { status: 200 })
  } catch (err) {
    console.error('Webhook handler error:', err)
    return new Response('Handler error', { status: 500 })
  }
}
```

---

## Subscription Sync to DB

```typescript
async function handleSubscriptionUpdate(subscription: Stripe.Subscription) {
  const userId = subscription.metadata.userId

  await prisma.subscription.upsert({
    where: { stripeSubscriptionId: subscription.id },
    update: {
      status: subscription.status,
      priceId: subscription.items.data[0].price.id,
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
      cancelAtPeriodEnd: subscription.cancel_at_period_end,
    },
  })
}
```

---

## Customer Portal

```typescript
// app/api/portal/route.ts
export async function POST(request: Request) {
  const user = await requireAuth()

  const subscription = await prisma.subscription.findUnique({
    where: { userId: user.id },
  })

  if (!subscription?.stripeCustomerId) {
    return NextResponse.json({ error: 'No subscription' }, { status: 400 })
  }

  const session = await stripe.billingPortal.sessions.create({
    customer: subscription.stripeCustomerId,
    return_url: `${process.env.NEXT_PUBLIC_URL}/settings/billing`,
  })

  return NextResponse.json({ url: session.url })
}
```

---

## Pricing Page Pattern

```typescript
// lib/stripe.ts
export const PLANS = {
  free: {
    name: 'Free',
    price: 0,
    priceId: null,
    features: ['5 projects', 'Basic support'],
  },
  pro: {
    name: 'Pro',
    price: 29,
    priceId: process.env.STRIPE_PRO_PRICE_ID,
    features: ['Unlimited projects', 'Priority support', 'API access'],
  },
  enterprise: {
    name: 'Enterprise',
    price: 99,
    priceId: process.env.STRIPE_ENTERPRISE_PRICE_ID,
    features: ['Everything in Pro', 'SSO', 'Dedicated support'],
  },
} as const
```

---

## Testing Webhooks Locally

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger test events
stripe trigger checkout.session.completed
```
