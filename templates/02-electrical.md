# Velocity AI — Electrical CRM Template

> Inherits from: 00-master-architecture.md
> Trades: Electricians, Data/Comms, Solar Installers, Air Con (electrical side)

---

## Categories (Job Types)

| Category | Description |
|----------|-------------|
| General Electrical | Powerpoints, switches, fault finding, safety switches |
| Switchboard | Upgrades, RCD installation, metering, safety compliance |
| Lighting | LED upgrades, downlights, outdoor/security lighting, smart lighting |
| Data & Communications | Network cabling, phone points, TV points, data racks |
| Solar | Panel install, inverter replacement, battery storage |
| EV Charging | Home and commercial EV charger installation |
| Air Conditioning | Split system install (electrical side), circuit additions |
| Ceiling Fans | Supply and install, replacement |
| Smoke Alarms | Install, replacement, compliance upgrades (hardwired) |
| Commercial | Office fit-outs, shop lighting, 3-phase, commercial maintenance |
| New Build | Rough-in and fit-off for new construction |
| Renovation | Full rewire, circuit additions, renovation electrical |
| Emergency | After-hours faults, power outages, safety hazards |
| Testing & Tagging | Appliance testing, safety certificates |
| Security | CCTV, alarms, intercom, access control (electrical connection) |

---

## Statuses

### Planning Phase
- **New** — Enquiry received
- **Assessment Booked** — Site visit scheduled
- **Assessed** — Site visited, ready to quote

### Quoting Phase
- **Quoting** — Preparing quote
- **Quote Sent** — Sent to customer
- **Follow-Up** — Chasing response
- **Accepted** — Customer approved

### Delivery Phase
- **Scheduled** — Booked in calendar
- **In Progress** — Onsite, work underway
- **Rough-In** — First fix (cables in walls before plaster)
- **Fit-Off** — Second fix (switches, GPOs, fixtures)
- **Waiting on Materials** — Parts on order
- **Waiting on Inspection** — Awaiting electrical inspector
- **Warranty/Defect** — Return visit

### Completion Phase
- **Complete** — Work done, certificate issued
- **Invoice Sent** — Invoice raised
- **Paid** — Payment received
- **Cancelled** — Job cancelled

---

## Product Catalog (Starter Items)

### Switchboard & Safety
| Product | Category | Cost | Sell |
|---------|----------|------|------|
| Safety Switch (RCD) 2-pole | Switchboard | $45 | $85 |
| Safety Switch (RCD) 4-pole | Switchboard | $65 | $120 |
| MCB 10A | Switchboard | $12 | $25 |
| MCB 16A | Switchboard | $12 | $25 |
| MCB 20A | Switchboard | $14 | $28 |
| MCB 32A | Switchboard | $18 | $35 |
| Switchboard 12-way | Switchboard | $120 | $220 |
| Switchboard 18-way | Switchboard | $180 | $320 |
| Switchboard 24-way | Switchboard | $250 | $420 |

### Powerpoints & Switches
| Product | Category | Cost | Sell |
|---------|----------|------|------|
| Single GPO | General | $8 | $15 |
| Double GPO | General | $10 | $18 |
| Weatherproof GPO | General | $22 | $40 |
| Light Switch (single) | General | $8 | $15 |
| Dimmer Switch | General | $35 | $65 |
| USB GPO | General | $25 | $45 |

### Lighting
| Product | Category | Cost | Sell |
|---------|----------|------|------|
| LED Downlight (10W) | Lighting | $18 | $35 |
| LED Downlight (13W) | Lighting | $22 | $42 |
| LED Batten (1200mm) | Lighting | $35 | $65 |
| LED Floodlight (30W) | Lighting | $45 | $85 |
| LED Floodlight (50W) | Lighting | $65 | $120 |
| Sensor Light (LED) | Lighting | $55 | $100 |

### Solar
| Product | Category | Cost | Sell |
|---------|----------|------|------|
| Solar Panel 400W (each) | Solar | $180 | $320 |
| Inverter 5kW (single phase) | Solar | $1,200 | $1,800 |
| Inverter 8kW (single phase) | Solar | $1,800 | $2,600 |
| Inverter 10kW (3 phase) | Solar | $2,200 | $3,200 |
| Battery 10kWh | Solar | $8,000 | $11,000 |
| Battery 13.5kWh (Tesla PW) | Solar | $10,500 | $14,500 |

### Ceiling Fans
| Product | Category | Cost | Sell |
|---------|----------|------|------|
| Ceiling Fan (standard 1200mm) | Fans | $120 | $220 |
| Ceiling Fan (DC motor 1300mm) | Fans | $250 | $420 |
| Ceiling Fan + Light | Fans | $180 | $320 |

### Smoke Alarms
| Product | Category | Cost | Sell |
|---------|----------|------|------|
| Hardwired Smoke Alarm (240V) | Safety | $55 | $95 |
| Hardwired Smoke Alarm + Interconnect | Safety | $65 | $110 |

### Flat-Rate Services
| Product | Category | Cost | Sell |
|---------|----------|------|------|
| Fault Finding (first hour) | Service | $0 | $180 |
| Switchboard Safety Inspection | Service | $0 | $220 |
| Smoke Alarm Compliance Check | Service | $0 | $150 |
| Certificate of Compliance (ECOC) | Service | $0 | $80 |
| Test & Tag (per item) | Service | $0 | $8 |

---

## Labour Sections

| Section | Description | Default Rate |
|---------|-------------|-------------|
| Rough-In | Cable runs, conduit, back boxes (before plaster) | $90/hr |
| Fit-Off | Install switches, GPOs, fixtures, final connections | $90/hr |
| Commissioning | Testing, labelling, compliance checks | $90/hr |
| Switchboard | Board upgrades, RCD installs, circuit additions | $100/hr |
| Solar Install | Panel mounting, DC wiring, inverter install | $100/hr |
| Emergency/After-Hours | After 5pm and weekends | $140/hr |

---

## Billing Defaults

| Setting | Default Value |
|---------|--------------|
| Standard hourly rate | $90/hr |
| After-hours rate | $140/hr |
| Callout fee | $80 |
| Emergency callout fee | $150 |
| Parts markup | 50–80% |
| GST rate | 10% |
| Quote expiry | 30 days |
| Payment terms | Due on completion (resi), 14–30 days (commercial) |

---

## Checklist Templates

### Switchboard Upgrade
- [ ] Isolate main supply
- [ ] Photo existing board layout
- [ ] Remove old board/components
- [ ] Install new switchboard enclosure
- [ ] Wire main switch
- [ ] Install RCDs (minimum 2 per AS/NZS 3000)
- [ ] Install MCBs per circuit schedule
- [ ] Label all circuits
- [ ] Terminate all active, neutral, earth conductors
- [ ] Insulation resistance test (all circuits)
- [ ] Earth continuity test
- [ ] Polarity check (all circuits)
- [ ] RCD trip time test
- [ ] Issue Electrical Certificate of Compliance (ECOC)
- [ ] Photo completed board
- [ ] Customer walkthrough (show RCD test button)

### LED Lighting Upgrade
- [ ] Confirm fixture count and locations with customer
- [ ] Isolate lighting circuits
- [ ] Remove old fixtures
- [ ] Install LED downlights/battens
- [ ] Connect and test each fixture
- [ ] Check dimmer compatibility (if applicable)
- [ ] Dispose of old fittings
- [ ] Clean up site
- [ ] Test all circuits
- [ ] Customer sign-off

### Solar Installation
- [ ] Confirm roof orientation and shading assessment
- [ ] Install racking/mounting system
- [ ] Install panels per design layout
- [ ] DC wiring from panels to inverter location
- [ ] Install inverter (wall mount)
- [ ] AC wiring from inverter to switchboard
- [ ] Install solar supply main switch
- [ ] Install generation meter (if required)
- [ ] System commissioning and testing
- [ ] Configure monitoring app
- [ ] Register system with distributor (Energex/Ergon)
- [ ] Submit STC paperwork
- [ ] Issue ECOC + design compliance cert
- [ ] Customer handover (app setup, monitoring)
- [ ] Completion photos (roof, inverter, board)

### Smoke Alarm Compliance
- [ ] Check existing alarm locations and types
- [ ] Identify required alarm positions (per QLD legislation)
- [ ] Install hardwired alarms in required locations
- [ ] Interconnect all alarms (hardwired or wireless)
- [ ] Test each alarm individually
- [ ] Test interconnect function (trigger one, all sound)
- [ ] Issue compliance certificate
- [ ] Provide certificate copy to customer
- [ ] Clean up

---

## Dependency Rules (Auto-Add)

| When Category Is | Auto-Add | Qty | Notes |
|-----------------|----------|-----|-------|
| Switchboard | Certificate of Compliance | 1 | Mandatory for all electrical work |
| Solar | STC Paperwork | 1 | Required for rebate |
| Solar | Design Compliance Cert | 1 | CEC requirement |
| Smoke Alarms | Compliance Certificate | 1 | QLD legislation |
| Any job | Certificate of Compliance | 1 | All work needs ECOC |

---

## Scope of Works (Auto-Generated)

### Switchboard Upgrade
> Supply and install new [SIZE]-way switchboard at [SITE_ADDRESS] to replace existing [ceramic fuse/older] board. Works include removal of existing board, installation of new enclosure, main switch, safety switches (RCDs) to all circuits as per AS/NZS 3000, individual circuit breakers, labelling of all circuits, and full testing and certification. Electrical Certificate of Compliance (ECOC) issued on completion.

### LED Lighting Package
> Supply and install [QTY]x [PRODUCT] LED downlights/battens at [SITE_ADDRESS]. Works include removal and disposal of existing fittings, installation of new LED fixtures, connection, testing, and clean-up. All work completed in accordance with AS/NZS 3000.

---

## AI Voice Agent — Electrical Script

### Key Questions
- "What electrical work do you need done?"
- "Is this for a house or a commercial property?"
- "Is this an emergency — like exposed wires, sparking, or a total power outage?"
- "Is your switchboard the old ceramic fuse type or a modern circuit breaker board?"
- "Are you looking at solar, and if so, have you had any quotes yet?"
- "When would suit for us to come and have a look?"

### Qualifying Logic
- Emergency → Flag urgent, attempt immediate callback
- Switchboard upgrade → High-value, common upsell from safety inspection
- Solar enquiry → High-value, book site assessment
- Smoke alarm compliance → Quick win, often same-day
- LED upgrade → Good margin, easy to quote over phone

---

## Customisation Points

1. **Their licence scope** — Not all sparkies do solar, data, or security
2. **Their supplier pricing** — Middys, L&H, Rexel, Electrico, etc.
3. **Their solar brands** — Which panel/inverter brands they install
4. **Their service area and travel charges**
5. **Their team structure** — Apprentice rates vs qualified rates
6. **State-specific compliance** — QLD smoke alarm laws differ from NSW/VIC
7. **Ava's greeting and services offered**
