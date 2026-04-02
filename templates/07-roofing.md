# Velocity AI — Roofing CRM Template

> Inherits from: 00-master-architecture.md
> Trades: Roofers, Roof Restorers, Gutter Specialists

---

## Categories (Job Types)

| Category | Description |
|----------|-------------|
| Metal Roofing | Colorbond or zinc-aluminium roofing install, replacement, re-roofing |
| Tile Roofing | Concrete/ceramic tile roof install, repair, replacement |
| Roof Restoration | Cleaning, recoating, re-waterproofing existing roofs |
| Gutters & Downpipes | Gutter replacement, downpipe install, leaf guards, cleanout |
| Skylights | Skylight install, repair, replacement, flashings |
| Roof Insulation | Glasswool, polyester batts, foam installation between rafters |
| Leak Repairs | Roof leak detection, flashing repair, pointing, temporary tarping |
| Re-Roofing | Full roof removal and replacement (existing structure retained) |
| Fascia & Soffit | Fascia boards, soffit lining, guttering coordination |
| Commercial Roofing | Large-scale installs, membrane roofing, industrial applications |

---

## Statuses

### Planning Phase
- **New** — Lead/enquiry just received
- **Quoted by Phone** — Quick phone quote given (no formal quote)
- **Site Visit Booked** — Roof inspection scheduled
- **Site Visit Complete** — Assessed, ready to quote

### Quoting Phase
- **Quoting** — Formal quote being prepared
- **Quote Sent** — Sent to customer
- **Follow-Up** — Chasing customer response
- **Accepted** — Customer accepted quote

### Delivery Phase
- **Scheduled** — Job booked into the calendar
- **In Progress** — Work underway (roof removal, new install)
- **Waiting on Materials** — Colorbond, tiles, gutters on order
- **Waiting on Customer** — Access issue, approval, or payment before proceeding
- **Weather Hold** — Work paused due to rain/wind forecasts
- **Warranty/Recall** — Return visit for defects or warranty work

### Completion Phase
- **Complete** — Work finished
- **Invoice Sent** — Invoice issued
- **Paid** — Payment received
- **Cancelled** — Job cancelled

---

## Product Catalog (Starter Items)

### Colorbond Roofing
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Colorbond Sheet (per m²) | Metal Roofing | $35 | $65 |
| Colorbond Flashing Kit | Metal Roofing | $180 | $320 |
| Fasteners & Sealant (per 100) | Metal Roofing | $45 | $95 |
| Ridge Cap (per metre) | Metal Roofing | $28 | $55 |

### Tile Roofing
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Concrete Roof Tiles (per m²) | Tile Roofing | $22 | $45 |
| Ceramic Roof Tiles (per m²) | Tile Roofing | $45 | $85 |
| Tile Adhesive & Bedding (per bag) | Tile Roofing | $18 | $35 |
| Ridge Tiles (per metre) | Tile Roofing | $25 | $50 |

### Guttering & Downpipes
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Colorbond Gutter (per metre) | Gutters | $18 | $40 |
| Aluminium Gutter (per metre) | Gutters | $15 | $35 |
| Downpipe 100mm (per metre) | Gutters | $12 | $28 |
| Downpipe 150mm (per metre) | Gutters | $18 | $38 |
| Gutter Guard/Leaf Guard (per metre) | Gutters | $22 | $50 |
| Gutter Brackets & Fixings (per 10) | Gutters | $25 | $55 |

### Flashings & Sealing
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Roof Flashing (per unit) | Flashings | $35 | $75 |
| Chimney Flashing Kit | Flashings | $120 | $250 |
| Roof Penetration Flashing | Flashings | $45 | $95 |
| Polyurethane Sealant (per 600ml) | Flashings | $12 | $28 |

### Insulation
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Glasswool Batts (per m²) | Insulation | $8 | $18 |
| Polyester Batts (per m²) | Insulation | $12 | $25 |
| Roof Membrane (per m²) | Insulation | $15 | $35 |

### Roof Restoration
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Roof Cleaning (per m²) | Service | $0 | $15 |
| Roof Coating (per litre) | Service | $28 | $60 |
| Pointing & Bedding (per metre) | Service | $0 | $35 |

### Skylights
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Fixed Skylight 600x600mm | Skylights | $180 | $380 |
| Opening Skylight 600x600mm | Skylights | $250 | $520 |
| Motorised Skylight 600x600mm | Skylights | $450 | $950 |
| Skylight Flashing Kit | Skylights | $75 | $160 |

### Flat-Rate Services
| Product | Category | Cost | Sell |
|---------|----------|------|------|
| Roof Inspection & Report | Service | $0 | $180 |
| Gutter Cleaning | Service | $0 | $140 |
| Minor Leak Repair | Service | $0 | $220 |
| Temporary Tarping (per m²) | Service | $0 | $25 |

---

## Labour Sections

| Section | Description | Default Rate |
|---------|-------------|-------------|
| Roof Assessment & Inspection | Site inspection, measurements, condition report | $0 (rolled into callout fee) |
| Roof Removal | Strip existing roof, remove debris | $65/m² |
| Installation (Metal) | Install Colorbond, flashings, guttering | $45/m² |
| Installation (Tile) | Lay and bed tiles, ridge caps | $55/m² |
| Guttering & Downpipes | Install or replace gutters, downpipes, brackets | $85/hr |
| Flashing & Sealing | Install/repair flashings, seal penetrations | $110/hr |
| Roof Restoration | Cleaning, coating application | $35/m² |
| Fascia & Soffit | Install fascia boards, soffit lining | $75/hr |
| Safety Equipment | Scaffolding, harnesses, fall protection (if charged separately) | $120/hr |

---

## Billing Defaults

| Setting | Default Value |
|---------|--------------|
| Standard hourly rate | $95/hr |
| Removal labour rate | $65/m² |
| Installation labour rate (metal) | $45/m² |
| Installation labour rate (tile) | $55/m² |
| Callout fee | $100 |
| Parts markup | 50–75% |
| GST rate | 10% |
| Quote expiry | 30 days |
| Payment terms | 50% deposit on acceptance, balance on completion |

---

## Checklist Templates

### New Metal Roof Installation
- [ ] Safety equipment in place (scaffolding, harnesses, signs)
- [ ] Remove existing roof and dispose
- [ ] Inspect and repair roof frame/trusses (if needed)
- [ ] Install roof membrane/underlayment
- [ ] Install flashings at penetrations and edges
- [ ] Install Colorbond sheets (start from bottom)
- [ ] Secure fasteners per manufacturer spec (spacing, sealant)
- [ ] Install gutter and downpipes
- [ ] Install ridge caps
- [ ] Install fascia and soffit
- [ ] Check all penetrations for leaks (water test if possible)
- [ ] Clean site and remove debris
- [ ] Provide customer handover & maintenance notes
- [ ] Take completion photos

### Re-Roofing Existing Roof (Metal to Metal)
- [ ] Safety setup and site protection
- [ ] Remove old Colorbond sheets
- [ ] Inspect and repair timber, treat if needed
- [ ] Remove/replace damaged membrane
- [ ] Install new roof membrane
- [ ] Install new Colorbond sheets
- [ ] Install new flashings and gutters
- [ ] Final leak check
- [ ] Cleanup and debris removal
- [ ] Customer walkthrough

### Gutter Replacement
- [ ] Remove old gutters and downpipes
- [ ] Inspect and repair fascia boards
- [ ] Install new gutter profile (measure for correct fall)
- [ ] Install brackets at correct spacing (every 1.2–1.5m)
- [ ] Connect downpipes
- [ ] Install leaf guards (if specified)
- [ ] Test water flow
- [ ] Cleanup
- [ ] Invoice and closeout

### Roof Restoration (Clean & Coat)
- [ ] Safety setup on existing roof
- [ ] High-pressure clean (low PSI to avoid damage)
- [ ] Remove moss/algae and allow drying (24–48 hrs)
- [ ] Point and bed loose tiles or flashings
- [ ] Apply roof coating (first coat)
- [ ] Allow cure time per product specs
- [ ] Apply second coat (if required)
- [ ] Final inspection
- [ ] Cleanup
- [ ] Provide maintenance schedule to customer

---

## Dependency Rules (Auto-Add)

| When Job Category Is | Auto-Add Product | Qty | Notes |
|---------------------|------------------|-----|-------|
| Metal Roofing | Colorbond Flashing Kit | 1 | Essential for weatherproofing |
| Metal Roofing | Ridge Cap | 1 per 10m² | Running length depends on roof pitch/size |
| Tile Roofing | Tile Adhesive & Bedding | 1 per 50m² | Bedding mortar for tiles |
| Gutters & Downpipes | Gutter Brackets | 1 per 1.2m | Brackets needed every 1.2–1.5m |
| Gutters & Downpipes | Gutter Guard | 1 per 10m | Optional, popular upsell |
| Any Penetration Work | Roof Flashing | 1 per penetration | Chimneys, vents, skylights |
| Skylight Install | Skylight Flashing Kit | 1 | Required for weatherproofing |

---

## Scope of Works (Auto-Generated Text)

### Metal Roof Installation
> Supply and install Colorbond roofing to replace existing roof at [SITE_ADDRESS]. Works include removal and disposal of existing roof covering, inspection and repair of roof structure, installation of roof membrane, installation of Colorbond sheets with fasteners and sealant as per manufacturer specifications, installation of all flashings at penetrations and edges, installation of gutters and downpipes, installation of ridge caps and fascia. All works completed in accordance with AS/NZS 2394 (Wind loads) and local building codes. Includes inspection for water-tightness and customer handover.

### Gutter Replacement
> Remove and replace guttering and downpipes at [SITE_ADDRESS]. Works include removal of existing gutters and downpipes, inspection and repair of fascia boards where required, installation of new [TYPE] gutter profile with brackets at correct spacing and fall, installation of new downpipes, and [leaf guard installation if applicable]. All connections sealed and tested for water flow. Site cleaned and debris removed.

### Roof Restoration
> Provide professional cleaning, pointing, and protective coating to existing roof at [SITE_ADDRESS]. Works include high-pressure cleaning to remove moss and algae, inspection and pointing of tiles/flashings, application of roof coating (number of coats as specified), and 24-hour curing period between coats. Coating provides protection against UV damage and extends roof life by 5–10 years. Maintenance schedule provided to customer.

---

## AI Voice Agent (Ava) — Roofing Script Additions

### Key Questions Ava Asks
- "Can you describe the issue with your roof — is it leaking, damaged, or in need of maintenance?"
- "Is this an emergency situation like active leaking into your home?"
- "Approximately how old is your roof?"
- "What type of roofing material is currently on the roof — metal, tiles, or asphalt?"
- "Are you looking for repair, restoration, or full replacement?"
- "Is the property residential or commercial?"
- "What's the best time for us to come and inspect the roof?"

### Ava Qualifying Logic
- Emergency (active leak, damage) → Flag urgent, attempt same-day inspection
- Full replacement → High-value lead, book site visit immediately
- Gutter work → Medium value, can often quote range over phone if gutters only
- Restoration (cleaning/coating) → Standard scheduling, common job
- Minor repair → Quick assessment, often quote over phone
- Commercial property → Escalate to senior staff, larger scope

---

## Customisation Points (Per Client)

When onboarding a roofing client, customise:

1. **Their specific services** — Not all roofers do metal, tiles, gutters, or restoration
2. **Their pricing** — Update product catalog with their actual supplier costs and sell prices
3. **Their suppliers** — BlueScope (Colorbond), local tile suppliers, gutter fabricators
4. **Their service area** — Suburbs/postcodes (some roofers travel 50km+)
5. **Their team** — Staff names, roles, colours
6. **Their business hours** — Standard hours (roofing rarely after-hours)
7. **Their warranty policy** — Workmanship warranty duration (typically 3–5 years)
8. **Safety protocols** — Scaffolding requirements, fall protection standards
9. **Their existing customers** — Import from previous system
10. **Ava's greeting** — Business name, specific roofing services offered
