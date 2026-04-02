# Velocity AI — Plumbing CRM Template

> Inherits from: 00-master-architecture.md
> Trades: Plumbers, Gas Fitters, Drainers, Roofers (plumbing)

---

## Categories (Job Types)

| Category | Description |
|----------|-------------|
| General Plumbing | Tap repairs, toilet fixes, leak detection, general maintenance |
| Hot Water | System install, replacement, repairs (electric, gas, solar, heat pump) |
| Gas Fitting | Gas appliance install/service, gas leak detection, compliance certs |
| Drainage | Blocked drains, CCTV inspections, drain relining, stormwater |
| Renovation | Bathroom renos, kitchen plumbing, laundry fit-outs |
| New Build | Rough-in plumbing for new construction |
| Commercial | Body corp, restaurant, office building plumbing |
| Emergency | After-hours callouts, burst pipes, flooding |
| Backflow | Testing, installation, certification |
| Roofing/Gutters | Gutter replacement, downpipes, roof flashings, leak repairs |

---

## Statuses

### Planning Phase
- **New** — Lead/enquiry just received
- **Quoted by Phone** — Quick phone quote given (no formal quote)
- **Site Visit Booked** — Assessment visit scheduled
- **Site Visit Complete** — Assessed, ready to quote

### Quoting Phase
- **Quoting** — Formal quote being prepared
- **Quote Sent** — Sent to customer
- **Follow-Up** — Chasing customer response
- **Accepted** — Customer accepted quote

### Delivery Phase
- **Scheduled** — Job booked into the calendar
- **In Progress** — Work underway
- **Waiting on Materials** — Parts ordered, waiting for delivery
- **Waiting on Customer** — Need access, decision, or approval
- **Warranty/Recall** — Return visit for warranty work

### Completion Phase
- **Complete** — Work finished
- **Invoice Sent** — Invoice issued
- **Paid** — Payment received
- **Cancelled** — Job cancelled

---

## Product Catalog (Starter Items)

### Hot Water Systems
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Electric Storage 50L | Hot Water | $650 | $850 |
| Electric Storage 80L | Hot Water | $750 | $980 |
| Electric Storage 125L | Hot Water | $850 | $1,100 |
| Electric Storage 250L | Hot Water | $1,100 | $1,450 |
| Electric Storage 315L | Hot Water | $1,200 | $1,580 |
| Gas Storage 135L | Hot Water | $1,100 | $1,450 |
| Gas Storage 170L | Hot Water | $1,250 | $1,650 |
| Gas Continuous Flow 20L | Hot Water | $1,400 | $1,850 |
| Gas Continuous Flow 26L | Hot Water | $1,600 | $2,100 |
| Heat Pump 270L | Hot Water | $3,200 | $4,200 |
| Heat Pump 315L | Hot Water | $3,500 | $4,600 |
| Solar Hot Water (flat panel) | Hot Water | $3,800 | $5,000 |

### Common Parts & Materials
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Tempering Valve | Parts | $120 | $180 |
| Pressure Limiting Valve | Parts | $80 | $130 |
| Expansion Valve | Parts | $60 | $95 |
| Isolation Valve (15mm) | Parts | $15 | $30 |
| Isolation Valve (20mm) | Parts | $20 | $40 |
| Flexi Hose (pair) | Parts | $25 | $50 |
| P-Trap | Parts | $15 | $35 |
| S-Trap | Parts | $15 | $35 |
| Cistern Mechanism | Parts | $45 | $85 |
| Mixer Tap (standard) | Parts | $120 | $220 |

### Drainage
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| CCTV Drain Inspection | Service | $0 | $250 |
| Jet Blasting (per hour) | Service | $0 | $280 |
| Drain Relining (per metre) | Service | $80 | $180 |

### Flat-Rate Services
| Product | Category | Cost | Sell |
|---------|----------|------|------|
| Tap Washer Replacement | Service | $5 | $120 |
| Toilet Repair (cistern) | Service | $45 | $180 |
| Blocked Drain (basic) | Service | $0 | $180 |
| Gas Compliance Certificate | Service | $0 | $220 |
| Backflow Test | Service | $0 | $150 |

---

## Labour Sections

| Section | Description | Default Rate |
|---------|-------------|-------------|
| Call Out / Assessment | Travel + initial inspection | $0 (rolled into callout fee) |
| Rough-In | First fix — pipework before walls close | $95/hr |
| Fit-Off | Second fix — fixtures, appliances, connections | $95/hr |
| Drainage Works | Drain excavation, laying, backfill | $110/hr |
| Emergency/After-Hours | After 5pm and weekends | $150/hr |

---

## Billing Defaults

| Setting | Default Value |
|---------|--------------|
| Standard hourly rate | $95/hr |
| After-hours rate | $150/hr |
| Callout fee | $80 |
| Emergency callout fee | $150 |
| Parts markup | 40–60% |
| GST rate | 10% |
| Quote expiry | 30 days |
| Payment terms | Due on completion (residential), 14 days (commercial) |

---

## Checklist Templates

### Hot Water Replacement
- [ ] Isolate water supply
- [ ] Isolate gas/electrical supply
- [ ] Drain existing unit
- [ ] Remove old unit and dispose
- [ ] Install new unit (check manufacturer specs)
- [ ] Install tempering valve (if required)
- [ ] Install PTR valve and drain line
- [ ] Connect water (hot, cold, relief)
- [ ] Connect gas/electrical
- [ ] Test for leaks
- [ ] Check temperature at nearest tap (max 50°C)
- [ ] Commission and set thermostat
- [ ] Complete compliance certificate (gas)
- [ ] Clean up site
- [ ] Walk customer through operation
- [ ] Take completion photos

### Blocked Drain
- [ ] Assess blockage (customer interview)
- [ ] Locate access point
- [ ] CCTV inspection (if required)
- [ ] Clear blockage (machine/jet)
- [ ] Post-clear CCTV inspection
- [ ] Identify root cause
- [ ] Provide repair recommendation
- [ ] Clean up site
- [ ] Issue drain report to customer

### Bathroom Renovation
- [ ] Strip existing fixtures
- [ ] Remove existing pipework
- [ ] Rough-in hot/cold supply lines
- [ ] Rough-in drainage (floor waste, basin, toilet, shower)
- [ ] Pressure test pipework
- [ ] Waterproofing (coordinate with tiler)
- [ ] Fit-off basin and taps
- [ ] Fit-off toilet
- [ ] Fit-off shower mixer and head
- [ ] Fit-off bath (if applicable)
- [ ] Connect hot water
- [ ] Test all fixtures
- [ ] Final leak check
- [ ] Customer sign-off

---

## Dependency Rules (Auto-Add)

| When Job Category Is | Auto-Add Product | Qty | Notes |
|---------------------|------------------|-----|-------|
| Hot Water | Tempering Valve | 1 | Required by AS/NZS 3500 |
| Hot Water | PTR Valve | 1 | Pressure/temperature relief |
| Hot Water (Gas) | Gas Compliance Cert | 1 | Mandatory for gas work |
| Backflow | Backflow Test Tag | 1 | Required certification |
| Any Gas Work | Gas Compliance Cert | 1 | Mandatory |

---

## Scope of Works (Auto-Generated Text)

### Hot Water Replacement
> Supply and install [PRODUCT_NAME] hot water system to replace existing unit at [SITE_ADDRESS]. Works include removal and disposal of existing unit, installation of new system, connection of water supply (hot/cold), [gas connection and compliance certification / electrical connection], installation of tempering valve and PTR valve as required. All works completed in accordance with AS/NZS 3500 and local plumbing regulations. Includes commissioning, temperature check, and customer handover.

### Blocked Drain
> Attend site at [SITE_ADDRESS] to investigate and clear blocked drain. Works include CCTV drain inspection, mechanical/jet clearing of blockage, post-clear inspection, and drain condition report. Any additional repair works identified during inspection will be quoted separately.

---

## AI Voice Agent (Ava) — Plumbing Script Additions

### Key Questions Ava Asks
- "Can you describe the plumbing issue you're experiencing?"
- "Is this an emergency — like active flooding or a burst pipe?"
- "Is the property residential or commercial?"
- "Do you know approximately how old your hot water system is?" (if HW related)
- "Can you describe any visible leaks or water damage?"
- "What's the best time for us to come and have a look?"

### Ava Qualifying Logic
- Emergency (burst, flooding) → Flag as urgent, attempt immediate callback
- Hot water replacement → High-value lead, prioritise
- Blocked drain → Common job, can often quote range over phone
- Renovation enquiry → Book site visit, high-value
- General maintenance → Standard scheduling

---

## Customisation Points (Per Client)

When onboarding a plumbing client, customise:

1. **Their specific services** — Not all plumbers do gas, drainage, or roofing
2. **Their pricing** — Update product catalog with their actual supplier costs and sell prices
3. **Their suppliers** — Reece, Tradelink, Samios, Bunnings Trade, etc.
4. **Their service area** — Suburbs/postcodes for scheduling
5. **Their team** — Staff names, roles, colours
6. **Their business hours** — Standard and after-hours windows
7. **Their existing customers** — Import from previous system or spreadsheet
8. **Ava's greeting** — Business name, specific services offered
