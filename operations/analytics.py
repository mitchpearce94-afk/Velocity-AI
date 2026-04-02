#!/usr/bin/env python3
"""
Velocity AI — Analytics & Reporting Engine
============================================
Pulls data from Retell AI, Resend, Cal.com, and local pipeline data
to generate business performance reports.

Usage:
  python analytics.py                    # Full dashboard summary
  python analytics.py --calls            # Call performance metrics
  python analytics.py --emails           # Email sequence metrics
  python analytics.py --pipeline         # Lead pipeline funnel
  python analytics.py --revenue          # Revenue projections
  python analytics.py --daily-report     # Send daily report via email
  python analytics.py --export csv       # Export all data to CSV
  python analytics.py --export json      # Export all data to JSON
"""

import json
import os
import sys
import csv
import logging
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
from collections import Counter, defaultdict

try:
    import requests
except ImportError:
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

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
RESEND_API_BASE = "https://api.resend.com"

CALCOM_API_KEY = os.environ.get("CAL_API_KEY", "")
CALCOM_API_BASE = "https://api.cal.com/v2"

SCRIPT_DIR = Path(__file__).resolve().parent
LEADS_FILE = SCRIPT_DIR / "leads.json"
CALL_LOG_FILE = SCRIPT_DIR / "call_log.json"
REPORTS_DIR = SCRIPT_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

AEST = timezone(timedelta(hours=10))

# Pricing tiers for revenue projection
PRICING = {
    "solo":         499,
    "professional": 899,
    "enterprise":   1499,
}
AVG_DEAL_VALUE = 699  # Weighted average monthly deal value

# Pipeline conversion benchmarks
BENCHMARKS = {
    "lead_to_call":      0.90,   # 90% of leads get called
    "call_to_connect":   0.35,   # 35% of calls connect (not voicemail/no answer)
    "connect_to_interested": 0.40,  # 40% of connected calls show interest
    "interested_to_booked":  0.50,  # 50% of interested leads book discovery
    "booked_to_closed":      0.40,  # 40% of discovery calls close
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
log = logging.getLogger("analytics")


def now_aest() -> datetime:
    return datetime.now(AEST)


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_leads() -> list[dict]:
    if not LEADS_FILE.exists():
        return []
    with open(LEADS_FILE) as f:
        return json.load(f)


def load_call_log() -> list[dict]:
    if not CALL_LOG_FILE.exists():
        return []
    with open(CALL_LOG_FILE) as f:
        return json.load(f)


def fetch_retell_calls(days: int = 30) -> list[dict]:
    """Fetch recent calls from Retell API."""
    try:
        resp = requests.post(
            f"{RETELL_API_BASE}/v2/list-calls",
            headers={
                "Authorization": f"Bearer {RETELL_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "sort_order": "descending",
                "limit": 1000,
            },
            timeout=30,
        )
        if resp.status_code == 200:
            return resp.json()
        else:
            log.warning(f"Retell API error {resp.status_code}: {resp.text}")
            return []
    except requests.RequestException as e:
        log.warning(f"Failed to fetch Retell calls: {e}")
        return []


def fetch_calcom_bookings(days: int = 30) -> list[dict]:
    """Fetch recent bookings from Cal.com."""
    try:
        after_date = (now_aest() - timedelta(days=days)).strftime("%Y-%m-%d")
        resp = requests.get(
            f"{CALCOM_API_BASE}/bookings",
            headers={
                "Authorization": f"Bearer {CALCOM_API_KEY}",
                "cal-api-version": "2024-08-13",
                "Content-Type": "application/json",
            },
            params={
                "afterStart": after_date,
                "status": "upcoming",
            },
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("data", [])
        else:
            log.warning(f"Cal.com API error {resp.status_code}: {resp.text}")
            return []
    except requests.RequestException as e:
        log.warning(f"Failed to fetch Cal.com bookings: {e}")
        return []


# ---------------------------------------------------------------------------
# Analytics: Pipeline
# ---------------------------------------------------------------------------

def pipeline_report(leads: list[dict]) -> dict:
    """Analyse the lead pipeline funnel."""
    total = len(leads)
    if total == 0:
        return {"total": 0}

    statuses = Counter(l.get("status", "unknown") for l in leads)
    dispositions = Counter(l.get("disposition") or "none" for l in leads)
    trades = Counter(l.get("trade_type", "unknown") for l in leads)
    locations = Counter(l.get("location", "unknown") for l in leads)
    sources = Counter(l.get("lead_source", "unknown") for l in leads)

    # Funnel metrics
    called = sum(1 for l in leads if l.get("call_attempts", 0) > 0)
    connected = sum(1 for l in leads if l.get("disposition") in
                    ("INTERESTED", "BOOKED", "CALLBACK", "NOT_INTERESTED", "DNC", "GATEKEEPER"))
    interested = sum(1 for l in leads if l.get("disposition") in ("INTERESTED", "BOOKED", "CALLBACK"))
    booked = sum(1 for l in leads if l.get("disposition") == "BOOKED")

    # Email metrics from leads
    emails_started = sum(1 for l in leads if l.get("email_sequence_started"))
    emails_step_avg = 0
    email_leads = [l for l in leads if l.get("email_sequence_step", 0) > 0]
    if email_leads:
        emails_step_avg = sum(l["email_sequence_step"] for l in email_leads) / len(email_leads)

    # Score distribution
    scores = [l.get("lead_score", 0) for l in leads]
    avg_score = sum(scores) / len(scores) if scores else 0
    high_score_leads = sum(1 for s in scores if s >= 50)

    # Call attempt distribution
    attempt_dist = Counter(l.get("call_attempts", 0) for l in leads)

    return {
        "total": total,
        "statuses": dict(statuses),
        "dispositions": dict(dispositions),
        "trades": dict(trades),
        "locations": dict(locations),
        "sources": dict(sources),
        "funnel": {
            "total_leads": total,
            "called": called,
            "connected": connected,
            "interested": interested,
            "booked": booked,
            "call_rate": f"{called/total*100:.0f}%" if total else "0%",
            "connect_rate": f"{connected/called*100:.0f}%" if called else "0%",
            "interest_rate": f"{interested/connected*100:.0f}%" if connected else "0%",
            "book_rate": f"{booked/interested*100:.0f}%" if interested else "0%",
        },
        "emails": {
            "sequences_started": emails_started,
            "avg_step_reached": round(emails_step_avg, 1),
        },
        "scoring": {
            "average_score": round(avg_score, 1),
            "high_score_leads": high_score_leads,
            "score_buckets": {
                "0-19": sum(1 for s in scores if s < 20),
                "20-39": sum(1 for s in scores if 20 <= s < 40),
                "40-59": sum(1 for s in scores if 40 <= s < 60),
                "60-79": sum(1 for s in scores if 60 <= s < 80),
                "80-100": sum(1 for s in scores if s >= 80),
            },
        },
        "call_attempts": dict(attempt_dist),
    }


# ---------------------------------------------------------------------------
# Analytics: Calls
# ---------------------------------------------------------------------------

def call_report(call_log: list[dict], retell_calls: list[dict] = None) -> dict:
    """Analyse call performance."""
    if not call_log and not retell_calls:
        return {"total_calls": 0, "note": "No call data yet — pipeline hasn't run in live mode"}

    # Use local call log primarily
    calls = call_log if call_log else []
    total = len(calls)

    if total == 0:
        # Try Retell data
        if retell_calls:
            total = len(retell_calls)
            durations = [c.get("duration_ms", 0) / 1000 for c in retell_calls if c.get("duration_ms")]
            return {
                "total_calls": total,
                "source": "retell_api",
                "avg_duration_seconds": round(sum(durations) / len(durations), 1) if durations else 0,
                "total_talk_time_minutes": round(sum(durations) / 60, 1),
            }
        return {"total_calls": 0, "note": "No call data yet"}

    dispositions = Counter(c.get("disposition", "unknown") for c in calls)
    durations = [c.get("duration_seconds", 0) for c in calls if c.get("duration_seconds")]

    # Calls by day
    daily = defaultdict(int)
    for c in calls:
        ts = c.get("timestamp", "")
        if ts:
            try:
                day = datetime.fromisoformat(ts).strftime("%Y-%m-%d")
                daily[day] += 1
            except (ValueError, TypeError):
                pass

    # Calls by attempt number
    by_attempt = Counter(c.get("attempt_number", 0) for c in calls)

    avg_duration = sum(durations) / len(durations) if durations else 0
    total_talk_time = sum(durations)

    return {
        "total_calls": total,
        "dispositions": dict(dispositions),
        "avg_duration_seconds": round(avg_duration, 1),
        "total_talk_time_minutes": round(total_talk_time / 60, 1),
        "longest_call_seconds": round(max(durations), 1) if durations else 0,
        "calls_per_day": dict(sorted(daily.items())),
        "by_attempt_number": dict(by_attempt),
        "connect_rate": f"{sum(1 for c in calls if c.get('disposition') not in ('NO_ANSWER', 'VOICEMAIL', 'WRONG_NUMBER')) / total * 100:.0f}%" if total else "0%",
    }


# ---------------------------------------------------------------------------
# Analytics: Revenue Projection
# ---------------------------------------------------------------------------

def revenue_report(leads: list[dict], bookings: list[dict] = None) -> dict:
    """Project revenue based on pipeline data and conversion benchmarks."""
    total_leads = len(leads)
    booked = sum(1 for l in leads if l.get("disposition") == "BOOKED")
    interested = sum(1 for l in leads if l.get("disposition") in ("INTERESTED", "CALLBACK"))

    # Actual bookings from Cal.com
    actual_bookings = len(bookings) if bookings else 0

    # Projection based on current pipeline
    projected_calls = total_leads * BENCHMARKS["lead_to_call"]
    projected_connects = projected_calls * BENCHMARKS["call_to_connect"]
    projected_interested = projected_connects * BENCHMARKS["connect_to_interested"]
    projected_bookings = projected_interested * BENCHMARKS["interested_to_booked"]
    projected_closes = projected_bookings * BENCHMARKS["booked_to_closed"]

    monthly_revenue = projected_closes * AVG_DEAL_VALUE
    annual_revenue = monthly_revenue * 12

    # Best case / worst case (±30%)
    best_case_monthly = monthly_revenue * 1.3
    worst_case_monthly = monthly_revenue * 0.7

    # Revenue per lead metric
    revenue_per_lead = monthly_revenue / total_leads if total_leads else 0

    # Break-even analysis (assuming ~$500/mo operating costs)
    operating_costs = 500
    clients_to_break_even = operating_costs / AVG_DEAL_VALUE if AVG_DEAL_VALUE else 0

    return {
        "current_pipeline": {
            "total_leads": total_leads,
            "booked_discovery": booked,
            "interested": interested,
            "actual_cal_bookings": actual_bookings,
        },
        "projection_from_current_pipeline": {
            "projected_calls": round(projected_calls),
            "projected_connects": round(projected_connects),
            "projected_interested": round(projected_interested),
            "projected_bookings": round(projected_bookings),
            "projected_closes": round(projected_closes),
        },
        "revenue_forecast": {
            "avg_deal_value_monthly": AVG_DEAL_VALUE,
            "projected_monthly_revenue": round(monthly_revenue),
            "projected_annual_revenue": round(annual_revenue),
            "best_case_monthly": round(best_case_monthly),
            "worst_case_monthly": round(worst_case_monthly),
            "revenue_per_lead": round(revenue_per_lead, 2),
        },
        "break_even": {
            "monthly_operating_costs": operating_costs,
            "clients_to_break_even": round(clients_to_break_even, 1),
        },
        "benchmarks_used": BENCHMARKS,
    }


# ---------------------------------------------------------------------------
# Analytics: Email Sequences
# ---------------------------------------------------------------------------

def email_report(leads: list[dict]) -> dict:
    """Analyse email nurture sequence performance."""
    email_leads = [l for l in leads if l.get("email")]
    total_with_email = len(email_leads)
    sequences_started = sum(1 for l in leads if l.get("email_sequence_started"))

    step_distribution = Counter(l.get("email_sequence_step", 0) for l in leads if l.get("email_sequence_started"))

    # Leads with email vs without
    no_email = sum(1 for l in leads if not l.get("email"))

    return {
        "total_leads_with_email": total_with_email,
        "total_leads_without_email": no_email,
        "email_coverage": f"{total_with_email / len(leads) * 100:.0f}%" if leads else "0%",
        "sequences_started": sequences_started,
        "step_distribution": dict(step_distribution),
        "note": "Detailed open/click tracking available once Resend domain is verified and emails are sending",
    }


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_header(title: str):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"  {now_aest().strftime('%A %d %B %Y, %I:%M %p AEST')}")
    print(f"{'='*70}")


def print_section(title: str):
    print(f"\n  --- {title} ---\n")


def print_kv(key: str, value, indent: int = 4):
    print(f"{' '*indent}{key}: {value}")


def print_funnel(funnel: dict):
    """Print a visual pipeline funnel."""
    stages = [
        ("Total Leads",   funnel.get("total_leads", 0)),
        ("Called",         funnel.get("called", 0)),
        ("Connected",     funnel.get("connected", 0)),
        ("Interested",    funnel.get("interested", 0)),
        ("Booked",        funnel.get("booked", 0)),
    ]

    max_val = max(s[1] for s in stages) or 1
    bar_width = 40

    print()
    for label, val in stages:
        bar_len = int((val / max_val) * bar_width)
        bar = "█" * bar_len + "░" * (bar_width - bar_len)
        print(f"    {label:<16} {bar} {val}")
    print()


def display_pipeline(report: dict):
    print_section("LEAD PIPELINE")

    funnel = report.get("funnel", {})
    print_funnel(funnel)

    print_kv("Call Rate", funnel.get("call_rate", "N/A"))
    print_kv("Connect Rate", funnel.get("connect_rate", "N/A"))
    print_kv("Interest Rate", funnel.get("interest_rate", "N/A"))
    print_kv("Booking Rate", funnel.get("book_rate", "N/A"))

    print_section("BY TRADE")
    for trade, count in sorted(report.get("trades", {}).items(), key=lambda x: -x[1]):
        print_kv(trade, count)

    print_section("BY LOCATION")
    for loc, count in sorted(report.get("locations", {}).items(), key=lambda x: -x[1]):
        print_kv(loc, count)

    print_section("BY STATUS")
    for status, count in sorted(report.get("statuses", {}).items(), key=lambda x: -x[1]):
        print_kv(status, count)

    print_section("LEAD SCORING")
    scoring = report.get("scoring", {})
    print_kv("Average Score", scoring.get("average_score", 0))
    print_kv("High-Score Leads (50+)", scoring.get("high_score_leads", 0))
    buckets = scoring.get("score_buckets", {})
    for bucket, count in buckets.items():
        print_kv(f"  {bucket} pts", count)


def display_calls(report: dict):
    print_section("CALL PERFORMANCE")

    if report.get("note"):
        print(f"    {report['note']}")
        return

    print_kv("Total Calls", report.get("total_calls", 0))
    print_kv("Avg Duration", f"{report.get('avg_duration_seconds', 0):.0f}s")
    print_kv("Total Talk Time", f"{report.get('total_talk_time_minutes', 0):.1f} min")
    print_kv("Longest Call", f"{report.get('longest_call_seconds', 0):.0f}s")
    print_kv("Connect Rate", report.get("connect_rate", "N/A"))

    dispositions = report.get("dispositions", {})
    if dispositions:
        print_section("CALL DISPOSITIONS")
        for disp, count in sorted(dispositions.items(), key=lambda x: -x[1]):
            print_kv(disp, count)


def display_revenue(report: dict):
    print_section("REVENUE PROJECTION")

    pipeline = report.get("current_pipeline", {})
    print_kv("Total Leads", pipeline.get("total_leads", 0))
    print_kv("Booked Discovery", pipeline.get("booked_discovery", 0))
    print_kv("Interested", pipeline.get("interested", 0))
    print_kv("Cal.com Bookings", pipeline.get("actual_cal_bookings", 0))

    proj = report.get("projection_from_current_pipeline", {})
    print_section("PROJECTED FUNNEL (from current leads)")
    print_kv("Calls", proj.get("projected_calls", 0))
    print_kv("Connects", proj.get("projected_connects", 0))
    print_kv("Interested", proj.get("projected_interested", 0))
    print_kv("Discovery Calls", proj.get("projected_bookings", 0))
    print_kv("Closed Deals", proj.get("projected_closes", 0))

    rev = report.get("revenue_forecast", {})
    print_section("REVENUE FORECAST")
    print_kv("Avg Deal Value", f"${rev.get('avg_deal_value_monthly', 0):,}/mo")
    print_kv("Projected Monthly", f"${rev.get('projected_monthly_revenue', 0):,}/mo")
    print_kv("Projected Annual", f"${rev.get('projected_annual_revenue', 0):,}/yr")
    print_kv("Best Case Monthly", f"${rev.get('best_case_monthly', 0):,}/mo")
    print_kv("Worst Case Monthly", f"${rev.get('worst_case_monthly', 0):,}/mo")
    print_kv("Revenue Per Lead", f"${rev.get('revenue_per_lead', 0):.2f}")

    be = report.get("break_even", {})
    print_section("BREAK-EVEN")
    print_kv("Operating Costs", f"${be.get('monthly_operating_costs', 0):,}/mo")
    print_kv("Clients to Break Even", be.get("clients_to_break_even", 0))


def display_emails(report: dict):
    print_section("EMAIL SEQUENCES")
    print_kv("Leads with Email", report.get("total_leads_with_email", 0))
    print_kv("Leads without Email", report.get("total_leads_without_email", 0))
    print_kv("Email Coverage", report.get("email_coverage", "0%"))
    print_kv("Sequences Started", report.get("sequences_started", 0))
    if report.get("note"):
        print(f"\n    Note: {report['note']}")


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def export_data(leads: list[dict], call_log: list[dict], fmt: str = "json"):
    """Export all analytics data to a file."""
    timestamp = now_aest().strftime("%Y%m%d_%H%M")

    if fmt == "csv":
        # Export leads as CSV
        filepath = REPORTS_DIR / f"leads_export_{timestamp}.csv"
        if leads:
            with open(filepath, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=leads[0].keys())
                writer.writeheader()
                writer.writerows(leads)
            log.info(f"Leads exported to {filepath}")

        # Export call log as CSV
        if call_log:
            call_filepath = REPORTS_DIR / f"calls_export_{timestamp}.csv"
            with open(call_filepath, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=call_log[0].keys())
                writer.writeheader()
                writer.writerows(call_log)
            log.info(f"Call log exported to {call_filepath}")

    elif fmt == "json":
        filepath = REPORTS_DIR / f"analytics_export_{timestamp}.json"
        retell_calls = fetch_retell_calls()
        bookings = fetch_calcom_bookings()

        full_report = {
            "generated_at": now_aest().isoformat(),
            "pipeline": pipeline_report(leads),
            "calls": call_report(call_log, retell_calls),
            "revenue": revenue_report(leads, bookings),
            "emails": email_report(leads),
            "raw_leads": leads,
            "raw_call_log": call_log,
        }
        with open(filepath, "w") as f:
            json.dump(full_report, f, indent=2, default=str)
        log.info(f"Full analytics exported to {filepath}")

    print(f"\n  Exported to: {filepath}")


# ---------------------------------------------------------------------------
# Daily report email
# ---------------------------------------------------------------------------

def send_daily_report(leads: list[dict], call_log: list[dict]):
    """Send a daily summary report via Resend."""
    pipeline = pipeline_report(leads)
    calls = call_report(call_log)
    rev = revenue_report(leads)

    funnel = pipeline.get("funnel", {})
    rev_forecast = rev.get("revenue_forecast", {})

    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333;">
        <h2 style="color: #1a1a2e;">Velocity AI — Daily Report</h2>
        <p style="color: #666;">{now_aest().strftime('%A %d %B %Y')}</p>

        <h3>Pipeline</h3>
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;">Total Leads</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">{funnel.get('total_leads', 0)}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;">Called</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{funnel.get('called', 0)}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;">Connected</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{funnel.get('connected', 0)}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;">Interested</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{funnel.get('interested', 0)}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;">Booked</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #27ae60;">{funnel.get('booked', 0)}</td></tr>
        </table>

        <h3>Calls</h3>
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;">Total Calls</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{calls.get('total_calls', 0)}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;">Connect Rate</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{calls.get('connect_rate', 'N/A')}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;">Avg Duration</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{calls.get('avg_duration_seconds', 0):.0f}s</td></tr>
        </table>

        <h3>Revenue Forecast</h3>
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;">Projected Monthly</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #27ae60;">${rev_forecast.get('projected_monthly_revenue', 0):,}/mo</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;">Projected Annual</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">${rev_forecast.get('projected_annual_revenue', 0):,}/yr</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee;">Revenue Per Lead</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">${rev_forecast.get('revenue_per_lead', 0):.2f}</td></tr>
        </table>

        <h3>By Trade</h3>
        <table style="width: 100%; border-collapse: collapse;">
            {''.join(f'<tr><td style="padding: 4px;">{t}</td><td style="padding: 4px;">{c}</td></tr>'
                     for t, c in sorted(pipeline.get('trades', {}).items(), key=lambda x: -x[1]))}
        </table>

        <br>
        <p style="color: #999; font-size: 12px;">Generated by Velocity AI Analytics Engine</p>
    </div>
    """

    payload = {
        "from": "Velocity AI <ava@velocityai.com.au>",
        "reply_to": "mitchell@velocityai.com.au",
        "to": ["mitchell@velocityai.com.au"],
        "subject": f"Velocity AI — Daily Report — {now_aest().strftime('%d %b %Y')}",
        "html": html,
        "tags": [{"name": "campaign", "value": "internal-analytics"}],
    }

    try:
        resp = requests.post(
            f"{RESEND_API_BASE}/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=15,
        )
        if resp.status_code in (200, 201):
            log.info(f"Daily report sent to mitchell@velocityai.com.au")
            print("  Daily report sent successfully.")
        else:
            log.error(f"Failed to send daily report: {resp.status_code} — {resp.text}")
            print(f"  Failed: {resp.text}")
    except requests.RequestException as e:
        log.error(f"Failed to send daily report: {e}")
        print(f"  Failed: {e}")


# ---------------------------------------------------------------------------
# Main dashboard
# ---------------------------------------------------------------------------

def full_dashboard():
    """Print the full analytics dashboard."""
    leads = load_leads()
    call_log = load_call_log()
    retell_calls = fetch_retell_calls()
    bookings = fetch_calcom_bookings()

    pipeline = pipeline_report(leads)
    calls = call_report(call_log, retell_calls)
    rev = revenue_report(leads, bookings)
    emails = email_report(leads)

    print_header("VELOCITY AI — ANALYTICS DASHBOARD")
    display_pipeline(pipeline)
    display_calls(calls)
    display_revenue(rev)
    display_emails(emails)

    print(f"\n{'='*70}")
    print(f"  Run with --export json or --export csv to save full data")
    print(f"  Run with --daily-report to email this to Mitchell")
    print(f"{'='*70}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Velocity AI Analytics & Reporting")
    parser.add_argument("--calls", action="store_true", help="Call performance metrics")
    parser.add_argument("--emails", action="store_true", help="Email sequence metrics")
    parser.add_argument("--pipeline", action="store_true", help="Lead pipeline funnel")
    parser.add_argument("--revenue", action="store_true", help="Revenue projections")
    parser.add_argument("--daily-report", action="store_true", help="Send daily report email")
    parser.add_argument("--export", choices=["csv", "json"], help="Export data")

    args = parser.parse_args()

    leads = load_leads()
    call_log = load_call_log()

    # Specific view requested
    if args.pipeline:
        print_header("VELOCITY AI — PIPELINE REPORT")
        display_pipeline(pipeline_report(leads))
    elif args.calls:
        print_header("VELOCITY AI — CALL REPORT")
        retell_calls = fetch_retell_calls()
        display_calls(call_report(call_log, retell_calls))
    elif args.revenue:
        print_header("VELOCITY AI — REVENUE REPORT")
        bookings = fetch_calcom_bookings()
        display_revenue(revenue_report(leads, bookings))
    elif args.emails:
        print_header("VELOCITY AI — EMAIL REPORT")
        display_emails(email_report(leads))
    elif args.daily_report:
        send_daily_report(leads, call_log)
    elif args.export:
        export_data(leads, call_log, args.export)
    else:
        # Full dashboard
        full_dashboard()


if __name__ == "__main__":
    main()
