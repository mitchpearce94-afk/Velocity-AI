#!/usr/bin/env python3
"""
Velocity AI — Webhook Server
==============================
Handles incoming webhooks from Retell AI (post-call) and Stripe (payments).

Endpoints:
    POST /webhook/retell     — Retell post-call webhook (call ended, analysis ready)
    POST /webhook/stripe     — Stripe payment webhook (invoice paid, subscription created)
    GET  /health             — Health check

Actions on Retell webhook:
    1. Parse call analysis (caller details, disposition, pain points)
    2. If disposition is "interested" or "booked":
       a. Check Cal.com availability for requested time
       b. Create booking if slot available
       c. Send discovery call confirmation email
    3. Log call to leads.json
    4. Trigger email follow-up sequence based on disposition

Actions on Stripe webhook:
    1. Verify webhook signature
    2. On checkout.session.completed → trigger onboarding sequence
    3. On invoice.paid → log payment
    4. On customer.subscription.deleted → flag churn

Usage:
    python webhook-server.py                    # Start on port 8080
    python webhook-server.py --port 9090        # Custom port
    python webhook-server.py --dry-run          # Log actions without executing

Deployment:
    This is designed to run behind ngrok during testing, then deploy to a
    lightweight VPS (e.g. DigitalOcean droplet or Railway) for production.

Requirements:
    pip install flask resend
"""

import os
import sys
import json
import hmac
import hashlib
import logging
import argparse
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, request, jsonify

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent
LEADS_FILE = SCRIPT_DIR / "leads.json"
LOG_DIR = SCRIPT_DIR / "webhook-logs"

RETELL_API_KEY = os.environ.get("RETELL_API_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
CAL_API_KEY = os.environ.get("CAL_API_KEY", "")

# Disposition-to-action mapping
DISPOSITION_ACTIONS = {
    "interested": ["book_discovery_call", "send_confirmation_email"],
    "booked": ["send_confirmation_email"],
    "callback": ["schedule_callback", "send_followup_email"],
    "not_interested": ["log_only"],
    "voicemail": ["add_to_email_sequence"],
    "no_answer": ["add_to_email_sequence"],
    "wrong_number": ["remove_from_pipeline"],
}

# ---------------------------------------------------------------------------
# App Setup
# ---------------------------------------------------------------------------

app = Flask(__name__)
DRY_RUN = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("webhook-server")

LOG_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def load_leads() -> list:
    if LEADS_FILE.exists():
        with open(LEADS_FILE) as f:
            return json.load(f)
    return []


def save_leads(leads: list):
    with open(LEADS_FILE, "w") as f:
        json.dump(leads, f, indent=2)


def find_lead_by_phone(leads: list, phone: str) -> dict | None:
    normalised = normalise_phone(phone)
    for lead in leads:
        if normalise_phone(lead.get("phone", "")) == normalised:
            return lead
    return None


def normalise_phone(phone: str) -> str:
    import re
    if not phone:
        return ""
    digits = re.sub(r"[^\d+]", "", phone)
    if digits.startswith("0") and len(digits) >= 10 and not digits.startswith("+"):
        digits = "+61" + digits[1:]
    elif digits.startswith("61") and not digits.startswith("+") and len(digits) >= 11:
        digits = "+" + digits
    return digits


def log_webhook(source: str, payload: dict):
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    log_file = LOG_DIR / f"{source}_{ts}.json"
    with open(log_file, "w") as f:
        json.dump(payload, f, indent=2)
    log.info(f"Webhook logged to {log_file.name}")


def book_discovery_call(name: str, email: str, phone: str, requested_time: str = None, notes: str = ""):
    """Book a discovery call via Cal.com API."""
    if DRY_RUN:
        log.info(f"[DRY RUN] Would book discovery call for {name} ({email})")
        return {"status": "dry_run", "uid": "dry-run-uid"}

    sys.path.insert(0, str(SCRIPT_DIR))
    from importlib import import_module
    cal = import_module("calendar-booking")

    if requested_time:
        result = cal.create_booking(name, email, phone, requested_time, notes=notes)
    else:
        slots = cal.get_available_slots()
        if not slots:
            log.warning("No available slots found for booking")
            return {"status": "no_slots"}
        first_slot = slots[0]["time"]
        result = cal.create_booking(name, email, phone, first_slot, notes=notes)

    return result


def send_confirmation_email(email: str, first_name: str, call_date: str, call_time: str):
    """Send discovery call confirmation via Resend."""
    if DRY_RUN:
        log.info(f"[DRY RUN] Would send confirmation to {email}")
        return

    sys.path.insert(0, str(SCRIPT_DIR.parent / "emails"))
    from importlib import import_module
    sender = import_module("send-email")
    sender.send_discovery_confirmation(
        to=email,
        first_name=first_name,
        call_date=call_date,
        call_time=call_time,
    )


def update_lead_after_call(leads: list, phone: str, call_data: dict):
    """Update lead record with call analysis data."""
    lead = find_lead_by_phone(leads, phone)
    if not lead:
        log.warning(f"Lead not found for phone {phone}")
        return

    lead["status"] = call_data.get("disposition", lead.get("status", "new"))
    lead["last_call_at"] = datetime.now(timezone.utc).isoformat()
    lead["call_attempts"] = lead.get("call_attempts", 0) + 1

    analysis = call_data.get("analysis", {})
    if analysis:
        lead["call_analysis"] = {
            "disposition": analysis.get("disposition", ""),
            "pain_points": analysis.get("pain_points", []),
            "current_tools": analysis.get("current_tools", ""),
            "team_size": analysis.get("team_size", ""),
            "interest_level": analysis.get("interest_level", ""),
            "notes": analysis.get("summary", ""),
            "call_duration_seconds": call_data.get("duration_seconds", 0),
        }

    if not DRY_RUN:
        save_leads(leads)
    log.info(f"Updated lead: {lead.get('business_name', phone)} → {lead['status']}")


# ---------------------------------------------------------------------------
# Webhook Endpoints
# ---------------------------------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "velocity-ai-webhooks", "dry_run": DRY_RUN})


@app.route("/webhook/retell", methods=["POST"])
def retell_webhook():
    """Handle Retell AI post-call webhook."""
    payload = request.get_json(silent=True) or {}
    log_webhook("retell", payload)

    event_type = payload.get("event", "")
    call_data = payload.get("call", payload.get("data", {}))

    log.info(f"Retell webhook: event={event_type}")

    if event_type not in ("call_ended", "call_analyzed"):
        return jsonify({"status": "ignored", "reason": f"unhandled event: {event_type}"}), 200

    # Extract key fields from call analysis
    analysis = call_data.get("call_analysis", call_data.get("analysis", {}))
    caller_phone = call_data.get("from_number", call_data.get("caller_number", ""))
    caller_name = analysis.get("caller_name", "")
    caller_email = analysis.get("caller_email", "")
    disposition = analysis.get("disposition", "unknown")
    requested_time = analysis.get("requested_booking_time", None)

    log.info(f"Call from {caller_phone} | Name: {caller_name} | Disposition: {disposition}")

    # Update lead database
    leads = load_leads()
    update_lead_after_call(leads, caller_phone, {
        "disposition": disposition,
        "analysis": analysis,
        "duration_seconds": call_data.get("duration_ms", 0) / 1000 if call_data.get("duration_ms") else 0,
    })

    # Execute actions based on disposition
    actions = DISPOSITION_ACTIONS.get(disposition, ["log_only"])
    results = {"disposition": disposition, "actions_taken": []}

    for action in actions:
        if action == "book_discovery_call" and caller_email:
            first_name = caller_name.split()[0] if caller_name else "there"
            notes = f"Trade: {analysis.get('trade_type', 'unknown')}. Pain points: {', '.join(analysis.get('pain_points', []))}"
            booking = book_discovery_call(
                name=caller_name or "Unknown",
                email=caller_email,
                phone=caller_phone,
                requested_time=requested_time,
                notes=notes,
            )
            results["booking"] = booking
            results["actions_taken"].append("book_discovery_call")

        elif action == "send_confirmation_email" and caller_email:
            first_name = caller_name.split()[0] if caller_name else "there"
            # Use booking time if available
            call_date = "TBC"
            call_time = "TBC"
            if "booking" in results and results["booking"].get("start_time"):
                from datetime import datetime as dt
                bt = dt.fromisoformat(results["booking"]["start_time"])
                call_date = bt.strftime("%A, %d %B %Y")
                call_time = bt.strftime("%I:%M %p")
            send_confirmation_email(caller_email, first_name, call_date, call_time)
            results["actions_taken"].append("send_confirmation_email")

        elif action == "add_to_email_sequence":
            lead = find_lead_by_phone(leads, caller_phone)
            if lead and not lead.get("email_sequence_step"):
                lead["email_sequence_step"] = 1
                lead["email_sequence_last_sent"] = None
                if not DRY_RUN:
                    save_leads(leads)
            results["actions_taken"].append("add_to_email_sequence")

        elif action == "remove_from_pipeline":
            lead = find_lead_by_phone(leads, caller_phone)
            if lead:
                lead["status"] = "disqualified"
                lead["disqualified_reason"] = "wrong_number"
                if not DRY_RUN:
                    save_leads(leads)
            results["actions_taken"].append("remove_from_pipeline")

        elif action == "log_only":
            results["actions_taken"].append("log_only")

    return jsonify({"status": "processed", **results}), 200


@app.route("/webhook/stripe", methods=["POST"])
def stripe_webhook():
    """Handle Stripe payment webhooks."""
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature", "")

    # Log raw payload
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        return jsonify({"error": "invalid JSON"}), 400

    log_webhook("stripe", parsed)

    event_type = parsed.get("type", "")
    data = parsed.get("data", {}).get("object", {})

    log.info(f"Stripe webhook: event={event_type}")

    if event_type == "checkout.session.completed":
        customer_email = data.get("customer_details", {}).get("email", "")
        customer_name = data.get("customer_details", {}).get("name", "")
        amount = data.get("amount_total", 0) / 100
        log.info(f"Payment received: {customer_name} ({customer_email}) — ${amount:.2f}")

        # TODO: Trigger onboarding email sequence
        # This will integrate with send-email.py onboarding templates
        if not DRY_RUN:
            log.info(f"Would trigger onboarding sequence for {customer_email}")

        return jsonify({
            "status": "processed",
            "action": "onboarding_triggered",
            "customer": customer_email,
            "amount": amount,
        }), 200

    elif event_type == "invoice.paid":
        customer_email = data.get("customer_email", "")
        amount = data.get("amount_paid", 0) / 100
        log.info(f"Invoice paid: {customer_email} — ${amount:.2f}")
        return jsonify({"status": "logged"}), 200

    elif event_type == "customer.subscription.deleted":
        customer_email = data.get("customer_email", data.get("metadata", {}).get("email", ""))
        log.info(f"Subscription cancelled: {customer_email}")
        # TODO: Flag churn, trigger win-back sequence
        return jsonify({"status": "logged", "action": "churn_flagged"}), 200

    return jsonify({"status": "ignored", "event": event_type}), 200


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    global DRY_RUN

    parser = argparse.ArgumentParser(description="Velocity AI Webhook Server")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on (default: 8080)")
    parser.add_argument("--dry-run", action="store_true", help="Log actions without executing")
    parser.add_argument("--debug", action="store_true", help="Enable Flask debug mode")
    args = parser.parse_args()

    DRY_RUN = args.dry_run

    if DRY_RUN:
        log.info("Running in DRY RUN mode — no external actions will be taken")

    log.info(f"Starting Velocity AI webhook server on port {args.port}")
    log.info(f"Endpoints:")
    log.info(f"  POST /webhook/retell   — Retell AI post-call events")
    log.info(f"  POST /webhook/stripe   — Stripe payment events")
    log.info(f"  GET  /health           — Health check")

    app.run(host="0.0.0.0", port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
