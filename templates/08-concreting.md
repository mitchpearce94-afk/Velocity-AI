# Velocity AI — Concreting CRM Template

> Inherits from: 00-master-architecture.md
> Trades: Concreters, Concrete Finishers, Excavation & Concreting Specialists

---

## Categories (Job Types)

| Category | Description |
|----------|-------------|
| Driveways | Concrete driveway pour, resurfacing, repairs |
| Paths & Walkways | Concrete pathways, garden paths, entrance areas |
| Concrete Slabs | Foundation slabs, garage floors, storage shed bases |
| Pool Surrounds | Concrete decking around pools, slip-resistant finishes |
| Exposed Aggregate | Decorative concrete with pebbles/gravel exposed |
| Coloured Concrete | Concrete with integral colour pigments or acid stains |
| Polished Concrete | Grinding and polishing for decorative finish |
| Retaining Walls | Concrete block retaining walls, reinforced structures |
| Commercial Concrete | Large-scale pours, car parks, industrial floors |
| Concrete Repairs | Patch repairs, crack filling, surface restoration |

---

## Statuses

### Planning Phase
- **New** — Lead/enquiry just received
- **Quoted by Phone** — Quick phone quote given (no formal quote)
- **Site Visit Booked** — Inspection scheduled
- **Site Visit Complete** — Soil assessment, measurements, ready to quote

### Quoting Phase
- **Quoting** — Formal quote being prepared
- **Quote Sent** — Sent to customer
- **Follow-Up** — Chasing customer response
- **Accepted** — Customer accepted quote

### Delivery Phase
- **Scheduled** — Job booked into the calendar
- **Excavation** — Site prep, formwork, base preparation underway
- **In Progress** — Concrete pour and finishing underway
- **Curing** — Concrete setting (7–14 days, weather dependent)
- **Waiting on Materials** — Concrete truck or supplies on order
- **Waiting on Customer** — Access, approval, or payment before proceeding
- **Weather Hold** — Work paused due to rain/excessive heat
- **Warranty/Recall** — Return visit for surface defects

### Completion Phase
- **Complete** — Work finished, curing underway
- **Invoice Sent** — Invoice issued
- **Paid** — Payment received
- **Cancelled** — Job cancelled

---

## Product Catalog (Starter Items)

### Concrete Supply
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Standard Concrete (per m³) | Concrete | $280 | $380 |
| Reinforced Concrete (per m³) | Concrete | $310 | $410 |
| Exposed Aggregate Concrete (per m³) | Concrete | $350 | $480 |
| Coloured Concrete (per m³) | Concrete | $320 | $450 |
| Polished Concrete (per m²) | Concrete | $0 | $45 |

### Reinforcement & Formwork
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Steel Reinforcing Mesh (per m²) | Materials | $8 | $16 |
| Steel Reinforcing Bar 12mm (per metre) | Materials | $1.50 | $3.50 |
| Steel Reinforcing Bar 16mm (per metre) | Materials | $2.50 | $5.50 |
| Timber Formwork (per m²) | Materials | $12 | $25 |
| Plastic Formwork Edge (per metre) | Materials | $6 | $14 |

### Additives & Finishes
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Concrete Colour Oxide (per kg) | Additives | $18 | $38 |
| Concrete Sealer (per litre) | Additives | $24 | $52 |
| Slip-Resistant Coating (per litre) | Additives | $35 | $75 |
| Anti-stain Concrete Treatment (per litre) | Additives | $28 | $60 |
| Acid Stain (per litre) | Additives | $45 | $95 |

### Gravel & Base Materials
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Crushed Rock Base (per m³) | Base | $50 | $85 |
| Gravel for Exposure (per m³) | Base | $75 | $120 |
| Sand (per m³) | Base | $40 | $65 |

### Polishing & Grinding Supplies
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Diamond Grinding Pad (per set) | Equipment | $120 | $250 |
| Concrete Grind & Polish (per m²) | Service | $0 | $55 |

### Flat-Rate Services
| Product | Category | Cost | Sell |
|---------|----------|------|------|
| Site Inspection & Quote Prep | Service | $0 | $150 |
| Concrete Crack Repair | Service | $0 | $180 |
| Surface Cleanup & Sealing | Service | $0 | $35/m² |

---

## Labour Sections

| Section | Description | Default Rate |
|---------|-------------|-------------|
| Excavation & Prep | Digging, levelling, compacting base | $95/hr |
| Formwork | Building and setting forms for pour | $110/hr |
| Reinforcement | Laying mesh, tying rebar | $105/hr |
| Concrete Pour | Pouring concrete, spreading, initial levelling | $120/hr |
| Finishing (Trowel) | Screeding, trowelling, smoothing | $115/hr |
| Finishing (Broom) | Broom finish for slip resistance | $95/hr |
| Finishing (Exposed Aggregate) | Exposing aggregate, water-washing | $130/hr |
| Finishing (Polishing) | Grinding and polishing concrete | $140/hr |
| Sealing & Coating | Applying sealer or decorative coats | $105/hr |
| Cleanup & Site Restoration | Debris removal, site cleaning | $85/hr |

---

## Billing Defaults

| Setting | Default Value |
|---------|--------------|
| Standard hourly rate | $95/hr |
| Labour rate (formwork) | $110/hr |
| Labour rate (finishing) | $115/hr |
| Concrete supply + pour | Per m³ (typically $380–$480 depending on type) |
| Per m² billing | $65–$85/m² (labour inclusive, common for driveways) |
| Callout fee | $120 |
| Parts markup | 50–75% |
| GST rate | 10% |
| Quote expiry | 30 days |
| Payment terms | 50% deposit on acceptance, balance on completion |

---

## Checklist Templates

### Driveway Pour
- [ ] Mark out and measure driveway area
- [ ] Excavate and remove topsoil
- [ ] Compact subgrade (check fall/drainage)
- [ ] Install formwork (boards, levels, correct fall)
- [ ] Inspect formwork for accuracy
- [ ] Lay base layer (crushed rock, compact)
- [ ] Lay reinforcing mesh (overlap per spec)
- [ ] Tie mesh at intersections
- [ ] Confirm concrete delivery time (usually morning)
- [ ] Place concrete delivery area
- [ ] Pour concrete in sections
- [ ] Spread and level concrete
- [ ] Remove air pockets (vibration or tapping)
- [ ] Screeding (strike off excess)
- [ ] First trowelling
- [ ] Broom finish for slip resistance
- [ ] Control joint cuts (every 2–3m)
- [ ] Remove formwork (after 24–48 hrs)
- [ ] Apply sealer (after 7–10 days curing)
- [ ] Site cleanup
- [ ] Customer handover with curing instructions

### Concrete Slab (Shed/Garage Base)
- [ ] Site marking and measurement
- [ ] Excavate to required depth (100–150mm typically)
- [ ] Compact subgrade
- [ ] Install edge formwork
- [ ] Lay crushed rock base (50mm)
- [ ] Compact base
- [ ] Lay reinforcing mesh
- [ ] Confirm correct fall (if outdoor)
- [ ] Concrete pour
- [ ] Level and spread concrete
- [ ] Trowel finish to required smoothness
- [ ] Control joints every 2–3m
- [ ] Allow curing (7 days minimum before loading)
- [ ] Apply sealer (optional, recommended for exposure)
- [ ] Site cleanup

### Exposed Aggregate Driveway
- [ ] Excavate and prepare base
- [ ] Install formwork
- [ ] Lay reinforcing mesh
- [ ] Pour exposed aggregate concrete
- [ ] Initial levelling
- [ ] Light trowel (minimal smoothing)
- [ ] Wait 4–6 hours (concrete surface hardens)
- [ ] Water wash to expose aggregate (gentle spray)
- [ ] Light brushing to clear dust
- [ ] Allow drying and inspect exposure
- [ ] Additional wash if needed
- [ ] Sealer application (after 7 days)
- [ ] Site cleanup

### Pool Surround (Slip-Resistant Finish)
- [ ] Mark out pool surround area (minimum 1.5m clearance)
- [ ] Excavate and compact subgrade
- [ ] Install formwork (level, follows pool edge)
- [ ] Lay base and reinforcing mesh
- [ ] Pour concrete
- [ ] Initial levelling and spread
- [ ] Trowel to smooth finish
- [ ] Add slip-resistant coating (broadcast before concrete hardens or seal after)
- [ ] Control joints around pool perimeter
- [ ] Allow 7-day cure before pool fill
- [ ] Final sealing with pool-safe sealer
- [ ] Site cleanup and removal of formwork

### Concrete Crack Repair
- [ ] Assess crack (active, dormant, structural)
- [ ] Clean crack (remove debris, dust)
- [ ] Apply concrete crack filler or epoxy
- [ ] Trowel smooth
- [ ] Sand if necessary (for sealable finish)
- [ ] Apply sealer
- [ ] Inspect for complete fill
- [ ] Advise customer on cause and prevention

---

## Dependency Rules (Auto-Add)

| When Job Category Is | Auto-Add Product | Qty | Notes |
|---------------------|------------------|-----|-------|
| Any Concrete Pour | Crushed Rock Base | 1 per 5m² | 50mm minimum depth |
| Any Concrete Pour | Steel Reinforcing Mesh | 1 per 10m² | Standard reinforcement |
| Driveway | Concrete Sealer | 1 per 20m² | Post-cure protection recommended |
| Exposed Aggregate | Gravel for Exposure | 1 per 10m² | Pebbles embedded in concrete |
| Coloured Concrete | Concrete Colour Oxide | 1 per 2m³ | Colour pigment for batch |
| Pool Surround | Slip-Resistant Coating | 1 per 10m² | Safety requirement for wet areas |
| Any Large Pour | Excavation Labour | hourly rate | Base prep and site setup |

---

## Scope of Works (Auto-Generated Text)

### Concrete Driveway
> Supply and install concrete driveway at [SITE_ADDRESS] measuring approximately [LENGTH]m x [WIDTH]m. Works include site excavation and preparation, removal of topsoil, compaction of subgrade, installation of formwork to correct levels and fall, laying of reinforcing mesh, supply and pouring of [TYPE] concrete, screeding and trowelling finish, installation of control joints, application of [slip-resistant broom finish / polished finish / sealer as applicable]. Driveway cured for 7 days before use. All works completed in accordance with AS 3600 (Concrete Structures). Includes site cleanup and customer handover.

### Pool Surround
> Supply and install concrete pool surround at [SITE_ADDRESS]. Works include excavation and preparation of 1.5m perimeter around pool, installation of formwork, laying of reinforcing mesh, supply and pour of [slip-resistant / standard] concrete, trowelling to smooth finish, application of pool-safe sealer, and slip-resistant coating for wet area safety. Concrete allowed 7-day cure before pool commissioning. All materials and workmanship comply with pool safety standards and AS 3600.

### Exposed Aggregate Driveway
> Supply and install decorative exposed aggregate concrete driveway at [SITE_ADDRESS]. Works include site excavation and base preparation, installation of formwork, laying of reinforcing mesh, supply and pouring of exposed aggregate concrete blend, water-washing and brushing to expose decorative pebbles, and sealing with protective coating. Final finish provides both decorative appeal and slip-resistant surface. Cured for 7 days before use.

---

## AI Voice Agent (Ava) — Concreting Script Additions

### Key Questions Ava Asks
- "Can you describe the concrete project you're interested in — driveway, path, pool surround, or something else?"
- "What's the approximate size or area needing concrete?"
- "Is the ground level, sloping, or uneven?"
- "Do you have a specific finish in mind — smooth, broom finish, exposed aggregate, or decorative?"
- "Is weather a concern? (Rain forecast, hot weather — this impacts scheduling)"
- "Do you need excavation work, or is the base prepared?"
- "What's your timeline — are you looking to start within the next 2 weeks?"

### Ava Qualifying Logic
- Large pour (>20 m²) → High-value lead, book site visit
- Driveway or pool surround → Standard lead, high conversion
- Decorative (exposed aggregate, polished) → Premium pricing, upsell opportunity
- Exposed to weather/rain → Requires weather assessment, schedule carefully
- Site prep needed → Additional labour cost, book site visit
- Small repair work → Often quote over phone if simple
- Commercial (car park, large slab) → Escalate to senior staff, complex logistics

---

## Customisation Points (Per Client)

When onboarding a concreting client, customise:

1. **Their specific services** — Not all concreters do polishing, exposed aggregate, or commercial work
2. **Their pricing** — Update product catalog with their actual concrete supplier and labour rates
3. **Their suppliers** — Local concrete suppliers, reinforcing suppliers, sealer manufacturers
4. **Their service area** — Suburbs/postcodes (concrete trucks have limited range, typically 30–50km)
5. **Their team** — Staff names, roles, colours
6. **Their business hours** — Standard hours (concrete pours must occur during daylight)
7. **Their warranty policy** — Workmanship warranty duration (typically 2–3 years for surface)
8. **Weather protocols** — How they handle rain, extreme heat, frost risk
9. **Concrete suppliers** — Primary concrete supplier, minimum order quantities
10. **Their existing customers** — Import from previous system
11. **Ava's greeting** — Business name, specific concreting services offered
