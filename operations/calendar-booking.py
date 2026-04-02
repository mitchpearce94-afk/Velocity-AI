#!/usr/bin/env python3
"""
Cal.com Booking API Wrapper — Velocity AI
==========================================

Provides functions to check availability, create bookings, cancel, and
reschedule discovery calls with Mitchell via Cal.com API v2.

Usage (CLI):
    python calendar-booking.py slots tomorrow
    python calendar-booking.py slots 2026-04-03
    python calendar-booking.py slots 2026-04-03 2026-04-05
    python calendar-booking.py book "Dave Smith" "dave@email.com" "0412345678" "2026-04-03 09:00"
    python calendar-booking.py book "Dave Smith" "dave@email.com" "0412345678" "2026-04-03 09:00" --notes "Plumber, 5 staff"
    python calendar-booking.py cancel <booking_uid>
    python calendar-booking.py cancel <booking_uid> --reason "Caller requested"
    python calendar-booking.py reschedule <booking_uid> "2026-04-04 12:00"

Environment:
    CAL_API_KEY     — Your Cal.com API key (cal_live_xxxxxxxxxxxx)
    CAL_USERNAME    — Your Cal.com username
    CAL_EVENT_SLUG  — Event type slug (default: discovery-call)
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CAL_API_KEY = os.environ.get("CAL_API_KEY", "")
CAL_USERNAME = os.environ.get("CAL_USERNAME", "mitchell-pearce")
CAL_EVENT_SLUG = os.environ.get("CAL_EVENT_SLUG", "discovery-call")

BASE_URL = "https://api.cal.com/v2"

# Cal.com API v2 uses different API versions for different endpoint groups
API_VERSIONS = {
    "slots": "2024-09-04",
    "bookings": "2024-08-13",
    "event-types": "2024-06-14",
    "default": "2024-08-13",
}

# Australia/Brisbane is UTC+10 with no daylight saving
AEST_OFFSET = timezone(timedelta(hours=10))
AEST_TZ_NAME = "Australia/Brisbane"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _headers(auth: bool = False, endpoint: str = "default") -> dict:
    """Standard headers for Cal.com API v2 requests."""
    # Determine API version based on endpoint group
    version = API_VERSIONS.get(endpoint, API_VERSIONS["default"])
    h = {
        "Content-Type": "application/json",
        "cal-api-version": version,
    }
    if auth:
        h["Authorization"] = f"Bearer {CAL_API_KEY}"
    return h


def _request(method: str, path: str, params: dict | None = None,
             body: dict | None = None, auth: bool = False,
             endpoint: str = "default") -> dict:
    """Make an HTTP request to the Cal.com API and return parsed JSON."""
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urlencode(params)

    data = json.dumps(body).encode() if body else None
    req = Request(url, data=data, headers=_headers(auth, endpoint), method=method)

    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"API Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Connection Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def _utc_iso(dt: datetime) -> str:
    """Convert a datetime to UTC ISO 8601 string."""
    utc_dt = dt.astimezone(timezone.utc)
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def _parse_aest(date_str: str, time_str: str = "00:00") -> datetime:
    """Parse a date (and optional time) string as AEST datetime."""
    combined = f"{date_str} {time_str}"
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            naive = datetime.strptime(combined, fmt)
            return naive.replace(tzinfo=AEST_OFFSET)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse datetime: {combined}")


def _utc_to_aest(time_str: str) -> datetime:
    """Convert an ISO time string (UTC or offset-aware) to an AEST-aware datetime."""
    # Handle timezone-offset strings from Cal.com v2 (e.g., +10:00)
    if "+" in time_str[10:] and not time_str.endswith("Z"):
        # Already has timezone offset — parse with fromisoformat
        try:
            dt = datetime.fromisoformat(time_str)
            return dt.astimezone(AEST_OFFSET)
        except ValueError:
            pass
    # Handle various UTC ISO formats from Cal.com
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S.%f+00:00", "%Y-%m-%dT%H:%M:%S+00:00"):
        try:
            utc_dt = datetime.strptime(time_str, fmt).replace(tzinfo=timezone.utc)
            return utc_dt.astimezone(AEST_OFFSET)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse time: {time_str}")


def _resolve_date(date_arg: str) -> str:
    """Resolve 'today', 'tomorrow', or a date string to YYYY-MM-DD."""
    now_aest = datetime.now(AEST_OFFSET)
    if date_arg.lower() == "today":
        return now_aest.strftime("%Y-%m-%d")
    elif date_arg.lower() == "tomorrow":
        return (now_aest + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        # Validate format
        datetime.strptime(date_arg, "%Y-%m-%d")
        return date_arg


def _format_aest_time(dt: datetime) -> str:
    """Format an AEST datetime for human-readable display."""
    return dt.strftime("%A %-d %B at %-I:%M %p AEST")


# ---------------------------------------------------------------------------
# Core API Functions
# ---------------------------------------------------------------------------

def get_available_slots(start_date: str, end_date: str | None = None,
                        username: str | None = None,
                        event_slug: str | None = None) -> dict:
    """
    Check available slots for a date range.

    Args:
        start_date: Start date in YYYY-MM-DD format (AEST).
        end_date: End date in YYYY-MM-DD format (AEST). Defaults to start_date.
        username: Cal.com username. Defaults to CAL_USERNAME.
        event_slug: Event type slug. Defaults to CAL_EVENT_SLUG.

    Returns:
        Dict with date keys and lists of available slot times (AEST).
    """
    username = username or CAL_USERNAME
    event_slug = event_slug or CAL_EVENT_SLUG
    end_date = end_date or start_date

    # Cal.com v2 slots endpoint accepts date strings directly
    params = {
        "username": username,
        "eventTypeSlug": event_slug,
        "start": start_date,
        "end": end_date,
        "timeZone": AEST_TZ_NAME,
    }

    response = _request("GET", "/slots", params=params, endpoint="slots")

    # Parse and convert slots to AEST
    # v2 slots response: data is {date: [{start: "ISO-string"}, ...]}
    raw_slots = response.get("data", {})
    # Remove non-slot keys like 'status' if present at data level
    if isinstance(raw_slots, dict):
        raw_slots = {k: v for k, v in raw_slots.items()
                     if isinstance(v, list)}
    result = {}

    for date_key, slots in raw_slots.items():
        for slot in slots:
            slot_time = slot.get("start") or slot.get("time", "")
            if not slot_time:
                continue
            aest_dt = _utc_to_aest(slot_time)
            aest_date = aest_dt.strftime("%Y-%m-%d")
            if aest_date not in result:
                result[aest_date] = []
            result[aest_date].append({
                "time_aest": aest_dt.strftime("%H:%M"),
                "time_utc": slot["time"],
                "display": _format_aest_time(aest_dt),
            })

    # Sort slots within each date
    for date_key in result:
        result[date_key].sort(key=lambda s: s["time_aest"])

    return result


def create_booking(name: str, email: str, phone: str,
                   start_time_aest: str, notes: str = "",
                   username: str | None = None,
                   event_slug: str | None = None) -> dict:
    """
    Create a discovery call booking.

    Args:
        name: Attendee full name.
        email: Attendee email address.
        phone: Attendee phone number.
        start_time_aest: Start time in "YYYY-MM-DD HH:MM" format (AEST).
        notes: Optional notes about the caller/business.
        username: Cal.com username. Defaults to CAL_USERNAME.
        event_slug: Event type slug. Defaults to CAL_EVENT_SLUG.

    Returns:
        Booking confirmation dict from Cal.com.
    """
    username = username or CAL_USERNAME
    event_slug = event_slug or CAL_EVENT_SLUG

    parts = start_time_aest.split(" ")
    if len(parts) != 2:
        raise ValueError("start_time_aest must be 'YYYY-MM-DD HH:MM'")

    aest_dt = _parse_aest(parts[0], parts[1])
    utc_start = _utc_iso(aest_dt)

    body = {
        "eventTypeSlug": event_slug,
        "username": username,
        "start": utc_start,
        "attendee": {
            "name": name,
            "email": email,
            "timeZone": AEST_TZ_NAME,
        },
        "bookingFieldsResponses": {},
    }

    if phone:
        body["attendee"]["phoneNumber"] = phone
        body["bookingFieldsResponses"]["phone"] = phone
    if notes:
        body["bookingFieldsResponses"]["notes"] = notes

    response = _request("POST", "/bookings", body=body, auth=True,
                        endpoint="bookings")
    return response


def cancel_booking(booking_uid: str, reason: str = "") -> dict:
    """
    Cancel an existing booking.

    Args:
        booking_uid: The unique booking ID from Cal.com.
        reason: Optional cancellation reason.

    Returns:
        Cancellation confirmation from Cal.com.
    """
    body = {}
    if reason:
        body["cancellationReason"] = reason

    return _request("POST", f"/bookings/{booking_uid}/cancel",
                    body=body if body else None, auth=True,
                    endpoint="bookings")


def reschedule_booking(booking_uid: str, new_time_aest: str,
                       reason: str = "") -> dict:
    """
    Reschedule an existing booking to a new time.

    Args:
        booking_uid: The unique booking ID from Cal.com.
        new_time_aest: New start time in "YYYY-MM-DD HH:MM" format (AEST).
        reason: Optional reschedule reason.

    Returns:
        Reschedule confirmation from Cal.com.
    """
    parts = new_time_aest.split(" ")
    if len(parts) != 2:
        raise ValueError("new_time_aest must be 'YYYY-MM-DD HH:MM'")

    aest_dt = _parse_aest(parts[0], parts[1])
    utc_start = _utc_iso(aest_dt)

    body = {"start": utc_start}
    if reason:
        body["rescheduleReason"] = reason

    return _request("POST", f"/bookings/{booking_uid}/reschedule",
                    body=body, auth=True, endpoint="bookings")


# ---------------------------------------------------------------------------
# Webhook Handler (for Retell AI integration)
# ---------------------------------------------------------------------------

def handle_retell_webhook(payload: dict) -> str:
    """
    Process a Retell AI custom function webhook call.

    This is called by your webhook server when Ava triggers a booking function.
    Returns a plain-text string that Ava can speak to the caller.

    Args:
        payload: The parsed JSON body from the Retell webhook.

    Returns:
        A response string for Ava to relay to the caller.
    """
    function_name = payload.get("function_name", "")
    args = payload.get("arguments", {})

    if function_name == "check_availability":
        date = args.get("date", "tomorrow")
        try:
            resolved = _resolve_date(date)
        except ValueError:
            return "I couldn't understand that date. Could you try again?"

        slots = get_available_slots(resolved)
        if not slots:
            return (f"It looks like Mitchell doesn't have any availability on "
                    f"{date}. Would you like me to check another day?")

        # Build a natural response with up to 3 slots
        all_slots = []
        for date_key, day_slots in slots.items():
            all_slots.extend(day_slots)

        if len(all_slots) > 3:
            selected = [all_slots[0], all_slots[len(all_slots) // 2], all_slots[-1]]
        else:
            selected = all_slots

        times = [s["display"] for s in selected]
        if len(times) == 1:
            return f"I've got one slot available: {times[0]}. Would that work for you?"
        elif len(times) == 2:
            return f"I've got {times[0]} or {times[1]}. Which works better for you?"
        else:
            return (f"I've got a few options: {times[0]}, {times[1]}, "
                    f"or {times[2]}. What suits you best?")

    elif function_name == "book_discovery_call":
        name = args.get("caller_name", "")
        email = args.get("caller_email", "")
        phone = args.get("caller_phone", "")
        time_str = args.get("booking_time", "")
        notes = args.get("notes", "")

        if not all([name, email, phone, time_str]):
            return ("I just need a few details to lock that in — "
                    "could you give me your name, email, and phone number?")

        try:
            result = create_booking(name, email, phone, time_str, notes)
            return (f"You're all booked in, {name.split()[0]}. "
                    f"Mitchell will give you a call at the booked time. "
                    f"You'll get a confirmation email at {email} shortly.")
        except Exception as e:
            return ("Sorry, I had a bit of trouble locking that in. "
                    "Let me take your details and Mitchell will call you "
                    "to sort out a time. What's the best number to reach you on?")

    elif function_name == "cancel_booking":
        uid = args.get("booking_uid", "")
        reason = args.get("reason", "Caller requested cancellation")
        if not uid:
            return "I need the booking reference to cancel. Do you have it handy?"
        try:
            cancel_booking(uid, reason)
            return "Done — that booking's been cancelled. Is there anything else I can help with?"
        except Exception:
            return ("I wasn't able to cancel that one automatically. "
                    "I'll pass it on to Mitchell and he'll sort it out for you.")

    else:
        return ("I'm not sure how to handle that request. "
                "Let me take your details and Mitchell will get back to you.")


# ---------------------------------------------------------------------------
# CLI Interface
# ---------------------------------------------------------------------------

def cli_slots(args):
    """Handle the 'slots' CLI command."""
    start = _resolve_date(args.start_date)
    end = _resolve_date(args.end_date) if args.end_date else start

    print(f"\nChecking availability for {CAL_USERNAME}/{CAL_EVENT_SLUG}")
    print(f"Date range: {start} to {end} (AEST)\n")

    slots = get_available_slots(start, end)

    if not slots:
        print("No available slots found for this date range.")
        return

    total = 0
    for date_key in sorted(slots.keys()):
        day_slots = slots[date_key]
        print(f"  {date_key}:")
        for slot in day_slots:
            print(f"    {slot['time_aest']}  ({slot['display']})")
            total += 1
        print()

    print(f"Total: {total} available slot(s)")


def cli_book(args):
    """Handle the 'book' CLI command."""
    print(f"\nCreating booking...")
    print(f"  Name:  {args.name}")
    print(f"  Email: {args.email}")
    print(f"  Phone: {args.phone}")
    print(f"  Time:  {args.time} AEST")
    if args.notes:
        print(f"  Notes: {args.notes}")
    print()

    result = create_booking(
        name=args.name,
        email=args.email,
        phone=args.phone,
        start_time_aest=args.time,
        notes=args.notes or "",
    )

    print("Booking created successfully!")
    print(json.dumps(result, indent=2))


def cli_cancel(args):
    """Handle the 'cancel' CLI command."""
    print(f"\nCancelling booking {args.uid}...")
    result = cancel_booking(args.uid, args.reason or "")
    print("Booking cancelled.")
    print(json.dumps(result, indent=2))


def cli_reschedule(args):
    """Handle the 'reschedule' CLI command."""
    print(f"\nRescheduling booking {args.uid} to {args.new_time} AEST...")
    result = reschedule_booking(args.uid, args.new_time, args.reason or "")
    print("Booking rescheduled.")
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Cal.com Booking API — Velocity AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # slots
    p_slots = subparsers.add_parser("slots", help="Check available slots")
    p_slots.add_argument("start_date", help="Start date: YYYY-MM-DD, 'today', or 'tomorrow'")
    p_slots.add_argument("end_date", nargs="?", help="End date (optional, defaults to start)")
    p_slots.set_defaults(func=cli_slots)

    # book
    p_book = subparsers.add_parser("book", help="Create a booking")
    p_book.add_argument("name", help="Attendee full name")
    p_book.add_argument("email", help="Attendee email")
    p_book.add_argument("phone", help="Attendee phone number")
    p_book.add_argument("time", help="Booking time: 'YYYY-MM-DD HH:MM' (AEST)")
    p_book.add_argument("--notes", help="Optional notes about the caller")
    p_book.set_defaults(func=cli_book)

    # cancel
    p_cancel = subparsers.add_parser("cancel", help="Cancel a booking")
    p_cancel.add_argument("uid", help="Booking UID")
    p_cancel.add_argument("--reason", help="Cancellation reason")
    p_cancel.set_defaults(func=cli_cancel)

    # reschedule
    p_resched = subparsers.add_parser("reschedule", help="Reschedule a booking")
    p_resched.add_argument("uid", help="Booking UID")
    p_resched.add_argument("new_time", help="New time: 'YYYY-MM-DD HH:MM' (AEST)")
    p_resched.add_argument("--reason", help="Reschedule reason")
    p_resched.set_defaults(func=cli_reschedule)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Warn if using placeholder keys
    if CAL_API_KEY == "YOUR_CAL_API_KEY_HERE":
        print("WARNING: CAL_API_KEY not set. Export it or set in environment.", file=sys.stderr)
        print("  export CAL_API_KEY='cal_live_xxxxxxxxxxxx'", file=sys.stderr)
        if args.command != "slots":  # slots doesn't require auth
            print("  (Required for booking/cancel/reschedule operations)\n", file=sys.stderr)

    if CAL_USERNAME == "YOUR_CAL_USERNAME_HERE":
        print("WARNING: CAL_USERNAME not set. Export it or set in environment.", file=sys.stderr)
        print("  export CAL_USERNAME='your-cal-username'\n", file=sys.stderr)
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
