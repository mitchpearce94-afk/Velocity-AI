# Velocity AI — CRM Master Architecture

> Abstracted from the Centrefit Group CRM (Next.js + Supabase)
> This is the blueprint every trade-specific template inherits from.

---

## Core Modules

Every client CRM ships with these modules. The data fields, pipeline stages, and automations get customised per trade, but the module structure stays the same.

### 1. Dashboard
- Active jobs count
- Active customers count
- Overdue jobs (warning highlight)
- Pipeline value ($)
- Recent jobs (5 most recent)
- Today's schedule
- Filters: staff member, business unit/category

### 2. Customers
- Customer record: name, type (commercial/residential), ABN, is_active, total_revenue
- Customer sites: multiple locations per customer (address, site_name)
- Customer contacts: multiple contacts per customer (name, phone, email, role)
- Parent/child customer relationships (for property managers, franchises, body corps)
- Tabs: Overview, Contacts, Sites, Jobs, Notes

### 3. Jobs
- Job record: number (auto-increment), reference, description, due_date, customer_id, site_id, status_id, category_1_id, category_2_id
- Assigned staff (multiple, with roles)
- Status workflow with phase grouping (Planning → Quoting → Delivery → Completion)
- Tabs: Overview, Staff, Schedule, Notes, Time, Work, Checklist
- Timer for tracking billable hours
- Checklist templates (apply pre-built checklists to jobs)

### 4. Pipeline (Sales/Leads)
- Kanban board with drag-drop stage transitions
- Deal record: customer, value, probability, stage, assigned_to
- Stages: Lead → Proposal → Negotiation → Accepted → Won → Lost
- Convert deal to job (pre-fills customer, reference, description)

### 5. Quoting
- Quote wizard: customer → site → products/services → pricing → review
- Quote types: Full Quote or Progress Payments (PP1 deposit + PP2 balance)
- Line items: product catalog with cost/sell pricing
- Extras: additional charges (travel, callout, etc.)
- Labour: section-based hours with formula calculations
- Auto-generated scope of works text
- PDF generation and email sending
- Client-facing quote response page (accept/decline with digital signature)
- Quote statuses: Draft → Sent → Accepted/Declined/Expired
- Stats: total quotes, draft, sent, accepted, expired counts

### 6. Scheduler
- Weekly grid: staff rows × day columns
- Drag-drop job assignment to staff/date/time slots
- Schedule entries: job_id, staff_id, date, start_time, end_time, notes
- Permission-based: admins edit all, staff edit own

### 7. Reports
- Job completion metrics by status and phase
- Staff utilisation and billable hours
- Pipeline value and deal conversion rates
- Quote statistics and conversion funnel
- Customer metrics (new vs repeat, revenue)
- Revenue trends
- Project profitability

### 8. Checklists
- Reusable templates with ordered items
- Apply templates to jobs
- Track completion per item
- Categories for grouping checklist items

### 9. Staff
- Staff profiles: display_name, initials, colour (for UI), role, email, phone
- Roles: admin, project_manager, staff
- Permission-based UI (admins see management controls)

### 10. Settings
- **Products/Services catalog**: name, SKU, category, cost_price, sell_price, supplier, is_active
- **Dependency rules**: auto-add products when certain conditions are met
- **Billing settings**: labour rate/hr, callout fee, markup %, GST rate, payment terms, quote expiry
- **Checklist templates**: managed from settings

---

## Database Schema (Core Tables)

| Table | Purpose | Key Fields |
|-------|---------|------------|
| customers | Client records | name, type, abn, is_active, total_revenue, parent_customer_id |
| customer_sites | Client locations | customer_id, name, address, city, state, postcode |
| customer_contacts | Client contacts | customer_id, name, email, phone, role |
| jobs | Work orders | number, reference, description, customer_id, site_id, status_id, category_1_id, category_2_id, due_date |
| statuses | Job workflow states | name, phase, colour, sort_order, is_active |
| categories | Job/service categories | name, sort_order, is_active |
| job_staff | Staff assignments | job_id, staff_id, role |
| job_notes | Job activity log | job_id, staff_id, content, created_at |
| job_time | Time tracking | job_id, staff_id, start_time, end_time, billable, notes |
| job_work_entries | Work events | job_id, date, description, staff_id |
| job_checklist_items | Checklist progress | job_id, content, sort_order, is_completed |
| checklist_templates | Reusable checklists | name, items, is_active |
| schedule_entries | Job scheduling | job_id, staff_id, schedule_date, start_time, end_time, notes |
| pipeline_deals | Sales pipeline | customer_id, value, stage, probability, assigned_to |
| quotes | Quote records | ref, status, quote_type, customer_id, site_name, device_counts, pricing_snapshot, labour_data, discount_percent, expires_at, job_id |
| quote_line_items | Quote BOM | quote_id, product_id, quantity, unit_price, sell_price |
| quote_extras | Additional charges | quote_id, name, cost, sell_price |
| quote_products | Product catalog | name, sku, category, price, sell_price, supplier_id, is_active |
| suppliers | Product suppliers | name, is_active |
| billing_settings | Pricing config | labour_rate, callout_fee, markup_percent, gst_rate, payment_terms |
| staff | Team members | display_name, initials, colour, email, phone, role, is_active |

---

## Status Workflow (Universal)

Every trade uses the same 4-phase structure. The specific statuses within each phase get customised.

```
PLANNING         QUOTING           DELIVERY              COMPLETION
├── New          ├── Quoting       ├── Scheduled          ├── Complete
├── Assessment   ├── Quote Sent    ├── In Progress        ├── Invoice Sent
├── Site Visit   ├── Negotiation   ├── On Hold            ├── Cancelled
└── Scoping      └── Accepted      ├── Waiting Materials  └── Closed
                                   └── Rework/Warranty
```

---

## Automations (Universal)

These fire on status transitions and are the same across all trades:

| Trigger | Action |
|---------|--------|
| Quote accepted | Job status → "Accepted" |
| Quote sent | Job status → "Quote Sent" |
| Quote declined | Job status → "Declined" |
| Job marked complete | Prompt for invoice/time check |
| Job overdue | Flag on dashboard, notify assigned staff |
| New pipeline deal | Create customer if new |
| Deal won | Convert to job with pre-filled data |
| Schedule entry created | Notify assigned staff |
| Timer started | Track billable hours |

---

## What Gets Customised Per Trade

| Component | What Changes |
|-----------|-------------|
| **Categories** | Job types specific to the trade (e.g., "Hot Water" for plumber, "Switchboard" for sparkie) |
| **Product catalog** | Materials, parts, and services specific to the trade |
| **Quote structure** | Line items, labour sections, how pricing works |
| **Dependency rules** | Auto-add rules based on service type |
| **Checklist templates** | Trade-specific compliance and quality checklists |
| **Labour sections** | How work is broken down (phases, task types) |
| **Statuses** | Minor tweaks to status names within each phase |
| **Billing defaults** | Hourly rates, callout fees, markup percentages |
| **Scope of works** | Auto-generated text templates for quotes |
| **AI voice agent prompt** | Ava's script and FAQ for the specific trade |

---

## Tech Stack (Inherited)

| Layer | Tool |
|-------|------|
| Frontend | Next.js 14 (App Router) |
| UI | Tailwind CSS + shadcn/ui |
| Database | Supabase (Postgres) |
| Auth | Supabase Auth (email/password) |
| Storage | Supabase Storage (files, PDFs) |
| State | Zustand (client-side) |
| Email | Resend API |
| AI Voice | Retell AI (Ava) |
| Hosting | Vercel |
