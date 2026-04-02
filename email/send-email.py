#!/usr/bin/env python3
"""
Velocity AI — Email Sending Utility
====================================
Send branded emails via the Resend API using pre-built HTML templates.

Usage:
    python send-email.py welcome --to "jane@example.com" --first-name "Jane"
    python send-email.py discovery --to "jane@example.com" --first-name "Jane" --call-date "Wednesday, 9 April 2026" --call-time "10:00 AM"
    python send-email.py followup --to "jane@example.com" --first-name "Jane" --company-name "Acme Co"
    python send-email.py test --to "mitchell@velocityai.com.au"

Requirements:
    pip install resend
"""

import argparse
import os
import sys
import re

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
except ImportError:
    pass

import resend

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")

# Sender addresses (per resend-setup-guide.md)
SENDERS = {
    "welcome": "Velocity AI <hello@velocityai.com.au>",
    "discovery": "Velocity AI <bookings@velocityai.com.au>",
    "followup": "Mitchell Pearce <mitchell@velocityai.com.au>",
    "ava_welcome": "Ava from Velocity AI <ava@velocityai.com.au>",
    "default": "Velocity AI <hello@velocityai.com.au>",
}

# Resolve template paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = {
    "welcome": os.path.join(SCRIPT_DIR, "welcome-email.html"),
    "discovery": os.path.join(SCRIPT_DIR, "discovery-call-confirmation.html"),
    "followup": os.path.join(SCRIPT_DIR, "follow-up-email.html"),
    "signature": os.path.join(SCRIPT_DIR, "email-signature.html"),
}

# Subject lines
SUBJECTS = {
    "welcome": "Welcome to Velocity AI, {{first_name}}!",
    "discovery": "Your Discovery Call is Confirmed — {{call_date}} at {{call_time}}",
    "followup": "Great chatting, {{first_name}} — here's your summary",
}


# ---------------------------------------------------------------------------
# Template helpers
# ---------------------------------------------------------------------------

def load_template(template_key: str) -> str:
    """Load an HTML template from disk."""
    path = TEMPLATES[template_key]
    if not os.path.exists(path):
        print(f"ERROR: Template not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_signature() -> str:
    """Load the email signature HTML."""
    return load_template("signature")


def render(html: str, variables: dict) -> str:
    """Replace {{placeholder}} tokens with actual values."""
    for key, value in variables.items():
        placeholder = "{{" + key + "}}"
        html = html.replace(placeholder, str(value))
    return html


def inject_signature(html: str) -> str:
    """Insert the email signature just before the closing </body> tag.

    The branded templates already include a footer with Mitchell's details,
    so this is available for plain-text or simpler emails that need a sig.
    """
    sig = load_signature()
    if "</body>" in html:
        html = html.replace("</body>", f"\n{sig}\n</body>")
    else:
        html += f"\n{sig}"
    return html


# ---------------------------------------------------------------------------
# Email sending functions
# ---------------------------------------------------------------------------

def _send(
    to: str,
    subject: str,
    html: str,
    sender: str,
    reply_to: str = "mitchell@velocityai.com.au",
) -> dict:
    """Low-level send via Resend API. Returns the API response."""
    resend.api_key = RESEND_API_KEY

    params: resend.Emails.SendParams = {
        "from": sender,
        "to": [to],
        "subject": subject,
        "html": html,
        "reply_to": reply_to,
    }

    try:
        response = resend.Emails.send(params)
        print(f"  Email sent to {to}  |  ID: {response['id']}")
        return response
    except Exception as exc:
        print(f"  FAILED to send to {to}: {exc}", file=sys.stderr)
        raise


def send_welcome_email(
    to: str,
    first_name: str,
    *,
    from_ava: bool = False,
    unsubscribe_url: str = "https://velocityai.com.au/unsubscribe",
) -> dict:
    """Send the welcome email to a new lead (e.g. after a call with Ava).

    Args:
        to:               Recipient email address.
        first_name:       Recipient's first name.
        from_ava:         If True, send from ava@velocityai.com.au.
        unsubscribe_url:  Unsubscribe link.
    """
    html = load_template("welcome")
    variables = {
        "first_name": first_name,
        "unsubscribe_url": unsubscribe_url,
    }
    html = render(html, variables)
    subject = render(SUBJECTS["welcome"], variables)
    sender = SENDERS["ava_welcome"] if from_ava else SENDERS["welcome"]

    print(f"[Welcome] Sending to {to} (from_ava={from_ava})")
    return _send(to=to, subject=subject, html=html, sender=sender)


def send_discovery_confirmation(
    to: str,
    first_name: str,
    call_date: str,
    call_time: str,
    *,
    calendar_link: str = "#",
    reschedule_link: str = "mailto:mitchell@velocityai.com.au?subject=Reschedule",
) -> dict:
    """Send a discovery-call confirmation email.

    Args:
        to:              Recipient email address.
        first_name:      Recipient's first name.
        call_date:       e.g. "Wednesday, 9 April 2026"
        call_time:       e.g. "10:00 AM"
        calendar_link:   Google Calendar / ICS link.
        reschedule_link: Link or mailto for rescheduling.
    """
    html = load_template("discovery")
    variables = {
        "first_name": first_name,
        "call_date": call_date,
        "call_time": call_time,
        "calendar_link": calendar_link,
        "reschedule_link": reschedule_link,
    }
    html = render(html, variables)
    subject = render(SUBJECTS["discovery"], variables)

    print(f"[Discovery] Sending confirmation to {to}")
    return _send(to=to, subject=subject, html=html, sender=SENDERS["discovery"])


def send_followup_email(
    to: str,
    first_name: str,
    company_name: str,
    *,
    current_challenges_summary: str = "",
    goals_summary: str = "",
    opportunities_summary: str = "",
    next_steps: list[dict] | None = None,
    line_items: list[dict] | None = None,
    total_price: str = "",
    proposal_link: str = "#",
    unsubscribe_url: str = "https://velocityai.com.au/unsubscribe",
) -> dict:
    """Send the post-discovery-call follow-up / nurture email.

    Args:
        to:                           Recipient email address.
        first_name:                   Recipient's first name.
        company_name:                 Their company name.
        current_challenges_summary:   Summary of challenges discussed.
        goals_summary:                Summary of their goals.
        opportunities_summary:        AI opportunities identified.
        next_steps:                   List of dicts with 'title' and 'description' keys (up to 3).
        line_items:                   List of dicts with 'name' and 'price' keys (up to 3).
        total_price:                  e.g. "$4,500"
        proposal_link:                Link to full proposal doc.
        unsubscribe_url:              Unsubscribe link.
    """
    # Default next steps
    if next_steps is None:
        next_steps = [
            {"title": "Proposal Review", "description": "Review the attached proposal at your convenience."},
            {"title": "Follow-Up Call", "description": "We'll schedule a brief call to answer any questions."},
            {"title": "Kick Off", "description": "Once confirmed, we'll begin onboarding and implementation."},
        ]

    # Default line items
    if line_items is None:
        line_items = [
            {"name": "AI Strategy & Roadmap", "price": "TBC"},
            {"name": "Implementation & Build", "price": "TBC"},
            {"name": "Ongoing Support", "price": "TBC"},
        ]

    # Pad to exactly 3 entries
    while len(next_steps) < 3:
        next_steps.append({"title": "", "description": ""})
    while len(line_items) < 3:
        line_items.append({"name": "", "price": ""})

    variables = {
        "first_name": first_name,
        "company_name": company_name,
        "current_challenges_summary": current_challenges_summary,
        "goals_summary": goals_summary,
        "opportunities_summary": opportunities_summary,
        "next_step_1_title": next_steps[0]["title"],
        "next_step_1_description": next_steps[0]["description"],
        "next_step_2_title": next_steps[1]["title"],
        "next_step_2_description": next_steps[1]["description"],
        "next_step_3_title": next_steps[2]["title"],
        "next_step_3_description": next_steps[2]["description"],
        "line_item_1": line_items[0]["name"],
        "line_item_1_price": line_items[0]["price"],
        "line_item_2": line_items[1]["name"],
        "line_item_2_price": line_items[1]["price"],
        "line_item_3": line_items[2]["name"],
        "line_item_3_price": line_items[2]["price"],
        "total_price": total_price or "TBC",
        "proposal_link": proposal_link,
        "unsubscribe_url": unsubscribe_url,
    }
    html = load_template("followup")
    html = render(html, variables)
    subject = render(SUBJECTS["followup"], variables)

    print(f"[Follow-Up] Sending to {to} ({company_name})")
    return _send(to=to, subject=subject, html=html, sender=SENDERS["followup"])


def send_test_email(to: str) -> dict:
    """Send a quick test email with the signature to verify Resend is working."""
    sig = load_signature()
    html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; color: #333; max-width: 580px; margin: 0 auto; padding: 32px;">
        <p>Hey — this is a test email from the Velocity AI email system.</p>
        <p>If you're reading this, <strong>Resend is configured correctly</strong> and emails are sending from <code>velocityai.com.au</code>.</p>
        <br>
        {sig}
    </div>
    """
    print(f"[Test] Sending test email to {to}")
    return _send(
        to=to,
        subject="Resend Test — Velocity AI",
        html=html,
        sender=SENDERS["default"],
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Velocity AI — Send branded emails via Resend",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python send-email.py welcome \\
      --to "jane@example.com" --first-name "Jane"

  python send-email.py welcome \\
      --to "jane@example.com" --first-name "Jane" --from-ava

  python send-email.py discovery \\
      --to "jane@example.com" --first-name "Jane" \\
      --call-date "Wednesday, 9 April 2026" --call-time "10:00 AM"

  python send-email.py followup \\
      --to "jane@example.com" --first-name "Jane" \\
      --company-name "Acme Co" \\
      --challenges "Manual lead follow-up taking 10+ hrs/week" \\
      --goals "Automate lead nurture and reduce response time to < 5 min" \\
      --opportunities "AI voice agent for inbound, automated email sequences" \\
      --total-price "$4,500"

  python send-email.py test --to "mitchell@velocityai.com.au"
        """,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # -- welcome --
    p_welcome = subparsers.add_parser("welcome", help="Send welcome email to a new lead")
    p_welcome.add_argument("--to", required=True, help="Recipient email address")
    p_welcome.add_argument("--first-name", required=True, help="Recipient first name")
    p_welcome.add_argument("--from-ava", action="store_true", help="Send from ava@velocityai.com.au")
    p_welcome.add_argument("--unsubscribe-url", default="https://velocityai.com.au/unsubscribe")

    # -- discovery --
    p_disc = subparsers.add_parser("discovery", help="Send discovery call confirmation")
    p_disc.add_argument("--to", required=True, help="Recipient email address")
    p_disc.add_argument("--first-name", required=True, help="Recipient first name")
    p_disc.add_argument("--call-date", required=True, help='e.g. "Wednesday, 9 April 2026"')
    p_disc.add_argument("--call-time", required=True, help='e.g. "10:00 AM"')
    p_disc.add_argument("--calendar-link", default="#", help="Google Calendar / ICS link")
    p_disc.add_argument("--reschedule-link", default="mailto:mitchell@velocityai.com.au?subject=Reschedule")

    # -- followup --
    p_follow = subparsers.add_parser("followup", help="Send post-discovery follow-up email")
    p_follow.add_argument("--to", required=True, help="Recipient email address")
    p_follow.add_argument("--first-name", required=True, help="Recipient first name")
    p_follow.add_argument("--company-name", required=True, help="Company name")
    p_follow.add_argument("--challenges", default="", help="Current challenges summary")
    p_follow.add_argument("--goals", default="", help="Goals summary")
    p_follow.add_argument("--opportunities", default="", help="Opportunities identified")
    p_follow.add_argument("--total-price", default="", help='e.g. "$4,500"')
    p_follow.add_argument("--proposal-link", default="#", help="URL to full proposal")
    p_follow.add_argument("--unsubscribe-url", default="https://velocityai.com.au/unsubscribe")

    # -- test --
    p_test = subparsers.add_parser("test", help="Send a quick test email")
    p_test.add_argument("--to", required=True, help="Recipient email address")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  Velocity AI — Email Sender")
    print(f"  Command:  {args.command}")
    print(f"{'='*50}\n")

    if args.command == "welcome":
        send_welcome_email(
            to=args.to,
            first_name=args.first_name,
            from_ava=args.from_ava,
            unsubscribe_url=args.unsubscribe_url,
        )

    elif args.command == "discovery":
        send_discovery_confirmation(
            to=args.to,
            first_name=args.first_name,
            call_date=args.call_date,
            call_time=args.call_time,
            calendar_link=args.calendar_link,
            reschedule_link=args.reschedule_link,
        )

    elif args.command == "followup":
        send_followup_email(
            to=args.to,
            first_name=args.first_name,
            company_name=args.company_name,
            current_challenges_summary=args.challenges,
            goals_summary=args.goals,
            opportunities_summary=args.opportunities,
            total_price=args.total_price,
            proposal_link=args.proposal_link,
            unsubscribe_url=args.unsubscribe_url,
        )

    elif args.command == "test":
        send_test_email(to=args.to)

    print("\nDone.\n")


if __name__ == "__main__":
    main()
