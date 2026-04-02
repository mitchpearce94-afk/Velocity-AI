# Velocity AI — Landscaping CRM Template

> Inherits from: 00-master-architecture.md
> Trades: Landscapers, Garden Designers, Hardscapers, Irrigation Specialists

---

## Categories (Job Types)

| Category | Description |
|----------|-------------|
| Garden Design | Concept design, 3D rendering, plant selection, layout planning |
| Hardscaping | Paving, decking, retaining walls, pathways, patios, edging |
| Softscaping | Planting, turf laying, garden beds, mulching, soil preparation |
| Irrigation | System design, installation, controller setup, maintenance, drip systems |
| Outdoor Living | Pergolas, pavilions, fire pits, seating areas, water features |
| Pool Surrounds | Decking, paving around pools, landscape integration |
| Drainage | Grading, French drains, stormwater management, swale design |
| Maintenance | Lawn mowing, garden maintenance, seasonal clean-ups, mulch refresh |
| Tree Works | Tree removal, pruning, stump grinding, arborist assessment |
| Turf Installation | Turf supply and laying, soil preparation, establishment care |

---

## Statuses

### Design Phase
- **New** — Enquiry just received
- **Design Booked** — Initial design consultation scheduled
- **Design Complete** — Concept/plans created and presented
- **Design Approved** — Customer approved design and pricing

### Quoting Phase
- **Quote Being Prepared** — Formal quote being drafted
- **Quote Sent** — Quote delivered to customer
- **Follow-Up** — Chasing customer response on quote
- **Accepted** — Customer accepted quote and ready to proceed

### Delivery Phase
- **Scheduled** — Installation date booked in calendar
- **In Progress** — Work underway on site
- **Waiting on Materials** — Plants/materials ordered, delivery awaited
- **Waiting on Customer** — Need access, approval, or decision
- **Waiting on Weather** — Paused due to rain or unsuitable conditions
- **Establishment Phase** — Work complete, plant establishment period active

### Completion Phase
- **Complete** — All works finished
- **Invoice Sent** — Invoice issued to customer
- **Paid** — Payment received
- **Cancelled** — Job cancelled

---

## Product Catalog (Starter Items)

### Turf
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Warm Season Turf (premium, sq m) | Turf | $12 | $28 |
| Cool Season Turf (sq m) | Turf | $10 | $24 |
| Couch Grass (sq m) | Turf | $9 | $22 |
| Buffalo Grass (sq m) | Turf | $11 | $26 |
| Sir Walter (premium, sq m) | Turf | $14 | $32 |

### Hardscape Materials
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Boral Pavers 600x600 (per sq m) | Paving | $45 | $85 |
| Boral Pavers 400x400 (per sq m) | Paving | $48 | $90 |
| Decking Board (per linear m) | Decking | $35 | $70 |
| Retaining Wall Block (besser, per block) | Walls | $8 | $18 |
| Retaining Wall Block (timber sleeper, per m) | Walls | $25 | $55 |
| Natural Stone Pavers (per sq m) | Paving | $80 | $150 |
| Gravel (per tonne) | Surfacing | $45 | $85 |
| Mulch (per cubic metre) | Mulch | $55 | $110 |
| Garden Edging (steel, per linear m) | Edging | $12 | $25 |

### Plants & Soil
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Trees (medium, 45L pot) | Plants | $65 | $140 |
| Shrubs (large, 25L pot) | Plants | $28 | $65 |
| Shrubs (medium, 15L pot) | Plants | $18 | $42 |
| Perennials (5L pot) | Plants | $8 | $18 |
| Groundcover (tube stock) | Plants | $3 | $8 |
| Topsoil (per cubic metre) | Soil | $60 | $120 |
| Potting Mix (per cubic metre) | Soil | $80 | $160 |
| Compost (per cubic metre) | Soil | $90 | $175 |

### Irrigation
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Smart Irrigation Controller (WiFi) | Irrigation | $280 | $450 |
| Drip Line Kit (basic, per 100m) | Irrigation | $120 | $240 |
| Sprinkler Head (pop-up, each) | Irrigation | $8 | $18 |
| Solenoid Valve (each) | Irrigation | $45 | $95 |
| Soil Moisture Sensor (each) | Irrigation | $85 | $180 |
| Irrigation Design Service (per site) | Irrigation | $0 | $350 |

### Outdoor Living
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Pergola Kit (3x3m) | Outdoor Living | $450 | $950 |
| Pergola Kit (4x4m) | Outdoor Living | $650 | $1,400 |
| Fire Pit (metal, portable) | Outdoor Living | $120 | $280 |
| Built-in Seating (per linear m) | Outdoor Living | $180 | $380 |
| Water Feature (small, pump incl) | Outdoor Living | $280 | $650 |

### Services (Time-Based)
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Design Consultation (per hour) | Service | $0 | $150 |
| Site Survey & Measurement (per site) | Service | $0 | $250 |
| Lawn Mowing (per visit) | Service | $0 | $85 |
| Garden Maintenance (per visit) | Service | $0 | $120 |
| Mulch Refresh (per cubic metre) | Service | $55 | $130 |

---

## Labour Sections

| Section | Description | Default Rate |
|---------|-------------|-------------|
| Design Consultation | Initial meeting, concept, planning | $95/hr |
| Site Prep / Earthworks | Excavation, grading, soil prep, levelling | $110/hr |
| Hardscaping | Paving, retaining walls, decking installation | $120/hr |
| Softscaping | Planting, turf laying, garden bed prep | $105/hr |
| Irrigation Installation | Pipe laying, controller setup, testing | $115/hr |
| Tree Works / Removal | Felling, stump grinding, pruning | $140/hr |
| Clean-Up & Site Restoration | Site clean, waste removal, final tidy | $85/hr |

---

## Billing Defaults

| Setting | Default Value |
|---------|--------------|
| Standard hourly rate | $105/hr |
| Design consultation rate | $150/hr |
| Callout fee | $0 (rolled into design fee) |
| Day rate (labour) | $900/day (8 hours) |
| Materials markup | 50–70% |
| GST rate | 10% |
| Quote expiry | 30 days |
| Payment terms | Deposit 50% on acceptance, balance on completion |
| Establishment care period | 6–8 weeks post-install (sometimes included) |

---

## Checklist Templates

### Full Landscape Installation
- [ ] Design approved and signed off
- [ ] Site measured and marked
- [ ] Existing vegetation cleared (if applicable)
- [ ] Site graded and levels checked
- [ ] Soil testing (if required for plants)
- [ ] Drainage lines installed (if needed)
- [ ] Hardscape base prepared (compact, level)
- [ ] Paving/decking installed and levelled
- [ ] Retaining walls built (if applicable)
- [ ] Irrigation lines laid (trenched, tested)
- [ ] Irrigation controller installed and programmed
- [ ] Soil conditioner and compost applied
- [ ] Plants positioned and planted
- [ ] Turf laid and watered in
- [ ] Mulch applied to garden beds
- [ ] Edging installed
- [ ] Irrigation system commissioned (full pressure test)
- [ ] Site cleaned and waste removed
- [ ] Customer walk-through and handover
- [ ] Maintenance instructions provided
- [ ] Take completion photos
- [ ] Invoice issued

### Retaining Wall Installation
- [ ] Design and site plan confirmed
- [ ] Site marked and levels taken
- [ ] Excavation completed to design depth
- [ ] Base layer levelled and compacted
- [ ] Drainage rock placed behind wall line
- [ ] First course of blocks laid (level check)
- [ ] Wall built to height (level and plumb checks every course)
- [ ] Geotextile installed behind wall (if required)
- [ ] Backfill soil placed and compacted in layers
- [ ] Drainage outlet pipe installed
- [ ] Soil settled (24–48 hour wait for compaction)
- [ ] Top dressing and plants installed
- [ ] Site cleaned
- [ ] Customer sign-off

### Garden Maintenance Visit
- [ ] Inspect lawn condition and health
- [ ] Mow lawn (set height, edge, trim edges)
- [ ] Inspect and maintain garden beds
- [ ] Remove weeds from planting areas
- [ ] Check mulch coverage (top up if needed)
- [ ] Inspect irrigation system (heads clear, timers correct)
- [ ] Prune shrubs and deadhead flowers (as required)
- [ ] Remove dead leaves and debris
- [ ] Check for pest/disease issues
- [ ] Provide recommendations to customer
- [ ] Site cleaned and swept
- [ ] Log visit and note next scheduled maintenance

---

## Dependency Rules (Auto-Add)

| When Job Category Is | Auto-Add Product | Qty | Notes |
|---------------------|------------------|-----|-------|
| Hardscaping > 50 sq m | Gravel (base layer) | Calc | Base prep for paving |
| Turf Installation | Topsoil | Calc | 50–100mm depth typical |
| Planting | Soil Conditioner | Calc | Per plant bed area |
| Irrigation Install | Smart Controller | 1 | Essential for modern systems |
| Retaining Wall > 1m high | Geotextile | Calc | Drainage and stability |
| Garden Design | Site Survey Service | 1 | Required before design |
| Any Install | Clean-Up Service | 1 | Site restoration |

---

## Scope of Works (Auto-Generated Text)

### Full Landscape Installation
> Supply and install complete landscape at [SITE_ADDRESS] as per approved design. Works include site preparation and grading, [installation of paving/hardscape], [irrigation system design and installation], [planting of trees, shrubs, and groundcover], turf laying, application of mulch and soil conditioner, and site clean-up. All materials sourced and installed to industry standards. Irrigation system tested and commissioned. Customer to receive establishment care instructions and 8-week aftercare support. Completion subject to weather conditions.

### Hardscaping Works (Paving / Retaining Wall)
> Supply and install [paving / retaining wall] works at [SITE_ADDRESS]. Works include site excavation and preparation, base course laying and compaction, installation of [pavers / wall blocks] to design specification, backfill and compaction, and site clean-up. All materials supply and labour included. Completed to AS/NZS standards for structural stability and drainage.

### Irrigation System Installation
> Supply and design irrigation system at [SITE_ADDRESS] as per site plan. Works include trenching and pipe laying, installation of valve manifold and smart controller, connection to water main [or tank], installation of sprinkler/drip heads to coverage plan, full system pressure test, and controller programming. System ready for customer operation on completion.

---

## AI Voice Agent (Ava) — Landscaping Script Additions

### Key Questions Ava Asks
- "What type of landscaping work are you looking for — design, garden maintenance, paving, irrigation, or something else?"
- "Do you already have a design in mind, or are you starting from scratch?"
- "Approximately how large is the area you'd like landscaped?" (sq m or describe)
- "What's your budget range for this project?" (helps qualify leads)
- "When are you hoping to get the work done?" (timeline)
- "Have you had any landscaping done before at this property?"
- "Is the property residential or commercial?"
- "What's your preferred contact method — phone, email, or text?"

### Ava Qualifying Logic
- Garden design + large budget → High-value, book design consultation
- Lawn mowing/maintenance → Recurring revenue, schedule first visit
- Hardscaping/retaining walls → Medium-to-high value, book site visit
- Irrigation → Technical, may need site survey; schedule consultation
- Emergency tree removal → Check urgency, may fast-track
- Vague enquiry → Gather more info before scheduling
- Multiple services → Book comprehensive site visit

---

## Customisation Points (Per Client)

When onboarding a landscaping client, customise:

1. **Their service offerings** — Not all landscapers do design, irrigation, or tree works
2. **Their pricing** — Update plant prices (seasonal), labour rates, material markups
3. **Their suppliers** — Boral, Austral Turf, Ozbreed, local nurseries, soil suppliers
4. **Their service area** — Suburbs/postcodes they operate in
5. **Their team** — Staff names, roles, colours, equipment (mowers, bobcats, etc.)
6. **Their design capability** — In-house designer, software used (CAD, SketchUp), or referral-based
7. **Their plant library** — Preferred natives, water-wise varieties, local climate zone
8. **Their pricing model** — Hourly labour, day rates, fixed quotes, or hybrid
9. **Their existing customers** — Import customer base, maintenance schedules
10. **Ava's greeting** — Business name, specialties (e.g., "We do full landscape design and installation")
11. **Seasonal adjustments** — Planting seasons, irrigation timing, mowing schedules
12. **Warranty/aftercare** — Plant guarantee period, establishment visits, maintenance packages
