# Velocity AI — Pricing & Payment Structure

**Version:** 2.0
**Date:** April 2026
**Status:** Draft for Mitchell's review

---

## Pricing Philosophy

We're not selling software. We're selling a done-for-you AI operations build that replaces 3-4 different tools and agencies. The pricing needs to reflect that — but it also needs to feel accessible to a tradie who's never spent more than $50/mo on Tradify.

The structure below uses a **setup fee + monthly recurring** model. The setup fee covers the build. The monthly covers the platform, AI, and ongoing support. This is important because:

1. The setup fee qualifies serious buyers (filters out tyre-kickers)
2. The monthly recurring builds predictable, compounding revenue
3. Together they create high LTV with immediate cash flow

---

## Tier Structure

### Tier 1: Starter
**Who it's for:** Owner-operators and small teams (1-3 staff) who are drowning in admin and missing calls. They need the basics automated.

| Component | Price |
|-----------|-------|
| Setup Fee | $2,500 (one-time) |
| Monthly | $699/mo |
| Annual (paid upfront, 10% off) | $7,549/yr ($629/mo effective) |

**What's included:**
- AI Voice Agent (Ava) — inbound call answering, lead qualification, appointment booking (up to 200 minutes/mo)
- Basic CRM — customer records, job history, notes
- Automated quote follow-up — 5-email nurture sequence
- Google review request automation
- 1x onboarding session (60 mins)
- Email + chat support

**What it costs us to deliver:**
- Retell AI: ~$40/mo (200 mins)
- Claude API: ~$20/mo
- Infrastructure: ~$10/mo
- Support overhead: ~$30/mo
- **Total COGS: ~$100/mo → 86% gross margin**

---

### Tier 2: Professional
**Who it's for:** Growing teams (4-10 staff) who need proper scheduling, quoting, and team management. This is the sweet spot — highest volume tier.

| Component | Price |
|-----------|-------|
| Setup Fee | $5,000 (one-time) |
| Monthly | $1,499/mo |
| Annual (paid upfront, 10% off) | $16,189/yr ($1,349/mo effective) |

**What's included:**
Everything in Starter, plus:
- AI Voice Agent — inbound + outbound (up to 500 minutes/mo)
- Full CRM with pipeline management
- Automated quoting system — quote wizard with branded PDF output
- Smart scheduling — drag-and-drop, real-time team sync
- Marketing automation — seasonal campaigns, re-engagement, service reminders
- Business dashboard — live KPIs, revenue tracking, quote conversion
- 3x onboarding sessions (60 mins each)
- Priority email + phone support
- Monthly strategy check-in call

**What it costs us to deliver:**
- Retell AI: ~$100/mo (500 mins)
- Claude API: ~$50/mo
- Infrastructure: ~$20/mo
- Support + strategy call: ~$80/mo
- **Total COGS: ~$250/mo → 83% gross margin**

---

### Tier 3: Enterprise
**Who it's for:** Multi-team operations (10+ staff) running complex workflows across multiple locations or divisions. They need the full platform with custom integrations.

| Component | Price |
|-----------|-------|
| Setup Fee | $10,000 (one-time) |
| Monthly | $2,499/mo |
| Annual (paid upfront, 10% off) | $26,989/yr ($2,249/mo effective) |

**What's included:**
Everything in Professional, plus:
- AI Voice Agent — unlimited minutes
- Multi-location support
- Custom integrations (accounting software, supplier portals, etc.)
- Advanced reporting — per-team, per-location, per-trade breakdowns
- Automated compliance workflows (certificates, council submissions)
- Subcontractor management module
- Dedicated account manager (Mitchell initially)
- Weekly strategy calls
- Custom feature development (within reason)

**What it costs us to deliver:**
- Retell AI: ~$200/mo (heavy usage)
- Claude API: ~$100/mo
- Infrastructure: ~$40/mo
- Support + account management: ~$200/mo
- **Total COGS: ~$540/mo → 78% gross margin**

---

## Add-Ons (Any Tier)

These are upsells offered during onboarding or strategy calls. They expand ARPU without requiring a full tier upgrade.

| Add-On | Price | Cost | Margin |
|--------|-------|------|--------|
| Extra AI voice minutes (per 100 mins) | $99/mo | ~$20 | 80% |
| Outbound cold calling campaigns (Ava) | $499/mo | ~$80 | 84% |
| Website build (SEO-optimised, mobile-first) | $3,000 one-time | ~$200 (our time) | 93% |
| Google Ads management | $499/mo + ad spend | ~$100 | 80% |
| Social media content (4 posts/week) | $399/mo | ~$50 (AI-generated) | 87% |
| Custom integration (per integration) | $1,500 one-time | ~$300 | 80% |
| Staff training session (additional) | $250/session | ~$50 (time) | 80% |
| Annual system audit + optimisation | $1,500/yr | ~$200 | 87% |

---

## Revenue Per Client Modelling

### Average Revenue Per Client (ARPC)

Based on the tier mix and add-on uptake we'd realistically expect:

| Metric | Conservative | Realistic | Aggressive |
|--------|-------------|-----------|------------|
| Tier mix (Starter/Pro/Enterprise) | 50/40/10 | 35/50/15 | 25/55/20 |
| Average setup fee | $3,750 | $5,100 | $6,250 |
| Average monthly recurring | $1,099 | $1,449 | $1,699 |
| Average add-on revenue/mo | $100 | $250 | $400 |
| **Total avg monthly per client** | **$1,199** | **$1,699** | **$2,099** |
| **LTV (24 months, 5% churn)** | **$22,531** | **$32,481** | **$40,231** |
| Avg COGS per client/mo | $175 | $250 | $350 |
| **Gross margin per client** | **85%** | **85%** | **83%** |

---

## Payment Capture Flow

### How Payment Works End-to-End

```
Discovery Call (Mitchell closes)
        ↓
Send Stripe Payment Link (setup fee — 50% upfront)
        ↓
Client pays → Triggers onboarding sequence:
  • Welcome email from Ava
  • Intake form (Google Form or Typeform)
  • Cal.com link for onboarding session
        ↓
Build begins (2-week window)
        ↓
Build complete → Send Stripe Payment Link (remaining 50% setup)
        ↓
Client pays → Monthly subscription starts:
  • Stripe subscription (auto-billing on 1st of each month)
  • Payment receipt sent automatically
  • Failed payment → automatic retry + email notification
        ↓
Ongoing: Monthly billing via Stripe
  • Card on file, auto-charged
  • Annual prepay option offered at Month 3
```

### Stripe Setup Required

1. **Stripe Account** — Create at stripe.com (Australian entity, AUD)
2. **Products to create in Stripe:**
   - Starter Setup ($2,500 or $1,250 × 2 payments)
   - Professional Setup ($5,000 or $2,500 × 2 payments)
   - Enterprise Setup ($10,000 or $5,000 × 2 payments)
   - Starter Monthly ($699/mo recurring)
   - Professional Monthly ($1,499/mo recurring)
   - Enterprise Monthly ($2,499/mo recurring)
   - Starter Annual ($7,549/yr recurring)
   - Professional Annual ($16,189/yr recurring)
   - Enterprise Annual ($26,989/yr recurring)
   - Each add-on as a separate product
3. **Payment Links** — One per product, shareable via email/SMS
4. **Customer Portal** — Enable so clients can update cards, view invoices
5. **Webhook** — Stripe → our system for payment confirmations, failed payments

### Invoice Structure

**Setup Invoice (sent after discovery call close):**
```
Velocity AI — [Tier] Operations Build
─────────────────────────────────────
AI Operations System Build (50% deposit)    $X,XXX
─────────────────────────────────────
Total Due:                                  $X,XXX
Payment Terms: Due on receipt
```

**Monthly Invoice (auto-generated by Stripe):**
```
Velocity AI — Monthly Platform
─────────────────────────────────────
[Tier] Plan — [Month Year]                  $X,XXX
[Add-on, if applicable]                     $XXX
─────────────────────────────────────
Total:                                      $X,XXX
Billed to: Visa ending 4242
```

---

## Financial Impact (Updated Forecast)

Using the realistic tier mix (35% Starter / 50% Pro / 15% Enterprise):

| Month | New Clients | Active | Setup Revenue | MRR | Add-Ons | Total Monthly |
|-------|-------------|--------|---------------|-----|---------|---------------|
| 1 (Apr) | 1 | 1 | $5,100 | $1,449 | $250 | $6,799 |
| 3 (Jun) | 3 | 6 | $15,300 | $8,694 | $1,500 | $25,494 |
| 6 (Sep) | 4 | 15 | $20,400 | $21,735 | $3,750 | $45,885 |
| 9 (Dec) | 2 | 22 | $10,200 | $31,878 | $5,500 | $47,578 |
| 12 (Mar) | 5 | 30 | $25,500 | $43,470 | $7,500 | $76,470 |

| Metric | Year 1 Total |
|--------|-------------|
| Setup revenue | $188,700 |
| Monthly recurring | $300,000 |
| Add-on revenue | $54,000 |
| **Total revenue** | **$542,700** |
| Total COGS | ~$60,000 |
| **Gross profit** | **$482,700** |
| **Gross margin** | **89%** |

*Note: This is more conservative than the original $668K forecast because the tier structure is more nuanced. But the margins are more accurate because we've modelled real costs.*

---

## Pricing Objections & Responses

**"$699/mo is too much for software"**
→ "It's not software — it's your entire operations system, built and managed for you. Compare that to hiring a receptionist ($4K/mo), a marketing agency ($2K/mo), and buying a CRM ($200/mo). You're getting all three for $699."

**"Why is there a setup fee?"**
→ "Because we're building this specifically for your business — your products, your pricing, your workflow. It's not a template. The setup fee covers 2 weeks of dedicated build time, and you don't pay the second half until you're happy with it."

**"Can I just get the AI phone agent?"**
→ "We could do that as a standalone, but you'd be missing the system that makes it valuable. The AI books the job — but where does it go? The CRM catches it, the scheduler assigns it, the follow-up happens automatically. The phone agent without the system is like hiring a receptionist with no desk."

**"My mate pays $49/mo for ServiceM8"**
→ "And he's still doing admin at 9pm, right? ServiceM8 is a job management tool. We're building an AI-powered operations engine that runs your business while you're on the tools. Different category entirely."

---

## Recommended Next Steps

1. **Mitchell to create Stripe account** (stripe.com.au)
2. **Sage builds the Stripe products and payment links**
3. **Wire payment confirmation into onboarding automation**
4. **Update one-pager and website with new pricing**
5. **Update discovery call script close section with new pricing**
6. **Test the full payment → onboarding flow end-to-end**
