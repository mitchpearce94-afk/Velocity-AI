# Retell AI Booking Function Specification — Velocity AI

## Overview

This document defines the custom functions that Ava (our Retell AI voice agent) uses to check Mitchell's calendar availability and book discovery calls in real time during live phone calls.

Retell AI supports custom functions that the LLM can invoke mid-conversation. When triggered, Retell sends a POST request to our webhook endpoint. Our server processes the request (calling Cal.com's API), then returns a text response that Ava speaks to the caller.

---

## Functions

### 1. `check_availability`

**Purpose:** Check Mitchell's available time slots for a given date so Ava can offer specific options to the caller.

**When Ava should call this:** When the caller agrees to book a discovery call, or asks about availability.

**Function Definition (Retell format):**

```json
{
  "name": "check_availability",
  "description": "Check Mitchell's available time slots for discovery calls on a specific date. Call this when the caller wants to book a meeting or asks about availability. Returns available times in Brisbane time.",
  "parameters": {
    "type": "object",
    "properties": {
      "date": {
        "type": "string",
        "description": "The date to check availability for. Use 'tomorrow', 'today', or a specific date in YYYY-MM-DD format. If the caller says a day of the week (e.g., 'Thursday'), convert it to the next occurrence of that day."
      }
    },
    "required": ["date"]
  }
}
```

**Speak During Execution:** Enabled — Ava says something like "Let me check what's available..." while the function runs.

**Speak After Execution:** Enabled — Ava reads back the available slots from the response.

---

### 2. `book_discovery_call`

**Purpose:** Create a confirmed booking once the caller has chosen a time and provided their details.

**When Ava should call this:** After the caller selects a specific time slot and has provided their name, email, and phone number.

**Function Definition (Retell format):**

```json
{
  "name": "book_discovery_call",
  "description": "Book a 15-minute discovery call with Mitchell at a specific time. Only call this after the caller has confirmed a time slot and provided their name, email, and phone number.",
  "parameters": {
    "type": "object",
    "properties": {
      "caller_name": {
        "type": "string",
        "description": "The caller's full name."
      },
      "caller_email": {
        "type": "string",
        "description": "The caller's email address for the booking confirmation."
      },
      "caller_phone": {
        "type": "string",
        "description": "The caller's phone number (Australian format)."
      },
      "booking_time": {
        "type": "string",
        "description": "The selected booking time in 'YYYY-MM-DD HH:MM' format, Brisbane timezone. For example, '2026-04-03 09:00' for 9:00 AM Brisbane time on 3 April 2026."
      },
      "notes": {
        "type": "string",
        "description": "Brief notes about the caller's business and what they're interested in. Include trade type, business name, and key pain points discussed during the call."
      }
    },
    "required": ["caller_name", "caller_email", "caller_phone", "booking_time"]
  }
}
```

**Speak During Execution:** Enabled — Ava says "Just locking that in for you now..." while the booking is created.

**Speak After Execution:** Enabled — Ava confirms the booking details.

---

### 3. `cancel_booking` (future use)

**Purpose:** Cancel an existing discovery call booking.

**When Ava should call this:** When an existing caller requests to cancel their upcoming discovery call.

```json
{
  "name": "cancel_booking",
  "description": "Cancel an existing discovery call booking. Use when a caller wants to cancel their scheduled call with Mitchell.",
  "parameters": {
    "type": "object",
    "properties": {
      "booking_uid": {
        "type": "string",
        "description": "The unique booking reference ID."
      },
      "reason": {
        "type": "string",
        "description": "Reason for cancellation."
      }
    },
    "required": ["booking_uid"]
  }
}
```

---

## Webhook Endpoint

### URL

```
https://api.velocityai.com.au/retell/booking-webhook
```

(Replace with your actual deployed endpoint. This can be a Flask, FastAPI, or serverless function.)

### Request Format (from Retell to our server)

When Ava triggers a function, Retell sends a POST request:

```http
POST /retell/booking-webhook HTTP/1.1
Host: api.velocityai.com.au
Content-Type: application/json
X-Retell-Signature: <signature_for_verification>
```

```json
{
  "event": "function_call",
  "call_id": "call_abc123def456",
  "function_name": "check_availability",
  "arguments": {
    "date": "2026-04-03"
  }
}
```

For a booking call:

```json
{
  "event": "function_call",
  "call_id": "call_abc123def456",
  "function_name": "book_discovery_call",
  "arguments": {
    "caller_name": "Dave Smith",
    "caller_email": "dave@smithplumbing.com.au",
    "caller_phone": "0412 345 678",
    "booking_time": "2026-04-03 09:00",
    "notes": "Plumbing business, 5 employees, interested in AI phone answering and booking automation"
  }
}
```

### Response Format (our server back to Retell)

Our webhook must return a JSON response with a `result` string. This string is what Ava will use to continue the conversation.

**For `check_availability`:**

```json
{
  "result": "I've got a few options: Thursday 3 April at 7:30 AM Brisbane time, Thursday 3 April at 12:15 PM Brisbane time, or Thursday 3 April at 5:00 PM Brisbane time. What suits you best?"
}
```

**For `book_discovery_call`:**

```json
{
  "result": "You're all booked in, Dave. Mitchell will give you a call at the booked time. You'll get a confirmation email at dave@smithplumbing.com.au shortly."
}
```

**For errors:**

```json
{
  "result": "Sorry, I had a bit of trouble locking that in. Let me take your details and Mitchell will call you to sort out a time."
}
```

### Webhook Security

Verify the `X-Retell-Signature` header to confirm requests are from Retell:

```python
import hmac
import hashlib

def verify_retell_signature(payload_body: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

---

## Webhook Server Implementation

A minimal Flask server that handles both functions:

```python
from flask import Flask, request, jsonify
from calendar_booking import handle_retell_webhook

app = Flask(__name__)
RETELL_SECRET = "your_retell_webhook_secret"

@app.route("/retell/booking-webhook", methods=["POST"])
def booking_webhook():
    # Verify signature
    signature = request.headers.get("X-Retell-Signature", "")
    # (add verification logic here)

    payload = request.get_json()
    result = handle_retell_webhook(payload)

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, ssl_context="adhoc")
```

---

## Retell Agent Configuration

In the Retell AI dashboard, configure the agent with:

1. **Custom Functions:** Add `check_availability` and `book_discovery_call` using the JSON definitions above
2. **Webhook URL:** Set to your deployed endpoint (e.g., `https://api.velocityai.com.au/retell/booking-webhook`)
3. **Webhook Secret:** Generate and store securely; configure in both Retell and your server
4. **Speak During Execution:** Enable for both functions with natural filler phrases
5. **Speak After Execution:** Enable for both functions so Ava relays the response

---

## How Ava's Prompt References the Functions

In the agent prompt (see `agent-prompt.md`), the booking section tells Ava when and how to use the functions. Ava doesn't need to know the technical details — she just needs to know:

- When someone wants to book, call `check_availability` with the date
- When they choose a time and you have their details, call `book_discovery_call`
- If something goes wrong, fall back to taking their details manually

The LLM handles function invocation automatically based on the prompt context and conversation flow. See the updated "Booking a Discovery Call" section in `agent-prompt.md` for the exact prompt language.

---

## Testing

1. **Unit test the webhook handler:** Send mock payloads to `handle_retell_webhook()` in `calendar-booking.py`
2. **Integration test:** Deploy the webhook server, use Retell's test call feature to trigger functions
3. **End-to-end:** Make a real call to the Retell number, go through the booking flow, verify the booking appears in Google Calendar

### Test Payloads

**Test check_availability:**
```bash
curl -X POST https://api.velocityai.com.au/retell/booking-webhook \
  -H "Content-Type: application/json" \
  -d '{"event": "function_call", "call_id": "test_001", "function_name": "check_availability", "arguments": {"date": "tomorrow"}}'
```

**Test book_discovery_call:**
```bash
curl -X POST https://api.velocityai.com.au/retell/booking-webhook \
  -H "Content-Type: application/json" \
  -d '{"event": "function_call", "call_id": "test_002", "function_name": "book_discovery_call", "arguments": {"caller_name": "Test User", "caller_email": "test@test.com", "caller_phone": "0400000000", "booking_time": "2026-04-03 09:00", "notes": "Test booking"}}'
```
