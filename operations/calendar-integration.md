# Cal.com Integration Guide — Velocity AI

## Overview

This guide walks through setting up Cal.com as the calendar booking system for Velocity AI. The goal: let Ava (our Retell AI voice agent) check Mitchell's real availability and book discovery calls on the spot during live phone calls.

**Stack:** Cal.com (scheduling) → Google Calendar (Mitchell's calendar) → Cal.com API v2 → Retell AI custom function → Ava books in real time.

---

## 1. Cal.com Account Setup

### Which Plan?

The **Free plan** covers everything we need for a single-user setup:

- Unlimited calendar connections
- Unlimited event types
- API access (v2)
- Google Calendar integration
- Workflow automations
- No usage limits

The free plan includes Cal.com branding on booking pages, but since all bookings happen via API (through Ava), callers never see the booking page. If you later want branded booking pages for the website, the Teams plan ($15/user/month) removes branding.

### Signup Steps

1. Go to [cal.com/signup](https://cal.com/signup)
2. Sign up with your Google account (mitchpearce94@gmail.com) — this auto-connects Google Calendar
3. Set your timezone to **Australia/Brisbane** (AEST, UTC+10, no daylight saving)
4. Choose a username (e.g., `mitchell-velocityai` or `mitchellpearce`)
5. Complete the onboarding wizard

### Generate an API Key

1. Go to **Settings → Developer → API Keys**
2. Click **Create new API key**
3. Name it `retell-booking-integration`
4. Set expiry to **Never** (or 1 year if you prefer to rotate)
5. Copy the key — it'll look like `cal_live_xxxxxxxxxxxxxxxxxxxx`
6. Store it securely — you'll need it for the booking API wrapper and the webhook server

---

## 2. Connect Google Calendar

If you signed up with Google, this may already be done. To verify or add manually:

1. Go to **Settings → Calendars & Scheduling → Calendar connections**
2. Click **Connect Google Calendar**
3. Authorise access to your Google account
4. Under **Check for conflicts**, enable your primary Google Calendar — this ensures Cal.com checks your existing appointments before showing availability
5. Under **Add to calendar**, select your primary Google Calendar — this is where new bookings will appear

Once connected, any booking made through Cal.com (including via API) automatically creates a Google Calendar event with all the details.

---

## 3. Create the "Discovery Call" Event Type

1. Go to **Event Types** in the sidebar
2. Click **New Event Type**
3. Configure:

| Setting | Value |
|---|---|
| Title | Discovery Call with Mitchell |
| Slug | `discovery-call` |
| Duration | 15 minutes |
| Location | Phone call (you'll call them) |
| Description | A quick intro call to understand your business and see how Velocity AI can help. |

4. Under **Availability**, set a custom schedule (or create a new one):

**Weekday Mornings:**
- Monday–Friday: 7:00 AM – 9:00 AM

**Midday:**
- Monday–Friday: 12:00 PM – 1:00 PM

**Evenings:**
- Monday–Friday: 5:00 PM – 7:00 PM

5. Set timezone to **Australia/Brisbane**
6. Under **Advanced → Booking limits**, consider:
   - Minimum notice: 2 hours (so nobody books a call starting in 5 minutes)
   - Buffer before/after: 5 minutes
   - Max bookings per day: 6 (to avoid back-to-back burnout)
7. Under **Booking questions**, the default collects name and email. Add:
   - Phone number (required)
   - "What's your business about?" (optional, short text)
8. Save the event type

**Your booking slug will be:** `cal.com/{username}/discovery-call`

---

## 4. API Reference — Endpoints We Use

All requests go to `https://api.cal.com/v2/`. Every request must include the header `cal-api-version: 2024-08-13`.

### 4.1 Check Available Slots

```
GET /v2/slots
```

**Query Parameters:**

| Param | Type | Required | Example |
|---|---|---|---|
| `username` | string | Yes | `mitchellpearce` |
| `eventSlug` | string | Yes | `discovery-call` |
| `startTime` | ISO 8601 (UTC) | Yes | `2026-04-03T00:00:00Z` |
| `endTime` | ISO 8601 (UTC) | Yes | `2026-04-04T23:59:59Z` |

**Headers:**
```
cal-api-version: 2024-08-13
```

**Authentication:** Not required (public endpoint).

**Example Request:**
```
GET https://api.cal.com/v2/slots?username=mitchellpearce&eventSlug=discovery-call&startTime=2026-04-03T00:00:00Z&endTime=2026-04-04T23:59:59Z
```

**Response (200):**
```json
{
  "status": "success",
  "data": {
    "slots": {
      "2026-04-03": [
        { "time": "2026-04-02T21:00:00.000Z" },
        { "time": "2026-04-02T21:15:00.000Z" },
        { "time": "2026-04-02T21:30:00.000Z" },
        { "time": "2026-04-02T21:45:00.000Z" },
        { "time": "2026-04-02T22:00:00.000Z" }
      ]
    }
  }
}
```

Note: Times are returned in UTC. 7:00 AM AEST = 21:00 UTC (previous day). Convert to AEST by adding 10 hours.

### 4.2 Create a Booking

```
POST /v2/bookings
```

**Headers:**
```
Content-Type: application/json
cal-api-version: 2024-08-13
Authorization: Bearer cal_live_xxxxxxxxxxxx
```

**Request Body:**
```json
{
  "eventTypeSlug": "discovery-call",
  "username": "mitchellpearce",
  "start": "2026-04-02T21:00:00.000Z",
  "attendee": {
    "name": "Dave Smith",
    "email": "dave@email.com",
    "timeZone": "Australia/Brisbane"
  },
  "bookingFieldsResponses": {
    "phone": "0412 345 678",
    "notes": "Plumbing business, 5 employees, interested in AI phone answering"
  }
}
```

**Response (200):** Returns booking confirmation with a unique `uid` for future reference.

### 4.3 Cancel a Booking

```
POST /v2/bookings/{bookingUid}/cancel
```

**Headers:**
```
Content-Type: application/json
cal-api-version: 2024-08-13
Authorization: Bearer cal_live_xxxxxxxxxxxx
```

**Body (optional):**
```json
{
  "cancellationReason": "Caller requested cancellation"
}
```

### 4.4 Reschedule a Booking

```
POST /v2/bookings/{bookingUid}/reschedule
```

**Headers:**
```
Content-Type: application/json
cal-api-version: 2024-08-13
Authorization: Bearer cal_live_xxxxxxxxxxxx
```

**Body:**
```json
{
  "start": "2026-04-03T02:00:00.000Z",
  "rescheduleReason": "Caller requested a different time"
}
```

### 4.5 Rate Limits

- 120 requests per minute (API key auth)
- Headers `X-RateLimit-Remaining` and `X-RateLimit-Reset` are returned
- Implement exponential backoff on 429 responses
- For Ava's use case (a few calls per hour), we'll never hit limits

---

## 5. Timezone Handling

Mitchell operates in **Australia/Brisbane (AEST, UTC+10)**. Brisbane does not observe daylight saving time, so the offset is always +10:00.

**Conversions:**
- 7:00 AM AEST = 21:00 UTC (previous day)
- 12:00 PM AEST = 02:00 UTC (same day)
- 5:00 PM AEST = 07:00 UTC (same day)

**In the API:**
- All `startTime` and `endTime` params must be in UTC (ISO 8601 with Z suffix)
- The booking API wrapper (`calendar-booking.py`) handles conversion automatically
- When presenting times to callers, Ava always uses AEST (e.g., "Thursday at 8 AM")

---

## 6. How Retell AI Connects to Cal.com

The integration flow during a live call:

```
Caller: "Yeah, let's book something in"
  ↓
Ava triggers check_availability function
  ↓
Retell sends POST to our webhook server
  ↓
Webhook server calls Cal.com GET /v2/slots
  ↓
Server returns available times to Retell
  ↓
Ava reads options: "I've got Thursday at 7:30 AM or 12:15 PM — what works?"
  ↓
Caller picks a time
  ↓
Ava triggers book_discovery_call function with caller details
  ↓
Retell sends POST to webhook server
  ↓
Server calls Cal.com POST /v2/bookings
  ↓
Server returns confirmation to Retell
  ↓
Ava: "Done — you're locked in for Thursday at 7:30 AM. You'll get a confirmation email."
```

### Webhook Server Requirements

You need a simple HTTPS server (can be a Python Flask/FastAPI app or a serverless function) that:

1. Listens for POST requests from Retell AI
2. Validates the `x-retell-signature` header
3. Parses the function name and parameters from the request body
4. Calls the appropriate Cal.com API endpoint
5. Returns the result as a string that Ava can speak

See `calendar-booking.py` for the API wrapper, and `booking-function-spec.md` for the Retell function specification.

---

## 7. Testing Checklist

After setup, verify:

- [ ] Cal.com account created with correct timezone (Australia/Brisbane)
- [ ] Google Calendar connected — check for conflicts enabled
- [ ] "Discovery Call with Mitchell" event type created with correct availability windows
- [ ] API key generated and stored securely
- [ ] `python calendar-booking.py slots tomorrow` returns correct available times
- [ ] `python calendar-booking.py book "Test User" "test@test.com" "0400000000" "2026-04-03 07:00"` creates a booking
- [ ] Booking appears in Google Calendar
- [ ] Cancel test booking via CLI
- [ ] Webhook server deployed and accessible via HTTPS
- [ ] End-to-end test: call Ava → request booking → Ava checks availability → book a slot → confirm in Google Calendar
