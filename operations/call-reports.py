#!/usr/bin/env python3
"""
Velocity AI — Call Summary Reports & Discovery Call Prep Sheets

Usage:
    python call-reports.py recent                      # Print summaries of recent calls
    python call-reports.py recent --limit 5            # Last 5 calls
    python call-reports.py recent --save               # Save to markdown file
    python call-reports.py prep "caller name"          # Prep sheet for a specific lead
    python call-reports.py prep "caller name" --email  # Email the prep sheet to Mitchell
    python call-reports.py email-summary               # Email today's call summary to Mitchell
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system(f"{sys.executable} -m pip install requests --break-system-packages -q")
    import requests

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
RETELL_API_KEY = os.environ.get("RETELL_API_KEY", "")
RETELL_BASE_URL = "https://api.retellai.com"
AGENT_ID = os.environ.get("RETELL_REPORT_AGENT_ID", "agent_d20f1e490c9505de0d6453aafa")

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
MITCHELL_EMAIL = os.environ.get("MITCHELL_EMAIL", "mitchpearce94@gmail.com")
FROM_EMAIL = "reports@velocityai.com.au"

RETELL_HEADERS = {
    "Authorization": f"Bearer {RETELL_API_KEY}",
    "Content-Type": "application/json",
}


# ---------------------------------------------------------------------------
# Retell API helpers
# ---------------------------------------------------------------------------
def list_calls(limit: int = 20, sort_order: str = "descending") -> list:
    """Fetch recent calls from Retell API."""
    payload = {
        "limit": limit,
        "sort_order": sort_order,
        "filter_criteria": {
            "agent_id": [AGENT_ID],
        },
    }
    resp = requests.post(
        f"{RETELL_BASE_URL}/v2/list-calls",
        headers=RETELL_HEADERS,
        json=payload,
    )
    resp.raise_for_status()
    return resp.json()


def get_call(call_id: str) -> dict:
    """Get a single call's full details."""
    resp = requests.get(
        f"{RETELL_BASE_URL}/v2/get-call/{call_id}",
        headers=RETELL_HEADERS,
    )
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------
def ms_to_datetime(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)


def format_duration(ms: int) -> str:
    total_seconds = ms // 1000
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes}m {seconds}s"


def safe(val, fallback="—"):
    """Return val if truthy, else fallback."""
    if val is None or val == "":
        return fallback
    return val


def format_call_summary(call: dict) -> str:
    """Format a single call into a readable markdown summary."""
    analysis = call.get("call_analysis") or {}
    pca = call.get("post_call_analysis") or {}

    call_id = call.get("call_id", "unknown")
    start = ms_to_datetime(call["start_timestamp"]) if call.get("start_timestamp") else None
    duration = format_duration(call.get("duration_ms", 0))
    date_str = start.strftime("%a %d %b %Y, %I:%M %p UTC") if start else "Unknown"

    caller_name = safe(pca.get("caller_name"))
    business = safe(pca.get("business_name"))
    trade = safe(pca.get("trade_type"))
    employees = safe(pca.get("employee_count"))
    tools = safe(pca.get("current_tools"))
    pain_points = safe(pca.get("pain_points"))
    services = safe(pca.get("services_interested_in"))
    objections = safe(pca.get("objections_raised"))
    booked = safe(pca.get("discovery_call_booked"))
    booked_time = safe(pca.get("discovery_call_datetime"))
    phone = safe(pca.get("contact_phone"))
    email = safe(pca.get("contact_email"))
    source = safe(pca.get("referral_source"))
    tone = safe(pca.get("caller_tone"))
    projects = safe(pca.get("projects_and_timelines"))
    disposition = safe(pca.get("call_disposition"))
    summary = safe(pca.get("conversation_summary"))

    # Also pull from call_analysis if post_call_analysis is sparse
    user_sentiment = safe(analysis.get("user_sentiment"))
    call_summary_fallback = safe(analysis.get("call_summary"))
    if summary == "—" and call_summary_fallback != "—":
        summary = call_summary_fallback

    lines = [
        f"### {caller_name} — {business}",
        f"**Date:** {date_str}  |  **Duration:** {duration}  |  **ID:** `{call_id}`",
        "",
        f"| Field | Detail |",
        f"|---|---|",
        f"| **Trade** | {trade} |",
        f"| **Employees** | {employees} |",
        f"| **Phone** | {phone} |",
        f"| **Email** | {email} |",
        f"| **Referral Source** | {source} |",
        f"| **Caller Tone** | {tone} |",
        f"| **Disposition** | {disposition} |",
        f"| **Discovery Call Booked** | {booked} |",
        f"| **Booked For** | {booked_time} |",
        "",
        f"**Current Tools/Software:** {tools}",
        "",
        f"**Pain Points:** {pain_points}",
        "",
        f"**Services Interested In:** {services}",
        "",
        f"**Objections & Handling:** {objections}",
        "",
        f"**Projects & Timelines:** {projects}",
        "",
        f"**Conversation Summary:** {summary}",
        "",
        "---",
        "",
    ]
    return "\n".join(lines)


def format_prep_sheet(calls: list, lead_name: str) -> str:
    """Generate a discovery call prep sheet from all calls matching a lead name."""
    matching = []
    for call in calls:
        pca = call.get("post_call_analysis") or {}
        name = (pca.get("caller_name") or "").lower()
        if lead_name.lower() in name:
            matching.append(call)

    if not matching:
        return f"No calls found matching '{lead_name}'."

    # Sort oldest first for chronological context
    matching.sort(key=lambda c: c.get("start_timestamp", 0))

    latest = matching[-1]
    pca = latest.get("post_call_analysis") or {}
    analysis = latest.get("call_analysis") or {}

    caller_name = safe(pca.get("caller_name"))
    business = safe(pca.get("business_name"))
    trade = safe(pca.get("trade_type"))

    lines = [
        f"# Discovery Call Prep Sheet — {caller_name}",
        f"**Prepared:** {datetime.now().strftime('%a %d %b %Y, %I:%M %p')}",
        "",
        "---",
        "",
        "## Lead Snapshot",
        "",
        f"| | |",
        f"|---|---|",
        f"| **Name** | {caller_name} |",
        f"| **Business** | {business} |",
        f"| **Trade** | {trade} |",
        f"| **Employees** | {safe(pca.get('employee_count'))} |",
        f"| **Phone** | {safe(pca.get('contact_phone'))} |",
        f"| **Email** | {safe(pca.get('contact_email'))} |",
        f"| **Heard About Us** | {safe(pca.get('referral_source'))} |",
        f"| **Caller Tone** | {safe(pca.get('caller_tone'))} |",
        f"| **Total Calls with Ava** | {len(matching)} |",
        "",
        "---",
        "",
        "## What They're Dealing With",
        "",
        f"**Pain Points:** {safe(pca.get('pain_points'))}",
        "",
        f"**Current Tools:** {safe(pca.get('current_tools'))}",
        "",
        f"**Projects & Timelines:** {safe(pca.get('projects_and_timelines'))}",
        "",
        "---",
        "",
        "## What They're Interested In",
        "",
        f"{safe(pca.get('services_interested_in'))}",
        "",
        "---",
        "",
        "## Objections to Be Aware Of",
        "",
        f"{safe(pca.get('objections_raised'))}",
        "",
        "---",
        "",
        "## Conversation History",
        "",
    ]

    for i, call in enumerate(matching, 1):
        c_pca = call.get("post_call_analysis") or {}
        c_analysis = call.get("call_analysis") or {}
        start = ms_to_datetime(call["start_timestamp"]) if call.get("start_timestamp") else None
        date_str = start.strftime("%a %d %b %Y, %I:%M %p UTC") if start else "Unknown"
        duration = format_duration(call.get("duration_ms", 0))
        summary = safe(c_pca.get("conversation_summary"))
        if summary == "—":
            summary = safe(c_analysis.get("call_summary"))

        lines.extend([
            f"### Call {i} — {date_str} ({duration})",
            "",
            f"{summary}",
            "",
        ])

    lines.extend([
        "---",
        "",
        "## Suggested Talking Points",
        "",
        "- Reference their specific pain points to show you listened",
        "- Address the objections Ava noted — come prepared with answers",
        "- Ask about any timelines or projects they mentioned to create urgency",
        "- Tailor the demo to the services they showed interest in",
        f"- They heard about us via {safe(pca.get('referral_source')).lower()} — acknowledge that",
        "",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Email via Resend
# ---------------------------------------------------------------------------
def send_email(subject: str, body_markdown: str):
    """Send an email via Resend API with the given markdown body as HTML."""
    # Convert basic markdown to HTML for email
    html = markdown_to_html(body_markdown)

    resp = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": FROM_EMAIL,
            "to": [MITCHELL_EMAIL],
            "subject": subject,
            "html": html,
        },
    )
    if resp.status_code in (200, 201):
        print(f"Email sent to {MITCHELL_EMAIL}")
    else:
        print(f"Email failed ({resp.status_code}): {resp.text}")
    return resp


def markdown_to_html(md: str) -> str:
    """Minimal markdown-to-HTML conversion for email readability."""
    import re

    lines = md.split("\n")
    html_lines = []
    in_table = False

    for line in lines:
        stripped = line.strip()

        # Headings
        if stripped.startswith("### "):
            html_lines.append(f"<h3>{stripped[4:]}</h3>")
            continue
        elif stripped.startswith("## "):
            html_lines.append(f"<h2>{stripped[3:]}</h2>")
            continue
        elif stripped.startswith("# "):
            html_lines.append(f"<h1>{stripped[2:]}</h1>")
            continue

        # Horizontal rule
        if stripped == "---":
            if in_table:
                html_lines.append("</table>")
                in_table = False
            html_lines.append("<hr>")
            continue

        # Table rows
        if "|" in stripped and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            # Skip separator rows
            if all(set(c) <= {"-", ":"} for c in cells):
                continue
            if not in_table:
                html_lines.append('<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;">')
                in_table = True
            html_lines.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
            continue

        if in_table:
            html_lines.append("</table>")
            in_table = False

        # Bold
        stripped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", stripped)

        # Backticks
        stripped = re.sub(r"`(.+?)`", r"<code>\1</code>", stripped)

        # List items
        if stripped.startswith("- "):
            html_lines.append(f"<li>{stripped[2:]}</li>")
            continue

        # Empty lines
        if not stripped:
            html_lines.append("<br>")
            continue

        html_lines.append(f"<p>{stripped}</p>")

    if in_table:
        html_lines.append("</table>")

    return "\n".join(html_lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def cmd_recent(args):
    """Show recent call summaries."""
    print("Fetching recent calls...")
    calls = list_calls(limit=args.limit)

    if not calls:
        print("No calls found.")
        return

    header = f"# Velocity AI — Call Summaries\n**Generated:** {datetime.now().strftime('%a %d %b %Y, %I:%M %p')}\n\n---\n\n"
    body = header

    for call in calls:
        body += format_call_summary(call)

    if args.save:
        filename = f"call-summaries-{datetime.now().strftime('%Y-%m-%d')}.md"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, "w") as f:
            f.write(body)
        print(f"Saved to {filepath}")
    else:
        print(body)


def cmd_prep(args):
    """Generate a prep sheet for a specific lead."""
    print(f"Searching for calls from '{args.name}'...")
    calls = list_calls(limit=50)
    sheet = format_prep_sheet(calls, args.name)

    if args.email:
        pca = {}
        for call in calls:
            p = call.get("post_call_analysis") or {}
            if args.name.lower() in (p.get("caller_name") or "").lower():
                pca = p
                break
        subject = f"Prep Sheet — {safe(pca.get('caller_name', args.name))} @ {safe(pca.get('business_name', 'Unknown'))}"
        send_email(subject, sheet)

    if args.save:
        filename = f"prep-{args.name.lower().replace(' ', '-')}-{datetime.now().strftime('%Y-%m-%d')}.md"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, "w") as f:
            f.write(sheet)
        print(f"Saved to {filepath}")
    else:
        print(sheet)


def cmd_email_summary(args):
    """Email today's call summary to Mitchell."""
    print("Fetching calls and sending summary...")
    calls = list_calls(limit=args.limit)

    if not calls:
        print("No calls found.")
        return

    header = f"# Velocity AI — Call Summary Report\n**Generated:** {datetime.now().strftime('%a %d %b %Y, %I:%M %p')}\n\n---\n\n"
    body = header

    for call in calls:
        body += format_call_summary(call)

    subject = f"Ava Call Summary — {datetime.now().strftime('%a %d %b %Y')}"
    send_email(subject, body)


def main():
    parser = argparse.ArgumentParser(
        description="Velocity AI — Call Reports & Prep Sheets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # recent
    p_recent = subparsers.add_parser("recent", help="Show recent call summaries")
    p_recent.add_argument("--limit", type=int, default=10, help="Number of calls to fetch (default: 10)")
    p_recent.add_argument("--save", action="store_true", help="Save to a markdown file")

    # prep
    p_prep = subparsers.add_parser("prep", help="Generate a discovery call prep sheet")
    p_prep.add_argument("name", help="Caller name to search for")
    p_prep.add_argument("--email", action="store_true", help="Email the prep sheet to Mitchell")
    p_prep.add_argument("--save", action="store_true", help="Save to a markdown file")

    # email-summary
    p_email = subparsers.add_parser("email-summary", help="Email today's call summary to Mitchell")
    p_email.add_argument("--limit", type=int, default=20, help="Number of calls to include (default: 20)")

    args = parser.parse_args()

    if args.command == "recent":
        cmd_recent(args)
    elif args.command == "prep":
        cmd_prep(args)
    elif args.command == "email-summary":
        cmd_email_summary(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
