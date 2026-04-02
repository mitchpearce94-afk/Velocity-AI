#!/usr/bin/env python3
"""
Velocity AI — Outbound Pipeline
================================
Connects the lead research task (leads.json) to the Retell AI outbound voice agent
and Resend email follow-up system.

Flow:
  1. Reads leads from leads.json
  2. Filters leads ready for outbound (new or due for follow-up)
  3. Initiates outbound calls via Retell AI
  4. Polls for call completion and logs results
  5. Queues no-answers / callbacks for follow-up
  6. Triggers email nurture via Resend for interested leads

Usage:
  python outbound-pipeline.py                  # Run full pipeline
  python outbound-pipeline.py --dry-run        # Preview without making calls
  python outbound-pipeline.py --status         # Show current lead statuses
  python outbound-pipeline.py --follow-ups     # Process only follow-up queue
"""

import json
import os
import sys
import time
import logging
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system(f"{sys.executable} -m pip install requests --quiet")
    import requests

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RETELL_API_KEY = os.environ.get("RETELL_API_KEY", "")
RETELL_API_BASE = "https://api.retellai.com"
RETELL_AGENT_IDS = os.environ.get("RETELL_AGENT_IDS", "").split(",") if os.environ.get("RETELL_AGENT_IDS") else []
RETELL_AGENT_ID = RETELL_AGENT_IDS[0]  # Primary agent

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
RESEND_API_BASE = "https://api.resend.com"

TWILIO_FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER", "")

# Paths (relative to this script)
SCRIPT_DIR = Path(__file__).resolve().parent
LEADS_FILE = SCRIPT_DIR / "leads.json"
CALL_LOG_FILE = SCRIPT_DIR / "call_log.json"
PIPELINE_LOG_FILE = SCRIPT_DIR / "pipeline.log"

# Timing constraints (ACMA compliance — Australian hours)
CALL_WINDOW_START_HOUR = 9   # 9:00 AM local
CALL_WINDOW_END_HOUR = 20    # 8:00 PM local
MAX_CALL_ATTEMPTS = 5
FOLLOW_UP_DELAYS = {
    1: timedelta(days=0),   # First attempt: immediate
    2: timedelta(days=2),   # Second attempt: 2 days later
    3: timedelta(days=5),   # Third attempt: 5 days later
    4: timedelta(days=7),   # Fourth attempt: 7 days later (+ email)
    5: timedelta(days=14),  # Final attempt: 14 days later
}

# Email settings
FROM_EMAIL = "ava@velocityai.com.au"
FROM_NAME = "Ava from Velocity AI"
REPLY_TO_EMAIL = "mitchell@velocityai.com.au"
BOOKING_LINK = "https://cal.com/mitchell-pearce/discovery-call"

# Email template paths
EMAIL_TEMPLATE_DIR = SCRIPT_DIR.parent / "emails" / "outbound-sequence"
SEQUENCE_CONFIG_FILE = EMAIL_TEMPLATE_DIR / "sequence-config.json"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(PIPELINE_LOG_FILE),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("outbound-pipeline")

# ---------------------------------------------------------------------------
# Timezone helper — AEST (UTC+10)
# ---------------------------------------------------------------------------

AEST = timezone(timedelta(hours=10))


def now_aest() -> datetime:
    return datetime.now(AEST)


def is_within_call_window() -> bool:
    """Check if current time is within ACMA-compliant calling hours."""
    current = now_aest()
    if current.weekday() >= 5:  # Saturday=5, Sunday=6
        log.info("Weekend — skipping calls (ACMA compliance)")
        return False
    if current.hour < CALL_WINDOW_START_HOUR or current.hour >= CALL_WINDOW_END_HOUR:
        log.info(f"Outside call window ({CALL_WINDOW_START_HOUR}:00–{CALL_WINDOW_END_HOUR}:00 AEST)")
        return False
    return True


# ---------------------------------------------------------------------------
# Leads management
# ---------------------------------------------------------------------------

def load_leads() -> list[dict]:
    """Load leads from JSON file."""
    if not LEADS_FILE.exists():
        log.error(f"Leads file not found: {LEADS_FILE}")
        return []
    with open(LEADS_FILE, "r") as f:
        leads = json.load(f)
    log.info(f"Loaded {len(leads)} leads from {LEADS_FILE.name}")
    return leads


def save_leads(leads: list[dict]) -> None:
    """Save leads back to JSON file."""
    with open(LEADS_FILE, "w") as f:
        json.dump(leads, f, indent=2, default=str)
    log.info(f"Saved {len(leads)} leads to {LEADS_FILE.name}")


def get_callable_leads(leads: list[dict]) -> list[dict]:
    """Filter leads that are ready to be called right now."""
    now = now_aest()
    callable_leads = []

    for lead in leads:
        # Skip terminal states
        if lead.get("disposition") in ("BOOKED", "NOT_INTERESTED", "DNC", "WRONG_NUMBER"):
            continue

        # Skip leads that have exhausted all attempts
        if lead.get("call_attempts", 0) >= MAX_CALL_ATTEMPTS:
            continue

        # New leads are always callable
        if lead.get("status") == "new":
            callable_leads.append(lead)
            continue

        # Follow-up leads: check if enough time has passed
        follow_up_at = lead.get("follow_up_at")
        if follow_up_at:
            follow_up_time = datetime.fromisoformat(follow_up_at)
            if now >= follow_up_time:
                callable_leads.append(lead)

    log.info(f"Found {len(callable_leads)} leads ready to call")
    return callable_leads


def get_follow_up_leads(leads: list[dict]) -> list[dict]:
    """Get leads that are in follow-up queue."""
    return [
        lead for lead in leads
        if lead.get("status") == "follow_up"
        and lead.get("disposition") in ("NO_ANSWER", "VOICEMAIL", "CALLBACK", "GATEKEEPER")
        and lead.get("call_attempts", 0) < MAX_CALL_ATTEMPTS
    ]


# ---------------------------------------------------------------------------
# Call logging
# ---------------------------------------------------------------------------

def log_call(lead: dict, call_id: str, disposition: str, duration: float,
             notes: str = "") -> None:
    """Append a call record to the call log."""
    call_record = {
        "call_id": call_id,
        "lead_id": lead["id"],
        "contact_name": lead.get("contact_name"),
        "business_name": lead.get("business_name"),
        "phone": lead.get("phone"),
        "disposition": disposition,
        "duration_seconds": duration,
        "attempt_number": lead.get("call_attempts", 0),
        "timestamp": now_aest().isoformat(),
        "notes": notes,
    }

    call_log = []
    if CALL_LOG_FILE.exists():
        with open(CALL_LOG_FILE, "r") as f:
            call_log = json.load(f)

    call_log.append(call_record)

    with open(CALL_LOG_FILE, "w") as f:
        json.dump(call_log, f, indent=2, default=str)

    log.info(
        f"Logged call: {lead['business_name']} -> {disposition} "
        f"(attempt {lead.get('call_attempts', 0)}, {duration:.0f}s)"
    )


# ---------------------------------------------------------------------------
# Retell AI integration
# ---------------------------------------------------------------------------

def retell_headers() -> dict:
    return {
        "Authorization": f"Bearer {RETELL_API_KEY}",
        "Content-Type": "application/json",
    }


def initiate_call(lead: dict, dry_run: bool = False) -> Optional[str]:
    """
    Initiate an outbound call via Retell AI.
    Returns the call_id on success, None on failure.
    """
    phone = lead.get("phone")
    if not phone:
        log.warning(f"No phone number for lead {lead['id']} — skipping")
        return None

    # Build dynamic variables for the agent prompt
    retell_dynamic_variables = {
        "contact_name": lead.get("contact_name", ""),
        "business_name": lead.get("business_name", ""),
        "trade_type": lead.get("trade_type", "trade"),
        "location": lead.get("location", ""),
        "lead_source": lead.get("lead_source", "online directory"),
        "callback_number": TWILIO_FROM_NUMBER,
        "contact_phone": phone,
    }

    payload = {
        "agent_id": RETELL_AGENT_ID,
        "from_number": TWILIO_FROM_NUMBER,
        "to_number": phone,
        "retell_llm_dynamic_variables": retell_dynamic_variables,
        "metadata": {
            "lead_id": lead["id"],
            "attempt_number": lead.get("call_attempts", 0) + 1,
            "pipeline_run": now_aest().isoformat(),
        },
    }

    if dry_run:
        log.info(f"[DRY RUN] Would call {lead['business_name']} at {phone}")
        log.info(f"[DRY RUN] Payload: {json.dumps(payload, indent=2)}")
        return "dry_run_call_id"

    try:
        log.info(f"Initiating call to {lead['business_name']} ({phone})...")
        resp = requests.post(
            f"{RETELL_API_BASE}/v2/create-phone-call",
            headers=retell_headers(),
            json=payload,
            timeout=30,
        )

        if resp.status_code == 201 or resp.status_code == 200:
            data = resp.json()
            call_id = data.get("call_id")
            log.info(f"Call initiated: {call_id}")
            return call_id
        else:
            log.error(f"Retell API error {resp.status_code}: {resp.text}")
            return None

    except requests.RequestException as e:
        log.error(f"Failed to initiate call to {lead['business_name']}: {e}")
        return None


def get_call_status(call_id: str) -> Optional[dict]:
    """Poll Retell API for call status and result."""
    try:
        resp = requests.get(
            f"{RETELL_API_BASE}/v2/get-call/{call_id}",
            headers=retell_headers(),
            timeout=15,
        )
        if resp.status_code == 200:
            return resp.json()
        else:
            log.error(f"Failed to get call status for {call_id}: {resp.status_code}")
            return None
    except requests.RequestException as e:
        log.error(f"Error polling call status: {e}")
        return None


def wait_for_call_completion(call_id: str, timeout_seconds: int = 600,
                             poll_interval: int = 10) -> Optional[dict]:
    """Wait for a call to complete, polling at intervals."""
    start = time.time()
    while time.time() - start < timeout_seconds:
        status = get_call_status(call_id)
        if status and status.get("call_status") in ("ended", "error"):
            return status
        time.sleep(poll_interval)

    log.warning(f"Call {call_id} timed out after {timeout_seconds}s")
    return None


def map_retell_to_disposition(call_data: dict) -> str:
    """
    Map Retell AI call result data to our disposition codes.
    Uses call analysis and disconnection reason to determine outcome.
    """
    if not call_data:
        return "NO_ANSWER"

    call_status = call_data.get("call_status", "")
    disconnection_reason = call_data.get("disconnection_reason", "")
    call_analysis = call_data.get("call_analysis", {}) or {}

    # Call never connected
    if disconnection_reason in ("no_answer", "dial_no_answer"):
        return "NO_ANSWER"
    if disconnection_reason in ("busy", "dial_busy"):
        return "NO_ANSWER"
    if disconnection_reason in ("voicemail_reached",):
        return "VOICEMAIL"
    if disconnection_reason in ("invalid_number", "number_not_in_service"):
        return "WRONG_NUMBER"

    # Call connected — analyse the conversation
    user_sentiment = call_analysis.get("user_sentiment", "")
    call_successful = call_analysis.get("call_successful", False)

    # Check custom data from the agent
    custom_data = call_analysis.get("custom_analysis_data", {}) or {}
    agent_disposition = custom_data.get("disposition", "").upper()

    # If the agent explicitly set a disposition, use it
    if agent_disposition in ("BOOKED", "CALLBACK", "INTERESTED", "NOT_INTERESTED",
                              "DNC", "GATEKEEPER"):
        return agent_disposition

    # Fallback heuristics
    if call_successful:
        return "INTERESTED"
    if user_sentiment == "Negative":
        return "NOT_INTERESTED"
    if disconnection_reason == "agent_hangup":
        return "INTERESTED"
    if disconnection_reason == "user_hangup":
        # Short call + user hangup = not interested
        duration = call_data.get("duration_ms", 0) / 1000
        if duration < 15:
            return "NOT_INTERESTED"
        return "CALLBACK"

    return "NO_ANSWER"


# ---------------------------------------------------------------------------
# Follow-up scheduling
# ---------------------------------------------------------------------------

def schedule_follow_up(lead: dict) -> None:
    """Set the next follow-up time based on attempt count."""
    attempt = lead.get("call_attempts", 0)
    next_attempt = attempt + 1

    if next_attempt > MAX_CALL_ATTEMPTS:
        lead["status"] = "exhausted"
        lead["follow_up_at"] = None
        log.info(f"{lead['business_name']}: Max attempts reached — moving to nurture list")
        return

    delay = FOLLOW_UP_DELAYS.get(next_attempt, timedelta(days=7))
    follow_up_time = now_aest() + delay
    lead["follow_up_at"] = follow_up_time.isoformat()
    lead["status"] = "follow_up"
    log.info(
        f"{lead['business_name']}: Follow-up #{next_attempt} scheduled for "
        f"{follow_up_time.strftime('%a %d %b at %I:%M %p')}"
    )


# ---------------------------------------------------------------------------
# Resend email integration
# ---------------------------------------------------------------------------

def resend_headers() -> dict:
    return {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json",
    }


def load_sequence_config() -> dict:
    """Load the email sequence configuration from sequence-config.json."""
    if not SEQUENCE_CONFIG_FILE.exists():
        log.error(f"Sequence config not found: {SEQUENCE_CONFIG_FILE}")
        return {}
    with open(SEQUENCE_CONFIG_FILE, "r") as f:
        return json.load(f)


def load_email_template(template_filename: str) -> Optional[str]:
    """Load an HTML email template from the outbound-sequence directory."""
    template_path = EMAIL_TEMPLATE_DIR / template_filename
    if not template_path.exists():
        log.error(f"Email template not found: {template_path}")
        return None
    with open(template_path, "r") as f:
        return f.read()


def substitute_placeholders(html: str, lead: dict) -> str:
    """
    Replace {{placeholders}} in an email template with actual lead data.
    Supported: {{contact_name}}, {{business_name}}, {{trade_type}}.
    """
    first_name = (lead.get("contact_name") or "").split()[0] if lead.get("contact_name") else "there"
    replacements = {
        "{{contact_name}}": first_name,
        "{{business_name}}": lead.get("business_name", "your business"),
        "{{trade_type}}": lead.get("trade_type", "trade").lower(),
    }
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)
    return html


def resolve_subject_line(email_config: dict, lead: dict) -> str:
    """
    Pick the right subject line from the email config based on lead disposition.
    Falls back to 'default' if no disposition-specific variant exists.
    """
    subject_lines = email_config.get("subject_lines", {})
    disposition = (lead.get("disposition") or "").upper()

    # Map dispositions to subject line keys
    disposition_key_map = {
        "VOICEMAIL": "voicemail",
        "NO_ANSWER": "voicemail",
        "INTERESTED": "interested_thinking",
        "CALLBACK": "conversation_no_book",
    }
    key = disposition_key_map.get(disposition, "default")
    subject = subject_lines.get(key) or subject_lines.get("default", "Following up — Velocity AI")

    # Substitute placeholders in subject line too
    first_name = (lead.get("contact_name") or "").split()[0] if lead.get("contact_name") else "there"
    subject = subject.replace("{{contact_name}}", first_name)
    subject = subject.replace("{{business_name}}", lead.get("business_name", "your business"))
    subject = subject.replace("{{trade_type}}", lead.get("trade_type", "trade").lower())
    return subject


def get_next_sequence_email(lead: dict, sequence_config: dict) -> Optional[dict]:
    """
    Determine which email in the sequence to send next for a given lead.
    Returns the email config dict, or None if the sequence is complete or
    should be skipped.
    """
    step = lead.get("email_sequence_step", 0)
    disposition = (lead.get("disposition") or "").upper()
    emails = sequence_config.get("emails", [])

    # Check global stop rules
    stop_on = sequence_config.get("global_rules", {}).get("stop_sequence_on", [])
    if disposition in stop_on:
        log.info(f"{lead['business_name']}: Sequence stopped — disposition is {disposition}")
        return None

    if step >= len(emails):
        log.info(f"{lead['business_name']}: Sequence complete (all {len(emails)} emails sent)")
        return None

    email_config = emails[step]

    # Check skip conditions for this email
    skip_if = email_config.get("skip_if", [])
    if disposition in skip_if:
        log.info(f"{lead['business_name']}: Skipping {email_config['id']} — disposition {disposition} in skip_if")
        return None

    # Check if disposition is in the trigger list
    trigger_dispositions = email_config.get("trigger_dispositions", [])
    if trigger_dispositions and disposition not in trigger_dispositions:
        log.info(f"{lead['business_name']}: Skipping {email_config['id']} — disposition {disposition} not in triggers")
        return None

    return email_config


def send_sequence_email(lead: dict, dry_run: bool = False) -> bool:
    """
    Send the next email in the nurture sequence for a lead.
    Loads the template from file, substitutes placeholders, and sends via Resend.
    Updates lead tracking fields on success.
    """
    email_address = lead.get("email")
    if not email_address:
        log.warning(f"No email for {lead['business_name']} — cannot send sequence email")
        return False

    # Load sequence config
    sequence_config = load_sequence_config()
    if not sequence_config:
        return False

    # Determine which email to send
    email_config = get_next_sequence_email(lead, sequence_config)
    if not email_config:
        return False

    step = lead.get("email_sequence_step", 0)
    template_file = email_config.get("template")
    email_id = email_config.get("id", f"email-{step + 1}")

    # Load and personalise the template
    html_body = load_email_template(template_file)
    if not html_body:
        log.error(f"Failed to load template {template_file} for {lead['business_name']}")
        return False

    html_body = substitute_placeholders(html_body, lead)
    subject = resolve_subject_line(email_config, lead)

    log.info(f"Sending {email_id} (step {step + 1}/5) to {lead['business_name']} ({email_address})")

    payload = {
        "from": f"{FROM_NAME} <{FROM_EMAIL}>",
        "reply_to": REPLY_TO_EMAIL,
        "to": [email_address],
        "subject": subject,
        "html": html_body,
        "tags": [
            {"name": "campaign", "value": "outbound-cold-nurture"},
            {"name": "lead_id", "value": lead["id"]},
            {"name": "sequence_step", "value": str(step + 1)},
            {"name": "email_id", "value": email_id},
        ],
    }

    if dry_run:
        log.info(f"[DRY RUN] Would send {email_id} to {email_address} — subject: {subject}")
        # Still update tracking in dry-run so the pipeline logic flows correctly
        lead["email_sequence_started"] = True
        lead["email_sequence_step"] = step + 1
        lead["email_sequence_last_sent"] = now_aest().isoformat()
        return True

    try:
        resp = requests.post(
            f"{RESEND_API_BASE}/emails",
            headers=resend_headers(),
            json=payload,
            timeout=15,
        )
        if resp.status_code in (200, 201):
            data = resp.json()
            log.info(f"Email sent: {email_id} to {email_address} (Resend ID: {data.get('id', 'unknown')})")
            # Update sequence tracking on the lead
            lead["email_sequence_started"] = True
            lead["email_sequence_step"] = step + 1
            lead["email_sequence_last_sent"] = now_aest().isoformat()
            return True
        else:
            log.error(f"Resend API error {resp.status_code}: {resp.text}")
            return False
    except requests.RequestException as e:
        log.error(f"Failed to send email to {email_address}: {e}")
        return False


# ---------------------------------------------------------------------------
# Pipeline orchestration
# ---------------------------------------------------------------------------

def process_lead(lead: dict, dry_run: bool = False) -> str:
    """
    Process a single lead through the outbound pipeline.
    Returns the disposition code.
    """
    lead_label = f"{lead.get('business_name', 'Unknown')} ({lead.get('contact_name', 'No name')})"
    attempt = lead.get("call_attempts", 0) + 1
    log.info(f"--- Processing: {lead_label} (attempt #{attempt}) ---")

    # Initiate the call
    call_id = initiate_call(lead, dry_run=dry_run)

    if not call_id:
        log.warning(f"Could not initiate call to {lead_label}")
        schedule_follow_up(lead)
        lead["call_attempts"] = attempt
        return "FAILED"

    if dry_run:
        # Don't mutate lead data in dry-run mode
        return "DRY_RUN"

    # Wait for the call to complete
    log.info(f"Waiting for call {call_id} to complete...")
    call_data = wait_for_call_completion(call_id)

    # Determine disposition
    disposition = map_retell_to_disposition(call_data)
    duration = (call_data.get("duration_ms", 0) / 1000) if call_data else 0

    # Update lead record
    lead["call_attempts"] = attempt
    lead["last_call_at"] = now_aest().isoformat()
    lead["disposition"] = disposition

    # Log the call
    log_call(
        lead=lead,
        call_id=call_id,
        disposition=disposition,
        duration=duration,
        notes=call_data.get("call_analysis", {}).get("call_summary", "") if call_data else "",
    )

    # Route based on disposition
    if disposition == "BOOKED":
        lead["status"] = "booked"
        log.info(f"BOOKED: {lead_label} — discovery call booked!")
        # Send confirmation email if we have an address
        if lead.get("email"):
            send_sequence_email(lead, dry_run=dry_run)

    elif disposition == "INTERESTED":
        lead["status"] = "interested"
        log.info(f"INTERESTED: {lead_label} — sending follow-up email")
        if lead.get("email") and lead.get("email_sequence_step", 0) == 0:
            send_sequence_email(lead, dry_run=dry_run)
        schedule_follow_up(lead)

    elif disposition in ("NO_ANSWER", "VOICEMAIL"):
        log.info(f"{disposition}: {lead_label} — scheduling follow-up")
        schedule_follow_up(lead)
        # After 3rd attempt with no answer, start email sequence if available
        if attempt >= 3 and lead.get("email") and lead.get("email_sequence_step", 0) == 0:
            log.info(f"Attempt #{attempt} — triggering email sequence for {lead_label}")
            send_sequence_email(lead, dry_run=dry_run)

    elif disposition == "CALLBACK":
        lead["status"] = "follow_up"
        log.info(f"CALLBACK: {lead_label} — scheduling callback")
        schedule_follow_up(lead)

    elif disposition == "GATEKEEPER":
        log.info(f"GATEKEEPER: {lead_label} — will try again at a different time")
        schedule_follow_up(lead)

    elif disposition == "NOT_INTERESTED":
        lead["status"] = "nurture"
        log.info(f"NOT_INTERESTED: {lead_label} — moved to nurture list")

    elif disposition == "DNC":
        lead["status"] = "dnc"
        lead["follow_up_at"] = None
        log.info(f"DNC: {lead_label} — removed from outbound list")

    elif disposition == "WRONG_NUMBER":
        lead["status"] = "invalid"
        lead["follow_up_at"] = None
        log.info(f"WRONG_NUMBER: {lead_label} — marked as invalid")

    return disposition


def run_pipeline(dry_run: bool = False, follow_ups_only: bool = False) -> dict:
    """
    Run the full outbound pipeline.
    Returns a summary of results.
    """
    log.info("=" * 60)
    log.info(f"OUTBOUND PIPELINE RUN — {now_aest().strftime('%A %d %B %Y, %I:%M %p AEST')}")
    log.info(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log.info("=" * 60)

    # Check calling hours (skip for dry runs)
    if not dry_run and not is_within_call_window():
        log.warning("Outside calling hours — aborting pipeline run")
        return {"status": "skipped", "reason": "outside_call_window"}

    # Load leads
    leads = load_leads()
    if not leads:
        log.warning("No leads found — nothing to do")
        return {"status": "skipped", "reason": "no_leads"}

    # Get callable leads
    if follow_ups_only:
        to_call = get_follow_up_leads(leads)
        log.info(f"Processing follow-ups only: {len(to_call)} leads")
    else:
        to_call = get_callable_leads(leads)

    if not to_call:
        log.info("No leads ready to call right now")
        save_leads(leads)
        return {"status": "completed", "calls_made": 0}

    # Process each lead
    results = {
        "calls_made": 0,
        "dispositions": {},
        "emails_sent": 0,
    }

    for lead in to_call:
        disposition = process_lead(lead, dry_run=dry_run)
        results["calls_made"] += 1
        results["dispositions"][disposition] = results["dispositions"].get(disposition, 0) + 1

        # Brief pause between calls to avoid rate limiting
        if not dry_run and lead != to_call[-1]:
            log.info("Pausing 5 seconds before next call...")
            time.sleep(5)

    # Save updated leads
    save_leads(leads)

    # Summary
    log.info("=" * 60)
    log.info("PIPELINE RUN COMPLETE")
    log.info(f"Calls made: {results['calls_made']}")
    for disp, count in results["dispositions"].items():
        log.info(f"  {disp}: {count}")
    log.info("=" * 60)

    results["status"] = "completed"
    return results


def print_status() -> None:
    """Print a summary of all lead statuses."""
    leads = load_leads()
    if not leads:
        print("No leads found.")
        return

    status_counts: dict[str, int] = {}
    disposition_counts: dict[str, int] = {}

    print(f"\n{'='*80}")
    print(f"  VELOCITY AI — OUTBOUND PIPELINE STATUS")
    print(f"  {now_aest().strftime('%A %d %B %Y, %I:%M %p AEST')}")
    print(f"{'='*80}\n")

    print(f"  {'Lead':<30} {'Status':<15} {'Disp':<15} {'Attempts':<10} {'Follow-up':<20}")
    print(f"  {'-'*30} {'-'*15} {'-'*15} {'-'*10} {'-'*20}")

    for lead in leads:
        status = lead.get("status", "unknown")
        disposition = lead.get("disposition") or "—"
        attempts = lead.get("call_attempts", 0)
        follow_up = lead.get("follow_up_at") or "—"

        if follow_up and follow_up != "—":
            try:
                fu_dt = datetime.fromisoformat(follow_up)
                follow_up = fu_dt.strftime("%d %b %I:%M %p")
            except (ValueError, TypeError):
                pass

        name = lead.get("business_name", "Unknown")[:28]
        print(f"  {name:<30} {status:<15} {disposition or '—':<15} {attempts:<10} {follow_up:<20}")

        status_counts[status] = status_counts.get(status, 0) + 1
        if disposition:
            disposition_counts[disposition] = disposition_counts.get(disposition, 0) + 1

    print(f"\n  {'Summary':}")
    print(f"  Total leads: {len(leads)}")
    for s, c in sorted(status_counts.items()):
        print(f"    {s}: {c}")
    print()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    global LEADS_FILE, RETELL_AGENT_ID

    parser = argparse.ArgumentParser(
        description="Velocity AI Outbound Pipeline — Retell AI + Resend integration"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview pipeline actions without making real calls or sending emails",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current lead statuses and exit",
    )
    parser.add_argument(
        "--follow-ups",
        action="store_true",
        help="Process only leads in the follow-up queue",
    )
    parser.add_argument(
        "--leads-file",
        type=str,
        help="Path to leads JSON file (default: leads.json in same directory)",
    )
    parser.add_argument(
        "--agent-id",
        type=str,
        choices=RETELL_AGENT_IDS,
        default=RETELL_AGENT_ID,
        help="Retell agent ID to use for calls",
    )

    args = parser.parse_args()

    # Override paths if specified
    if args.leads_file:
        LEADS_FILE = Path(args.leads_file)
    if args.agent_id:
        RETELL_AGENT_ID = args.agent_id

    if args.status:
        print_status()
        return

    results = run_pipeline(dry_run=args.dry_run, follow_ups_only=args.follow_ups)

    if results.get("status") == "skipped":
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()
