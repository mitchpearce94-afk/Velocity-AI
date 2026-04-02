# Velocity AI — Client Delivery Guide

> How to use these templates to deliver a CRM build in 2 weeks.

---

## Template System Overview

Every Velocity AI client build starts from a trade-specific template, not from scratch. This cuts the build time from weeks to days because 70% of the CRM is pre-configured before the kickoff call even happens.

### File Structure

```
templates/
├── 00-master-architecture.md   ← Universal CRM structure (every build inherits this)
├── 01-plumbing.md              ← Plumbers, gas fitters, drainers
├── 02-electrical.md            ← Electricians, solar, data/comms
├── 03-building.md              ← Builders, carpenters, renovators
├── 04-hvac.md                  ← Air conditioning, refrigeration
├── 05-landscaping.md           ← Landscapers, garden design
├── 06-painting.md              ← Painters, decorators
├── 07-roofing.md               ← Roofers, gutter installers
├── 08-concreting.md            ← Concreters, paving
└── DELIVERY-GUIDE.md           ← This file
```

### What Each Template Contains

1. **Categories** — Pre-built job types for the trade
2. **Statuses** — 4-phase workflow (Planning → Quoting → Delivery → Completion)
3. **Product Catalog** — Common materials, parts, and services with realistic pricing
4. **Labour Sections** — How work is broken down for quoting
5. **Billing Defaults** — Hourly rates, markup percentages, payment terms
6. **Checklist Templates** — Trade-specific quality and compliance checklists
7. **Dependency Rules** — Auto-add items triggered by job type
8. **Scope of Works** — Auto-generated text for quotes
9. **AI Voice Agent Script** — Ava's questions and qualifying logic for that trade
10. **Customisation Points** — What needs to change per client

---

## 2-Week Build Timeline

### Day 0: Client Signs Up (Automated)
- [ ] Payment confirmation email sent (auto)
- [ ] Intake form email sent 4 hours later (auto)
- [ ] Select trade template based on their business
- [ ] Fork template into client-specific config

### Day 1–2: Kickoff & Configuration
- [ ] Review completed intake form
- [ ] 30-min kickoff call with client
- [ ] Confirm which categories apply to their business
- [ ] Get their specific pricing (labour rates, materials markup)
- [ ] Get their team list (names, roles, email, phone)
- [ ] Get their service area
- [ ] Import their existing customer list (if any)

### Day 3–5: Core Build
- [ ] Set up Supabase project (database + auth)
- [ ] Deploy CRM app (Vercel)
- [ ] Load trade template data:
  - Categories
  - Statuses
  - Product catalog (with their pricing)
  - Checklist templates
  - Dependency rules
  - Billing settings
- [ ] Create staff accounts
- [ ] Configure roles and permissions
- [ ] Import customer data (CSV or manual)

### Day 6–8: Quoting & Automations
- [ ] Configure quote engine with their products and pricing
- [ ] Set up labour sections with their rates
- [ ] Build scope of works templates with their branding
- [ ] Configure quote PDF with their logo, address, licence number
- [ ] Set up email templates (quote sent, accepted, follow-up)
- [ ] Test full quote cycle: create → send → accept → convert to job

### Day 9–10: AI Voice Agent
- [ ] Configure Ava for their trade (using template script)
- [ ] Customise greeting with business name
- [ ] Add their FAQ (services, service area, hours, pricing ranges)
- [ ] Set up call routing (when to transfer to owner)
- [ ] Test inbound calls
- [ ] Configure post-call analysis fields
- [ ] Set up webhook for auto-booking (if Cal.com integrated)

### Day 11–12: Integrations & Testing
- [ ] Connect to their existing tools (Xero, MYOB, Google Calendar, etc.)
- [ ] Set up automated follow-up emails
- [ ] Test the full workflow end-to-end:
  - Lead comes in (call or form) → Pipeline deal created
  - Deal qualified → Job created
  - Job quoted → Quote sent to customer
  - Quote accepted → Job scheduled
  - Job completed → Invoice triggered
- [ ] Load test data and verify reports
- [ ] Fix any bugs or config issues

### Day 13: Training
- [ ] 1-hour hands-on training session with client
- [ ] Walk through: dashboard, creating jobs, quoting, scheduling
- [ ] Train on mobile access (phone/tablet)
- [ ] Record training session for their team
- [ ] Provide quick-reference guide

### Day 14: Go-Live
- [ ] Final review with client
- [ ] Switch DNS / go live (if custom domain)
- [ ] Activate AI voice agent on their number
- [ ] Send go-live email (auto)
- [ ] Collect second half of setup fee
- [ ] Start monthly subscription billing
- [ ] Schedule 1-week check-in call

---

## Client Customisation Checklist

Use this during the kickoff call to capture everything needed:

### Business Details
- [ ] Business name (legal + trading)
- [ ] ABN
- [ ] Address
- [ ] Phone number
- [ ] Email
- [ ] Website
- [ ] Logo (high-res)
- [ ] Licence number (QBCC, electrical licence, etc.)

### Services & Pricing
- [ ] Which categories from the template apply? (delete unused ones)
- [ ] Any additional categories needed?
- [ ] Their hourly rate (standard + after-hours)
- [ ] Their callout fee
- [ ] Their materials markup percentage
- [ ] Payment terms (COD, 7 days, 14 days, 30 days)
- [ ] Do they do progress payments? (builders, large projects)

### Team
- [ ] Staff list: name, email, phone, role
- [ ] Who gets admin access?
- [ ] Who needs mobile-only access?
- [ ] Apprentice rates (if applicable)

### Quoting
- [ ] Their top 20 most-quoted products/services (with their actual pricing)
- [ ] Preferred suppliers
- [ ] Quote template preferences (simple vs detailed)
- [ ] Terms and conditions text
- [ ] Any industry-specific compliance text needed

### AI Voice Agent
- [ ] Business name pronunciation
- [ ] Services to mention on calls
- [ ] Service area boundaries
- [ ] Business hours
- [ ] Emergency handling (do they do after-hours?)
- [ ] When to transfer to owner vs book callback
- [ ] Any common questions to add to FAQ

### Integrations
- [ ] Current accounting software (Xero, MYOB, QuickBooks)
- [ ] Current job management tool (to migrate from)
- [ ] Google Business Profile
- [ ] Social media accounts
- [ ] Existing customer list (format: CSV, spreadsheet, or from old system)

---

## Per-Trade Quick Reference

| Trade | Template | Typical Build Complexity | Key Differentiator |
|-------|----------|------------------------|-------------------|
| Plumbing | 01 | Medium | Hot water product catalog, gas compliance certs |
| Electrical | 02 | Medium-High | Solar/EV charging products, ECOC compliance, smoke alarm rules |
| Building | 03 | High | Progress payment stages, subcontractor management, council approvals |
| HVAC | 04 | Medium | Unit sizing, refrigerant handling, ARCTICK compliance |
| Landscaping | 05 | Medium | Design phase workflow, seasonal scheduling, materials by m² |
| Painting | 06 | Low-Medium | Per-room/per-m² quoting, colour management |
| Roofing | 07 | Medium | Weather holds, safety requirements, per-m² material costing |
| Concreting | 08 | Medium | Weather holds, curing periods, per-m² and per-m³ pricing |

### Build Complexity Notes
- **Low-Medium** (Painting): Simpler product catalog, fewer integrations, straightforward quoting
- **Medium** (Plumbing, HVAC, Landscaping, Roofing, Concreting): Standard complexity, good product catalog, some compliance requirements
- **Medium-High** (Electrical): Multiple sub-specialties (solar, data, security), heavy compliance
- **High** (Building): Multi-stage progress payments, subcontractor coordination, council/certification workflows, complex quoting with provisional sums

---

## Scaling Notes

As the client base grows, these templates will evolve:
- Track which customisations are common → fold them back into the template
- Build trade-specific onboarding forms (ask the right questions upfront)
- Create pre-built Ava configurations per trade (one-click voice agent setup)
- Build a template marketplace where clients can share checklists and product catalogs within their trade
- Eventually: self-service onboarding for Starter tier clients using these templates
