# Stripe Integration — Setup Documentation

**Date:** 6 April 2026
**Environment:** Sandbox (test mode)
**Account:** Stripe account acct via `sk_test_51TJ7By...`

---

## What Was Created

### Products (17 total)

**Subscription Tiers (3 products, each with monthly + annual prices):**

| Tier | Monthly (AUD) | Annual (AUD) | Monthly Price ID | Annual Price ID |
|------|--------------|--------------|-----------------|-----------------|
| Starter | $699/mo | $7,549/yr | `price_1TJ7WZIwmeZH7II9pYW4Zsx1` | `price_1TJ7WZIwmeZH7II9YnAvV2us` |
| Professional | $1,499/mo | $16,199/yr | `price_1TJ7WbIwmeZH7II9ocZmjVrF` | `price_1TJ7WbIwmeZH7II9HRT3ePOD` |
| Enterprise | $2,499/mo | $26,999/yr | `price_1TJ7WdIwmeZH7II9R4QQ9yYs` | `price_1TJ7WeIwmeZH7II9NQQ5BWL0` |

**Setup Fees (6 products — deposit + final for each tier):**

| Tier | Deposit (50%) | Final (50%) |
|------|--------------|-------------|
| Starter | $1,250 (`price_1TJ7WaIwmeZH7II97pvhM3tl`) | $1,250 (`price_1TJ7WaIwmeZH7II9BS0nqpz9`) |
| Professional | $2,500 (`price_1TJ7WcIwmeZH7II9swaxqKdI`) | $2,500 (`price_1TJ7WdIwmeZH7II9QE7l3xqQ`) |
| Enterprise | $5,000 (`price_1TJ7WeIwmeZH7II9DVcprb98`) | $5,000 (`price_1TJ7WfIwmeZH7II9IOc0ReOJ`) |

**Add-Ons (8 products):**

| Add-On | Price (AUD) | Type | Price ID |
|--------|------------|------|----------|
| Extra Voice Minutes (100 mins) | $99/mo | Recurring | `price_1TJ7WgIwmeZH7II9i1POrr7C` |
| Outbound Cold Calling | $499/mo | Recurring | `price_1TJ7WgIwmeZH7II9KC3r5Sm5` |
| Google Ads Management | $499/mo | Recurring | `price_1TJ7WhIwmeZH7II9LK7vLQ0p` |
| Social Media Content | $399/mo | Recurring | `price_1TJ7WiIwmeZH7II9QS9n9cCv` |
| Website Build | $3,000 | One-time | `price_1TJ7WiIwmeZH7II9NJLzuynW` |
| Custom Integration | $1,500 | One-time | `price_1TJ7WjIwmeZH7II9QYP6oBtD` |
| Staff Training | $250 | One-time | `price_1TJ7WkIwmeZH7II9G47If8ua` |
| Annual Audit | $1,500 | One-time | `price_1TJ7WkIwmeZH7II9wh2euyJP` |

### Webhook Endpoint

- **ID:** `we_1TJ7WlIwmeZH7II94ztn3inz`
- **URL:** `https://velocity-ai-webhooks.up.railway.app/webhook/stripe`
- **Secret:** stored in `.env` as `STRIPE_WEBHOOK_SECRET`
- **Events subscribed:**
  - `checkout.session.completed`
  - `customer.subscription.created`
  - `customer.subscription.updated`
  - `customer.subscription.deleted`
  - `invoice.paid`
  - `invoice.payment_failed`
  - `payment_intent.succeeded`
  - `payment_intent.payment_failed`
  - `customer.created`
  - `customer.updated`

---

## Files Created / Modified

| File | Change |
|------|--------|
| `.env` | Added `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` |
| `.env.example` | Added `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY` placeholders |
| `requirements.txt` | Added `stripe>=15.0` |
| `operations/stripe_integration.py` | **NEW** — Full integration module (StripeManager class) |
| `operations/webhook-server.py` | Updated Stripe webhook handler to use StripeManager |

### `stripe_integration.py` — Key Features

- **StripeManager class** with methods for:
  - Customer management (create, find, update)
  - Checkout sessions (combines setup deposit + subscription)
  - Payment links (shareable via email/SMS after discovery call)
  - Subscription management (create, upgrade/downgrade, add-ons, cancel, reactivate)
  - One-time payments (setup final fee on Day 14, invoicing for add-ons)
  - Webhook verification and event handling
- All price IDs mapped in `PRICE_IDS` dict for easy reference
- Singleton pattern via `get_manager()` for use across the app

---

## Typical Payment Flow

1. **Discovery call** (Cal.com) → Mitchell closes the deal
2. **Send payment link** → `sm.create_payment_link("professional")` generates a shareable URL
3. **Customer pays** → Stripe Checkout collects setup deposit ($2,500) + starts monthly subscription ($1,499/mo)
4. **Webhook fires** → `checkout.session.completed` triggers onboarding email sequence
5. **Day 14 go-live** → `sm.charge_setup_final(customer_id, "professional")` charges remaining $2,500
6. **Monthly billing** → Stripe auto-charges subscription; `invoice.paid` events logged
7. **If payment fails** → `invoice.payment_failed` event triggers notification

---

## Going Live Checklist

When ready to switch from test to production:

1. **Swap API keys** in `.env`:
   - Replace `pk_test_...` → `pk_live_...`
   - Replace `sk_test_...` → `sk_live_...`
2. **Re-create products and prices** in live mode (test products don't carry over)
   - Update all price IDs in `stripe_integration.py` PRICE_IDS dict
3. **Create a new webhook endpoint** pointing to the production URL
   - Update `STRIPE_WEBHOOK_SECRET` in `.env`
4. **Update the webhook URL** if the Railway deployment URL changes
5. **Enable Stripe Tax** if needed for Australian GST
6. **Set up Stripe Customer Portal** for self-serve card updates and invoice history
7. **Test one real transaction** with a small amount before going fully live

---

## Test Results

All 14 integration tests passed on 6 April 2026:

- Products: 17 Velocity AI products found
- Prices: 20 AUD prices active
- Customer: create + retrieve OK
- Subscription: create + retrieve + cancel OK
- Webhook: configured with 10 events
- Payment intent: create OK ($1,250 test charge)
