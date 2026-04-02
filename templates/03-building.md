# Velocity AI — Building & Construction CRM Template

> Inherits from: 00-master-architecture.md
> Trades: Builders, Carpenters, Renovation Specialists, Project Builders

---

## Categories (Job Types)

| Category | Description |
|----------|-------------|
| New Build | Full house construction, granny flats, duplexes |
| Renovation | Kitchen, bathroom, full home reno, extensions |
| Extension | Room additions, second storey |
| Deck & Pergola | Timber/composite decks, pergolas, carports |
| Structural | Load-bearing walls, stumps, restumping, retaining walls |
| Fit-Out | Commercial or residential internal fit-outs |
| Maintenance | General carpentry repairs, door/window replacement |
| Insurance Work | Storm damage, flood repair, insurance claims |
| Fencing | Timber, Colorbond, pool fencing, gates |
| Demolition | Strip-outs, partial or full demolition |
| Concrete | Slabs, driveways, paths (if in scope) |

---

## Statuses

### Planning Phase
- **Enquiry** — Initial contact
- **Site Meeting Booked** — Meeting scheduled
- **Site Meeting Complete** — Assessed, measurements taken
- **Design/Plans** — Plans being drawn or reviewed
- **Council/Approval** — Waiting on DA, BA, or CDC

### Quoting Phase
- **Estimating** — Preparing detailed estimate
- **Quote Sent** — Sent to customer
- **Negotiation** — Client reviewing, changes requested
- **Accepted** — Contract signed

### Delivery Phase
- **Scheduled** — Start date locked in
- **Mobilisation** — Materials ordered, site prep underway
- **Foundation/Slab** — Slab poured, stumps done
- **Frame** — Framing stage
- **Lock-Up** — Roof, windows, doors — building is enclosed
- **Fit-Out** — Internal works (plaster, paint, fixtures)
- **Practical Completion** — Punch list/defects stage
- **Waiting on Subcontractor** — Waiting for sub to finish their scope
- **Waiting on Materials** — Delayed materials
- **On Hold** — Client pause or weather delay
- **Defect/Warranty** — Post-handover return visit

### Completion Phase
- **Handover** — Keys/access handed to client
- **Final Invoice** — Retention/final claim issued
- **Paid** — All payments received
- **Cancelled** — Job cancelled

---

## Product Catalog (Starter Items)

### Framing & Structural
| Product | Category | Unit | Notes |
|---------|----------|------|-------|
| Timber Frame (per m²) | Structural | m² | Varies by design |
| Steel Beam (per metre) | Structural | m | Priced per job |
| Truss Package | Structural | lot | Per roof design |
| Concrete Slab (per m²) | Foundation | m² | 100mm standard |
| Stumps (per stump) | Foundation | ea | Concrete or steel |

### Internal Fit-Out
| Product | Category | Unit | Notes |
|---------|----------|------|-------|
| Plasterboard (per m²) | Fit-Out | m² | Supply + fix |
| Internal Door (standard) | Fit-Out | ea | Hollow core + frame |
| Internal Door (solid core) | Fit-Out | ea | Premium |
| Skirting/Architrave (per m) | Fit-Out | m | Pine or MDF |
| Shelving/Joinery (per unit) | Fit-Out | ea | Custom quoted |

### External
| Product | Category | Unit | Notes |
|---------|----------|------|-------|
| Timber Deck (per m²) | Deck | m² | Merbau or treated pine |
| Composite Deck (per m²) | Deck | m² | Modwood, Trex etc |
| Pergola (standard) | Outdoor | lot | Per design |
| Colorbond Fencing (per m) | Fencing | m | Supply + install |
| Timber Fencing (per m) | Fencing | m | Supply + install |

### Provisional Sums & Allowances
| Item | Category | Notes |
|------|----------|-------|
| Plumbing Allowance | Provisional | Subcontractor scope |
| Electrical Allowance | Provisional | Subcontractor scope |
| Tiling Allowance | Provisional | Subcontractor scope |
| Painting Allowance | Provisional | Subcontractor scope |
| Council Fees | Provisional | DA/BA/CDC fees |
| Engineering | Provisional | Structural engineer fees |

---

## Labour Sections

| Section | Description | Default Rate |
|---------|-------------|-------------|
| Site Prep & Demolition | Strip-out, clearing, temporary works | $85/hr |
| Foundation | Slab prep, formwork, pour coordination | $90/hr |
| Framing | Wall frames, roof trusses, bracing | $90/hr |
| Lock-Up | Roofing, windows, external cladding | $90/hr |
| Fit-Out | Internal linings, doors, trim, joinery | $85/hr |
| Finishing | Final fix, touch-ups, cleaning | $80/hr |
| Project Management | Coordination, scheduling, inspections | $100/hr |
| Apprentice Rate | Reduced rate for apprentices | $45/hr |

---

## Billing Defaults

| Setting | Default Value |
|---------|--------------|
| Standard hourly rate | $85–90/hr (qualified carpenter) |
| Apprentice rate | $45/hr |
| Margin on materials | 15–25% |
| Margin on subcontractors | 10–15% |
| GST rate | 10% |
| Quote expiry | 30 days |
| Payment structure | Progress claims (stage-based) |

### Progress Payment Schedule (New Builds)
| Stage | % of Contract |
|-------|--------------|
| Deposit (on signing) | 5% |
| Slab/Foundation | 15% |
| Frame | 20% |
| Lock-Up | 20% |
| Fit-Out | 20% |
| Practical Completion | 15% |
| Final (retention) | 5% |

### Progress Payment Schedule (Renovations)
| Stage | % of Contract |
|-------|--------------|
| Deposit | 10% |
| Demolition Complete | 15% |
| Rough-In Complete | 25% |
| Fit-Out | 25% |
| Practical Completion | 20% |
| Final | 5% |

---

## Checklist Templates

### Pre-Start (New Build)
- [ ] Contract signed and deposit received
- [ ] Plans approved (DA/BA/CDC)
- [ ] Engineering completed
- [ ] Soil test report received
- [ ] Site survey completed
- [ ] Utility connections arranged (water, sewer, power, comms)
- [ ] Insurance in place (construction all risk)
- [ ] Temporary fencing and site signage installed
- [ ] Portaloo ordered
- [ ] Skip bin ordered
- [ ] Subcontractors booked (plumber, sparkie, tiler, painter)
- [ ] Material orders placed (frame, trusses, windows)
- [ ] Client colour selections confirmed
- [ ] QBCC notification lodged (if applicable)

### Frame Stage Inspection
- [ ] All walls plumb and braced
- [ ] Window and door openings match plans
- [ ] Truss installation per engineering specs
- [ ] Roof bracing installed
- [ ] Wet area noggins installed (for grab rails, towel rails)
- [ ] Services rough-in complete (plumber, sparkie)
- [ ] Frame tie-down straps installed (cyclone areas)
- [ ] Frame inspection booked with certifier
- [ ] Frame inspection passed
- [ ] Photo documentation taken

### Practical Completion
- [ ] All works complete per contract drawings
- [ ] Internal clean completed
- [ ] External clean completed
- [ ] Touch-up paint completed
- [ ] All fixtures and fittings operational
- [ ] Appliances installed and tested
- [ ] Smoke alarms tested
- [ ] Keys and remotes provided
- [ ] Maintenance guides provided (appliances, surfaces)
- [ ] Warranty documentation provided
- [ ] Defect walk-through with client
- [ ] Defect list signed (if any)
- [ ] Practical completion certificate signed
- [ ] Final claim issued

---

## Scope of Works — Auto-Generated

### Deck & Pergola
> Supply and construct [SIZE] m² [MATERIAL] deck with [DESCRIPTION] at [SITE_ADDRESS]. Works include demolition of existing structure (if applicable), concrete footings, structural posts and bearers, [hardwood/treated pine/composite] decking boards, handrails/balustrade as required, and finishing. All works in accordance with AS 1684 and local council requirements. Builder's warranty provided.

### Renovation
> Complete [SCOPE] renovation at [SITE_ADDRESS] as per agreed plans dated [DATE]. Works include demolition and strip-out of existing [AREAS], structural modifications as per engineer's design, framing, plasterboard linings, internal doors and trim, coordination of subcontractors (plumbing, electrical, tiling, painting), final fix, and clean-up. Progress payments as per schedule attached. All works covered under domestic building warranty insurance (QBCC).

---

## AI Voice Agent — Building Script

### Key Questions
- "Are you looking at a new build, renovation, or something smaller like a deck or pergola?"
- "Do you have plans or drawings already, or do you need help with design?"
- "Roughly what size are we talking — square metres or number of rooms?"
- "Have you had any other quotes yet?"
- "When are you looking to start? Is there a deadline like a lease end or baby on the way?"
- "What suburb is the property in?"

### Qualifying Logic
- New build/extension → High-value, book site meeting
- Renovation → High-value, needs detailed assessment
- Deck/pergola → Medium value, can often ballpark over phone
- Insurance work → Good margin, time-sensitive, get details quickly
- Maintenance/small job → May not be worth the build slot — qualify carefully

---

## Customisation Points

1. **Their licence class** — QBCC open builder vs restricted (low rise, medium rise)
2. **Their subcontractor network** — Preferred subbies for each trade
3. **Their progress payment schedule** — Varies by builder
4. **Their project management style** — Some use Buildertrend, Procore, Co-construct
5. **Their warranty terms** — QBCC 6 year + 6 month defect period (QLD)
6. **Their service area** — Travel zones
7. **Council-specific requirements** — Different DA processes per LGA
8. **Their template contracts** — HIA, MBA, or custom
