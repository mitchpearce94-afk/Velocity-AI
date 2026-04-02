# Velocity AI — Painting & Decorating CRM Template

> Inherits from: 00-master-architecture.md
> Trades: Painters, Decorators, Coating Specialists

---

## Categories (Job Types)

| Category | Description |
|----------|-------------|
| Interior Residential | Interior walls, ceilings, trim, feature walls, small spaces |
| Exterior Residential | Exterior walls, fascia, soffit, weatherboards, concrete, garage doors |
| Commercial | Office buildings, retail fit-outs, industrial facilities, schools |
| Strata/Body Corp | Multi-unit residential, common areas, building facades |
| New Build | New residential, paintwork on new construction pre-handover |
| Renovation | Kitchen/bathroom repaints, feature walls, heritage work, colour consults |
| Specialty Finishes | Epoxy floors, textured coatings, wallpaper, stone effects, murals |
| Roof Painting | Tile/metal roof paint, protective coatings, rust treatment |
| Furniture/Cabinetry | Furniture refinish, cabinet painting, doors, built-ins |

---

## Statuses

### Planning Phase
- **New** — Lead/enquiry just received
- **Phone Quote Given** — Quick phone quote provided (based on sq m estimate)
- **Site Visit Booked** — In-home assessment scheduled
- **Site Visit Complete** — Assessed, colour choices discussed, ready to quote

### Quoting Phase
- **Quoting** — Formal quote being prepared
- **Quote Sent** — Sent to customer
- **Follow-Up** — Chasing customer response
- **Accepted** — Customer accepted quote

### Delivery Phase
- **Scheduled** — Job booked into the calendar
- **In Progress** — Work underway
- **Waiting on Colour Decision** — Customer deciding on paint colour
- **Waiting on Materials** — Paint/materials ordered, waiting for delivery
- **Waiting on Customer** — Need access or approval to proceed
- **Drying/Curing** — Paint drying, customer unable to access room

### Completion Phase
- **Complete** — Work finished
- **Invoice Sent** — Invoice issued
- **Paid** — Payment received
- **Cancelled** — Job cancelled

---

## Product Catalog (Starter Items)

### Interior Paint (per litre)
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Dulux Standard Matt (1L) | Interior Paint | $18 | $32 |
| Dulux Standard Matt (10L) | Interior Paint | $145 | $245 |
| Dulux Premium (Equivalent) (1L) | Interior Paint | $22 | $38 |
| Dulux Premium (10L) | Interior Paint | $180 | $310 |
| Taubmans Endure (1L) | Interior Paint | $16 | $28 |
| Taubmans Endure (10L) | Interior Paint | $130 | $220 |
| Taubmans Econoquick (1L) | Interior Paint | $14 | $25 |
| Taubmans Econoquick (10L) | Interior Paint | $110 | $185 |

### Exterior Paint (per litre)
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Dulux Weathershield (1L) | Exterior Paint | $24 | $42 |
| Dulux Weathershield (10L) | Exterior Paint | $200 | $340 |
| Taubmans Weathermax (1L) | Exterior Paint | $22 | $38 |
| Taubmans Weathermax (10L) | Exterior Paint | $180 | $300 |
| Dulux Duralloy Metal (1L) | Metal/Roof | $26 | $45 |
| Dulux Duralloy Metal (10L) | Metal/Roof | $220 | $380 |

### Primers & Undercoats (per litre)
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Dulux Universal Primer (1L) | Primer | $16 | $28 |
| Dulux Universal Primer (10L) | Primer | $130 | $220 |
| Taubmans Primer 200 (1L) | Primer | $14 | $24 |
| Taubmans Primer 200 (10L) | Primer | $110 | $185 |
| Dulux Undercoat (1L) | Undercoat | $12 | $22 |
| Rust-Oleum Metal Primer (400ml spray) | Metal Primer | $8 | $16 |

### Fillers & Preparation
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Selleys Wall Putty (250g) | Filler | $4 | $9 |
| Selleys Wall Putty (1kg) | Filler | $12 | $22 |
| Selleys Spakfilla (Powder, 1kg) | Filler | $6 | $12 |
| All Purpose Jointing Compound (20kg) | Joint Compound | $18 | $35 |
| Sandpaper Assort Pack (80-240 grit) | Abrasive | $8 | $16 |

### Specialty Coatings
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Epoxy Floor Coating (5L kit) | Specialty | $85 | $150 |
| Metallic Paint Effect (1L) | Specialty | $20 | $38 |
| Textured Coating (20kg) | Specialty | $45 | $85 |
| Wallpaper Paste (5kg) | Wallpaper | $8 | $16 |
| Anti-Mould Paint Additive | Specialty | $12 | $22 |

### Tools & Equipment (hire/supply)
| Product | Category | Typical Cost | Typical Sell |
|---------|----------|-------------|-------------|
| Scaffolding (per day) | Equipment | $0 | $120 |
| Pressure Washer Hire (per day) | Equipment | $0 | $80 |
| Wallpaper Removal (labour) | Service | $0 | $45/hr |
| Colour Consultation | Service | $0 | $150 |

---

## Labour Sections

| Section | Description | Default Rate |
|---------|-------------|-------------|
| Site Prep | Surface preparation (clean, sand, fill, prime) | $55/hr |
| Painting — Interior (1–2 coats) | Interior walls and ceilings | $55/hr |
| Painting — Exterior (1–2 coats) | Exterior walls and weatherboards | $65/hr |
| Specialty Finishes | Epoxy, textured, effects, murals | $75/hr |
| Wallpaper Application | Hanging and sealing | $60/hr |
| Wallpaper Removal | Stripping and prep | $45/hr |
| Scaffolding/Access Setup | Tower erection, safety setup | $70/hr |
| Clean-Up | Post-paint cleanup, protection removal | $40/hr |

---

## Billing Defaults

| Setting | Default Value |
|---------|--------------|
| Interior hourly rate | $55/hr |
| Exterior hourly rate | $65/hr |
| Specialty finishes rate | $75/hr |
| Wallpaper rate | $60/hr |
| Interior per-room rate | $280–$650 (depending on size) |
| Interior per-m² rate | $18–$28/m² (2 coats) |
| Exterior per-m² rate | $22–$35/m² (2 coats) |
| Exterior per-room rate | $450–$1,200 |
| Roof per-m² rate | $25–$40/m² |
| Epoxy floor per-m² rate | $65–$95/m² |
| Day rate (2-person team) | $650–$850 |
| Paint markup | 30–50% |
| GST rate | 10% |
| Quote expiry | 30 days |
| Payment terms | Due on completion (residential), 14 days (commercial) |

---

## Checklist Templates

### Interior Repaint (1–2 Rooms)
- [ ] Pre-paint inspection and photos
- [ ] Move furniture and protect with drop sheets
- [ ] Mask doorways, windows, trim, electrical outlets
- [ ] Patch holes and cracks with filler
- [ ] Sand down patches once dry
- [ ] Vacuum/wipe dust and debris
- [ ] Prime any bare patches or stained areas
- [ ] Apply first coat of paint
- [ ] Check for drips, runs, coverage
- [ ] Allow proper drying time between coats
- [ ] Apply second coat (if scheduled)
- [ ] Remove masking tape while paint is still tacky
- [ ] Final touch-ups and inspection
- [ ] Clean up drop sheets and equipment
- [ ] Return furniture to original positions
- [ ] Customer sign-off and photos
- [ ] Invoice issued

### Exterior Repaint (House Facade)
- [ ] Pre-paint inspection and condition report
- [ ] Pressure wash or manual clean facade
- [ ] Allow drying time (48 hours min)
- [ ] Inspect for damage, cracks, rot
- [ ] Make any necessary repairs (caulking, wood filler)
- [ ] Prime any bare patches or new repairs
- [ ] Mask windows, fittings, and neighbours' property
- [ ] Set up scaffolding (if required)
- [ ] Apply first coat of exterior paint
- [ ] Inspect coverage and touch up gaps
- [ ] Allow curing time (weather dependent)
- [ ] Apply second coat if scheduled
- [ ] Final inspection and touch-ups
- [ ] Remove masking and protective coverings
- [ ] Dismantle scaffolding
- [ ] Clean up and dispose of waste
- [ ] Customer sign-off and photos

### New Build Paint (Standard Turnover)
- [ ] Inspect walls for defects (dings, marks, dust)
- [ ] Final sand-back of all painted surfaces
- [ ] Vacuum entire property
- [ ] Mask light fittings, windows, doors
- [ ] Prime any stained areas or repairs
- [ ] First coat all interior walls and ceilings
- [ ] Dry and inspect coverage
- [ ] Touch-ups as required
- [ ] Second coat all interior surfaces
- [ ] Remove masking
- [ ] Final clean and final coat of paint (if required)
- [ ] Touch up exterior primer and paint (if in scope)
- [ ] Final walkthrough with site manager/buyer
- [ ] Defect list and rectification plan
- [ ] Final photographs for handover

### Specialty Finish — Epoxy Floor
- [ ] Site inspection and moisture testing
- [ ] Concrete prep (grind, clean, degrease)
- [ ] Fill any cracks or holes in concrete
- [ ] Allow concrete to cure fully (if new)
- [ ] Vacuum and final clean
- [ ] Prime concrete with epoxy primer
- [ ] Measure area and calculate epoxy mix ratio
- [ ] Apply first coat of epoxy
- [ ] Allow full cure time (typically 24–48 hrs)
- [ ] Sand lightly between coats (if textured)
- [ ] Apply second coat
- [ ] Allow final cure before foot traffic
- [ ] Install edge trim or skirting (if required)
- [ ] Customer briefing on curing and care
- [ ] Final sign-off

---

## Dependency Rules (Auto-Add)

| When Job Category Is | Auto-Add Product | Qty | Notes |
|---------------------|------------------|-----|-------|
| Interior Paint | Universal Primer | 1–2L | As needed for new walls/patches |
| Exterior Paint | Exterior Primer | 1–2L | As needed for weatherboards/repairs |
| Specialty Finishes (Epoxy) | Epoxy Floor Coating | Per m² | Full kit required |
| Wallpaper Application | Wallpaper Paste | As needed | Sufficient for wall area |
| New Build | Universal Primer | 2–3L | For sealing/stain blocking |
| Exterior (Timber) | Rust-Oleum Metal Primer | 1–2 cans | For any metal work |

---

## Scope of Works (Auto-Generated Text)

### Interior Residential Repaint
> Supply and apply [PAINT_PRODUCT] interior paint to [NUMBER] rooms at [SITE_ADDRESS]. Works include surface preparation (patching, sanding, cleaning), application of primer to any bare patches or stained areas, and [NUMBER] coats of finish paint. All surfaces cleaned, masked, and protected throughout. Paint applied in accordance with manufacturer specifications and Australian Standards. Includes minor touch-ups and final cleanup. Customer signature required upon completion.

### Exterior Residential Repaint
> Supply and apply [PAINT_PRODUCT] exterior paint to facade of property at [SITE_ADDRESS]. Works include pressure washing and cleaning, inspection for damage, minor repairs (caulking, timber filler), priming of repairs, and [NUMBER] coats of finish paint. Includes masking of windows, fittings, and neighbours' property. [Scaffolding setup and removal included / Scaffolding to be hired separately]. All work completed in accordance with Australian weather guidelines and manufacturer specifications. Final inspection and customer sign-off upon completion.

### Specialty Finish — Epoxy Floor
> Supply and apply epoxy floor coating to [AREA] m² at [SITE_ADDRESS]. Works include concrete inspection and moisture testing, surface preparation (grinding, degreasing, cleaning), application of epoxy primer, and [NUMBER] coats of epoxy topcoat. Includes filling of any cracks or imperfections. Customer to ensure area is clear for [CURING_PERIOD] hours. All work completed to manufacturer specifications. Final sign-off upon full curing.

### Wallpaper Application
> Supply and hang wallpaper [WALLPAPER_SPEC] to [NUMBER] walls at [SITE_ADDRESS]. Works include surface preparation, priming (if required), measuring and cutting wallpaper, application of paste, hanging and smoothing, trimming, and final edge sealing. Includes removal of existing wallpaper if required. All work completed in accordance with Australian Standards. Customer sign-off upon completion.

---

## AI Voice Agent (Ava) — Painting Script Additions

### Key Questions Ava Asks
- "Are you looking to paint the interior, exterior, or both?"
- "Can you tell me which rooms or areas you'd like painted?"
- "What's the approximate size of the space — do you know the room dimensions or total wall area?"
- "Are you repainting with a fresh coat, or looking to change colour?"
- "Is the property residential, commercial, or a multi-unit building?"
- "Do you need help choosing a paint colour, or do you already have colours in mind?"
- "When would you like to get this work done — do you have a preferred timeframe?"
- "Is there anything else you'd like — specialty finishes, wallpaper, epoxy flooring?"

### Ava Qualifying Logic
- Interior + colour consult needed → High-value, book site visit
- Exterior (large area) → High-value, book site visit for quote
- Specialty finish (epoxy, wallpaper) → Book site visit, gather detail
- Single-room interior refresh → Phone quote possible (estimate per m²)
- Emergency/urgent job → Priority scheduling
- Commercial/multi-unit → Escalate for commercial rates quote

---

## Customisation Points (Per Client)

When onboarding a painting client, customise:

1. **Their service scope** — Interior only, exterior, or both? Specialty finishes offered? Colour consultation?
2. **Their pricing** — Update labour rates and per-room/per-m² rates to match their market position
3. **Their paint suppliers** — Which brands do they prefer? (Dulux, Taubmans, others?) Update supplier costs
4. **Their service area** — Suburbs/postcodes for scheduling and travel time allowance
5. **Their team** — Staff names, colours for calendar, painting specialty (interior/exterior/specialist)
6. **Their equipment** — Do they own scaffolding or hire? Pressure washer? Equipment costs
7. **Their colour palette** — Common colours for quick quoting, paint codes from their preferred brands
8. **Their turnaround times** — Drying/curing windows in their climate, job scheduling windows
9. **Their existing customers** — Import from previous system or CRM
10. **Ava's greeting** — Business name, key services (e.g., "Interior & Exterior Painting, Decorating, Specialist Finishes")
