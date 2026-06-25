---
name: asaas-integration
description: "ASAAS payment integration (Brazilian gateway: Pix, boleto, credit card, subscriptions). Use when: integrating ASAAS, charging via Pix/boleto/card, handling ASAAS webhooks, billing Brazilian customers, or migrating from Stripe to a BR provider. Keywords: ASAAS, Pix, boleto, cobrança, pagamento BR, gateway brasileiro, subscription BR. Do NOT use for: Stripe (stripe-integration), generic payment UI (frontend-ui-system), tax/fiscal documents (NF-e)."
model: sonnet
allowed-tools: Read, Grep, Glob, Edit
metadata:
  version: "1.0.0"
  note: "ASAAS docs/training coverage is thin — this skill carries the discipline; for the current API surface use Context7 (context7-docs-first)."
---

# ASAAS Integration (Pix · boleto · card)

**Iron Law:** `NEVER TRUST A CLIENT-REPORTED PAYMENT STATUS — CONFIRM VIA WEBHOOK + SERVER-SIDE API READ`

> **Current API:** ASAAS endpoints, field names, and limits change and are poorly covered by model training. For exact request/response shapes, **use Context7** (`context7-docs-first`) or `docs.asaas.com` — this skill is the discipline, not the API reference.

## When NOT to use
- Stripe or card-first global billing → use `stripe-integration`
- Pure checkout/payment UI with no provider logic → `frontend-ui-system`
- Fiscal documents (NF-e/NFS-e) → out of scope

## Process
### 1. Environment & secrets
Use the sandbox base URL first; switch to production only after end-to-end tests. The API key goes in the `access_token` request header and is loaded **server-side only** from env (never shipped to the client).
**Done when:** sandbox key works from a server route and no key appears in any client bundle.

### 2. Customer + charge
Create/reuse the customer, then create the charge with the right `billingType` (Pix / boleto / credit card). Persist the ASAAS id on your record before returning to the client.
**Done when:** a sandbox charge is created and its ASAAS id is stored locally.

### 3. Webhooks are the source of truth
Register the webhook, verify it (shared token/signature), and treat the webhook event as the authority for status transitions (CONFIRMED/RECEIVED/OVERDUE/REFUNDED). Make the handler **idempotent** (dedupe by event/payment id).
**Done when:** replaying the same webhook twice produces no duplicate side effects.

### 4. Reconcile
On webhook gaps, reconcile by reading the payment from the API — don't infer status from the client.
**Done when:** a charge whose webhook was missed still converges to the correct status via API read.

## Anti-patterns
| WRONG | RIGHT |
|---|---|
| Marking an order paid from a client callback | Mark paid only on a verified webhook (or API read) |
| API key in `NEXT_PUBLIC_*` / client code | Server-only env; never in the bundle |
| Non-idempotent webhook handler | Dedupe by event id; safe to replay |
| Hardcoding endpoint shapes from memory | Confirm the current API via Context7 |

## References
- Current API & limits → **Context7** (`context7-docs-first`) / `docs.asaas.com`
- Card-first/global equivalent → `skills/stripe-integration`
- Security of secrets/inputs → `skills/security-best-practices`
