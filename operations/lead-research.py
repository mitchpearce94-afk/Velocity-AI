#!/usr/bin/env python3
"""
Velocity AI — Lead Research Engine
====================================
Automates finding new trade business leads in South East Queensland.

Searches multiple directories, enriches with website/review data,
scores prospects by automation-readiness, and appends to leads.json
for the outbound pipeline.

Sources:
  - Google Places API (nearby search by trade + location)
  - Yellow Pages Australia (yellowpages.com.au)
  - HiPages (hipages.com.au)
  - True Local (truelocal.com.au)

Usage:
  python lead-research.py --trade plumbing --location brisbane --limit 10
  python lead-research.py --all
  python lead-research.py --enrich
  python lead-research.py --enrich --batch 10 --missing-only
  python lead-research.py --summary

Environment Variables (set in .env or export):
  GOOGLE_PLACES_API_KEY   — Google Places API key (required for Google source)
  VELOCITY_LEADS_PATH     — Override default leads.json path

Setup:
  pip install requests beautifulsoup4 python-dotenv
"""

import json
import os
import sys
import re
import time
import hashlib
import logging
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
from urllib.parse import quote_plus, urljoin

try:
    import requests
except ImportError:
    os.system(f"{sys.executable} -m pip install requests --quiet")
    import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    os.system(f"{sys.executable} -m pip install beautifulsoup4 --quiet")
    from bs4 import BeautifulSoup

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_LEADS_PATH = SCRIPT_DIR / "leads.json"
LEADS_PATH = Path(os.getenv("VELOCITY_LEADS_PATH", str(DEFAULT_LEADS_PATH)))

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY", "")

# Rate limiting (seconds between requests)
RATE_LIMIT_DELAY = 2.0
ENRICHMENT_DELAY = 1.5

# HTTP session config
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
REQUEST_TIMEOUT = 15

# ---------------------------------------------------------------------------
# Trade categories & SEQ locations
# ---------------------------------------------------------------------------

TRADE_CATEGORIES = [
    "plumbing", "electrical", "building", "landscaping",
    "hvac", "roofing", "painting", "concreting",
]

# Friendly names for display and search queries
TRADE_SEARCH_TERMS = {
    "plumbing":     ["plumber", "plumbing"],
    "electrical":   ["electrician", "electrical"],
    "building":     ["builder", "building construction"],
    "landscaping":  ["landscaper", "landscaping"],
    "hvac":         ["air conditioning", "hvac", "heating cooling"],
    "roofing":      ["roofer", "roofing"],
    "painting":     ["painter", "painting"],
    "concreting":   ["concreter", "concreting"],
}

SEQ_LOCATIONS = {
    "brisbane":       {"display": "Brisbane, QLD",        "lat": -27.4698, "lng": 153.0251},
    "gold-coast":     {"display": "Gold Coast, QLD",      "lat": -28.0167, "lng": 153.4000},
    "sunshine-coast": {"display": "Sunshine Coast, QLD",  "lat": -26.6500, "lng": 153.0667},
    "ipswich":        {"display": "Ipswich, QLD",         "lat": -27.6167, "lng": 152.7667},
    "logan":          {"display": "Logan, QLD",           "lat": -27.6389, "lng": 153.1094},
    "redlands":       {"display": "Redlands, QLD",        "lat": -27.5333, "lng": 153.2333},
}

# Location aliases for CLI convenience
LOCATION_ALIASES = {
    "brisbane": "brisbane", "bris": "brisbane", "bne": "brisbane",
    "gold-coast": "gold-coast", "goldcoast": "gold-coast", "gc": "gold-coast",
    "sunshine-coast": "sunshine-coast", "sunshinecoast": "sunshine-coast", "sc": "sunshine-coast",
    "ipswich": "ipswich", "ips": "ipswich",
    "logan": "logan",
    "redlands": "redlands", "redland": "redlands",
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("lead-research")

# ---------------------------------------------------------------------------
# HTTP Session
# ---------------------------------------------------------------------------

session = requests.Session()
session.headers.update({
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-AU,en;q=0.9",
})


def rate_limit(delay: float = RATE_LIMIT_DELAY):
    """Sleep to respect rate limits."""
    time.sleep(delay)


def safe_get(url: str, params: dict = None, timeout: int = REQUEST_TIMEOUT) -> Optional[requests.Response]:
    """GET request with error handling."""
    try:
        resp = session.get(url, params=params, timeout=timeout)
        resp.raise_for_status()
        return resp
    except requests.RequestException as e:
        log.warning(f"Request failed: {url} — {e}")
        return None


# ---------------------------------------------------------------------------
# Lead data model
# ---------------------------------------------------------------------------

def make_lead(
    business_name: str,
    trade_type: str,
    phone: str,
    location: str,
    source: str,
    **kwargs,
) -> dict:
    """Create a lead dict matching the existing leads.json schema."""
    # Generate deterministic ID from business name + phone
    raw = f"{business_name.lower().strip()}|{phone.strip()}"
    lead_hash = hashlib.md5(raw.encode()).hexdigest()[:8]
    lead_id = f"lead_{lead_hash}"

    return {
        "id": lead_id,
        "contact_name": kwargs.get("contact_name"),
        "business_name": business_name.strip(),
        "trade_type": trade_type.title(),
        "phone": normalise_phone(phone),
        "email": kwargs.get("email"),
        "location": location,
        "employee_count": kwargs.get("employee_count"),
        "lead_source": source,
        "website": kwargs.get("website"),
        "notes": kwargs.get("notes"),
        "researched_at": datetime.now(timezone(timedelta(hours=10))).isoformat(),
        "status": "new",
        "call_attempts": 0,
        "last_call_at": None,
        "disposition": None,
        "follow_up_at": None,
        "email_sequence_started": False,
        # Enrichment fields (populated by --enrich)
        "google_rating": kwargs.get("google_rating"),
        "google_review_count": kwargs.get("google_review_count"),
        "has_online_booking": kwargs.get("has_online_booking"),
        "has_chatbot": kwargs.get("has_chatbot"),
        "website_quality": kwargs.get("website_quality"),  # "modern" | "outdated" | "none"
        "lead_score": kwargs.get("lead_score", 0),
    }


def normalise_phone(phone: str) -> str:
    """Normalise AU phone numbers to E.164 format (+61XXXXXXXXX)."""
    if not phone:
        return ""
    digits = re.sub(r"[^\d+]", "", phone)
    # Convert 04xx (mobile) or 0X (landline) to +61X...
    if digits.startswith("0") and len(digits) >= 10 and not digits.startswith("+"):
        digits = "+61" + digits[1:]
    # Convert 61X... to +61X...
    elif digits.startswith("61") and not digits.startswith("+") and len(digits) >= 11:
        digits = "+" + digits
    return digits


def normalise_name(name: str) -> str:
    """Lowercase, strip punctuation for dedup matching."""
    return re.sub(r"[^a-z0-9\s]", "", name.lower()).strip()


# ---------------------------------------------------------------------------
# Source 1: Google Places API
# ---------------------------------------------------------------------------

def search_google_places(trade: str, location_key: str, limit: int = 20) -> list[dict]:
    """Search Google Places API for trade businesses in a location."""
    if not GOOGLE_PLACES_API_KEY:
        log.info("Skipping Google Places (no API key set — export GOOGLE_PLACES_API_KEY)")
        return []

    loc = SEQ_LOCATIONS[location_key]
    leads = []
    search_terms = TRADE_SEARCH_TERMS.get(trade, [trade])

    for term in search_terms[:1]:  # Use primary term only to avoid dupes
        query = f"{term} {loc['display']}"
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": query,
            "key": GOOGLE_PLACES_API_KEY,
            "region": "au",
            "type": "establishment",
        }

        resp = safe_get(url, params=params)
        if not resp:
            continue

        data = resp.json()
        results = data.get("results", [])
        log.info(f"Google Places: '{query}' → {len(results)} results")

        for place in results[:limit]:
            # Get details for phone number
            place_id = place.get("place_id")
            phone = ""
            website = ""

            if place_id:
                detail_url = "https://maps.googleapis.com/maps/api/place/details/json"
                detail_params = {
                    "place_id": place_id,
                    "fields": "formatted_phone_number,website,review",
                    "key": GOOGLE_PLACES_API_KEY,
                }
                detail_resp = safe_get(detail_url, params=detail_params)
                if detail_resp:
                    detail = detail_resp.json().get("result", {})
                    phone = detail.get("formatted_phone_number", "")
                    website = detail.get("website", "")
                rate_limit(0.5)  # Light rate limit for details

            if not phone:
                continue  # Skip leads without phone numbers

            lead = make_lead(
                business_name=place.get("name", ""),
                trade_type=trade,
                phone=phone,
                location=loc["display"],
                source="Google Places",
                website=website,
                google_rating=place.get("rating"),
                google_review_count=place.get("user_ratings_total"),
            )
            leads.append(lead)

        rate_limit()

    return leads


# ---------------------------------------------------------------------------
# Source 2: Yellow Pages Australia
# ---------------------------------------------------------------------------

def search_yellow_pages(trade: str, location_key: str, limit: int = 20) -> list[dict]:
    """Scrape Yellow Pages Australia for trade businesses."""
    loc = SEQ_LOCATIONS[location_key]
    leads = []
    search_terms = TRADE_SEARCH_TERMS.get(trade, [trade])
    term = search_terms[0]

    # Yellow Pages search URL format
    location_name = location_key.replace("-", "+")
    url = f"https://www.yellowpages.com.au/find/{quote_plus(term)}/{quote_plus(location_name)}-qld"

    log.info(f"Yellow Pages: searching '{term}' in {location_key}")
    resp = safe_get(url)
    if not resp:
        return leads

    soup = BeautifulSoup(resp.text, "html.parser")

    # Yellow Pages listing cards
    listings = soup.select("div.listing, div.search-contact-card, article.listing")
    if not listings:
        # Try alternative selectors
        listings = soup.select("[data-listing-id], .organic-result, .box-company")

    log.info(f"Yellow Pages: found {len(listings)} listing elements")

    for listing in listings[:limit]:
        try:
            # Business name
            name_el = (
                listing.select_one("h2 a, h3 a, .listing-name a, .business-name a")
                or listing.select_one("a.listing-name, a.business-name")
            )
            if not name_el:
                continue
            business_name = name_el.get_text(strip=True)

            # Phone number
            phone_el = listing.select_one(
                "a[href^='tel:'], .phone-number, .contact-phone, "
                "[data-phone], .call-number"
            )
            phone = ""
            if phone_el:
                phone = phone_el.get("href", "").replace("tel:", "") or phone_el.get_text(strip=True)
                phone = re.sub(r"[^\d+]", "", phone)

            if not phone:
                continue

            # Website
            website_el = listing.select_one("a.website-link, a[data-type='website'], a.visit-website")
            website = website_el.get("href", "") if website_el else ""

            # Address / location
            addr_el = listing.select_one(".listing-address, .address, .location")
            address = addr_el.get_text(strip=True) if addr_el else loc["display"]

            lead = make_lead(
                business_name=business_name,
                trade_type=trade,
                phone=phone,
                location=address if "QLD" in address.upper() else loc["display"],
                source="Yellow Pages",
                website=website,
            )
            leads.append(lead)

        except Exception as e:
            log.debug(f"Yellow Pages parse error: {e}")
            continue

    rate_limit()
    return leads


# ---------------------------------------------------------------------------
# Source 3: HiPages
# ---------------------------------------------------------------------------

def search_hipages(trade: str, location_key: str, limit: int = 20) -> list[dict]:
    """Scrape HiPages for trade businesses."""
    loc = SEQ_LOCATIONS[location_key]
    leads = []
    search_terms = TRADE_SEARCH_TERMS.get(trade, [trade])
    term = search_terms[0]

    # HiPages URL format
    slug_trade = term.replace(" ", "-").lower()
    slug_location = location_key.replace("-", "-")
    url = f"https://hipages.com.au/find/{quote_plus(slug_trade)}/{quote_plus(slug_location)}-qld"

    log.info(f"HiPages: searching '{term}' in {location_key}")
    resp = safe_get(url)
    if not resp:
        return leads

    soup = BeautifulSoup(resp.text, "html.parser")

    # HiPages uses various listing containers
    listings = soup.select(
        "div[data-testid='business-card'], .business-card, "
        ".search-result-card, article.result, div.listing-card"
    )
    if not listings:
        listings = soup.select("[class*='BusinessCard'], [class*='business-listing']")

    log.info(f"HiPages: found {len(listings)} listing elements")

    for listing in listings[:limit]:
        try:
            # Business name
            name_el = listing.select_one(
                "h2, h3, [data-testid='business-name'], "
                ".business-name, a[class*='BusinessName']"
            )
            if not name_el:
                continue
            business_name = name_el.get_text(strip=True)

            # Phone — HiPages sometimes hides phone behind a "Call" button
            phone_el = listing.select_one(
                "a[href^='tel:'], [data-testid='phone-number'], "
                ".phone-number, button[class*='phone']"
            )
            phone = ""
            if phone_el:
                href = phone_el.get("href", "")
                if "tel:" in href:
                    phone = href.replace("tel:", "")
                else:
                    phone = phone_el.get_text(strip=True)
                phone = re.sub(r"[^\d+]", "", phone)

            # HiPages often requires clicking to reveal phone; try data attributes
            if not phone:
                data_phone = listing.get("data-phone") or listing.get("data-business-phone")
                if data_phone:
                    phone = re.sub(r"[^\d+]", "", data_phone)

            if not phone:
                continue

            # Website link
            website_el = listing.select_one("a[class*='website'], a[data-testid='website-link']")
            website = website_el.get("href", "") if website_el else ""

            # Reviews
            review_el = listing.select_one("[class*='review-count'], [class*='ReviewCount']")
            review_count = None
            if review_el:
                nums = re.findall(r"\d+", review_el.get_text())
                review_count = int(nums[0]) if nums else None

            lead = make_lead(
                business_name=business_name,
                trade_type=trade,
                phone=phone,
                location=loc["display"],
                source="HiPages",
                website=website,
                google_review_count=review_count,
            )
            leads.append(lead)

        except Exception as e:
            log.debug(f"HiPages parse error: {e}")
            continue

    rate_limit()
    return leads


# ---------------------------------------------------------------------------
# Source 4: True Local
# ---------------------------------------------------------------------------

def search_truelocal(trade: str, location_key: str, limit: int = 20) -> list[dict]:
    """Scrape True Local for trade businesses."""
    loc = SEQ_LOCATIONS[location_key]
    leads = []
    search_terms = TRADE_SEARCH_TERMS.get(trade, [trade])
    term = search_terms[0]

    location_name = location_key.replace("-", "+")
    url = f"https://www.truelocal.com.au/find/{quote_plus(term)}/{quote_plus(location_name)}-qld"

    log.info(f"True Local: searching '{term}' in {location_key}")
    resp = safe_get(url)
    if not resp:
        return leads

    soup = BeautifulSoup(resp.text, "html.parser")

    listings = soup.select(
        "div.search-result, div.listing-card, article.business-card, "
        "div[class*='SearchResult'], div[class*='ListingCard']"
    )

    log.info(f"True Local: found {len(listings)} listing elements")

    for listing in listings[:limit]:
        try:
            name_el = listing.select_one("h2 a, h3 a, .business-name, a.listing-name")
            if not name_el:
                continue
            business_name = name_el.get_text(strip=True)

            phone_el = listing.select_one("a[href^='tel:'], .phone, .contact-number")
            phone = ""
            if phone_el:
                href = phone_el.get("href", "")
                phone = href.replace("tel:", "") if "tel:" in href else phone_el.get_text(strip=True)
                phone = re.sub(r"[^\d+]", "", phone)

            if not phone:
                continue

            website_el = listing.select_one("a.website, a[class*='website']")
            website = website_el.get("href", "") if website_el else ""

            # Rating
            rating_el = listing.select_one("[class*='rating'], .star-rating")
            rating = None
            if rating_el:
                nums = re.findall(r"[\d.]+", rating_el.get_text())
                rating = float(nums[0]) if nums else None

            lead = make_lead(
                business_name=business_name,
                trade_type=trade,
                phone=phone,
                location=loc["display"],
                source="True Local",
                website=website,
                google_rating=rating,
            )
            leads.append(lead)

        except Exception as e:
            log.debug(f"True Local parse error: {e}")
            continue

    rate_limit()
    return leads


# ---------------------------------------------------------------------------
# Lead enrichment
# ---------------------------------------------------------------------------

def enrich_lead(lead: dict) -> dict:
    """Enrich a lead with website analysis and Google review data."""
    website = lead.get("website")
    if not website:
        lead["website_quality"] = "none"
        lead["has_online_booking"] = False
        lead["has_chatbot"] = False
        lead = score_lead(lead)
        return lead

    log.info(f"Enriching: {lead['business_name']} — {website}")

    resp = safe_get(website, timeout=10)
    if not resp:
        lead["website_quality"] = "outdated"
        lead["has_online_booking"] = False
        lead["has_chatbot"] = False
        lead = score_lead(lead)
        return lead

    html = resp.text.lower()
    soup = BeautifulSoup(resp.text, "html.parser")

    # --- Online booking detection ---
    booking_signals = [
        "book online", "book now", "schedule appointment", "online booking",
        "bookings", "calendly", "acuity", "servicem8", "simpro",
        "tradify", "jobber", "housecall", "fieldpulse",
    ]
    has_booking = any(signal in html for signal in booking_signals)
    lead["has_online_booking"] = has_booking

    # --- Chatbot detection ---
    chatbot_signals = [
        "intercom", "drift", "tidio", "livechat", "zendesk",
        "hubspot", "crisp", "freshchat", "olark", "tawk.to",
        "chat-widget", "chatbot", "live chat",
    ]
    has_chatbot = any(signal in html for signal in chatbot_signals)
    lead["has_chatbot"] = has_chatbot

    # --- Website quality assessment ---
    quality_signals = {
        "modern": 0,
        "outdated": 0,
    }

    # Modern signals
    if any(fw in html for fw in ["react", "next.js", "vue", "tailwind", "webpack"]):
        quality_signals["modern"] += 2
    if "viewport" in html:
        quality_signals["modern"] += 1  # Responsive design
    if "https" in (website or ""):
        quality_signals["modern"] += 1
    if soup.select("meta[property^='og:']"):
        quality_signals["modern"] += 1  # Open Graph tags

    # Outdated signals
    if any(old in html for old in ["<table", "bgcolor", "<font", "frontpage", "<marquee"]):
        quality_signals["outdated"] += 2
    if not soup.select("meta[name='viewport']"):
        quality_signals["outdated"] += 2  # Not mobile responsive
    if "wordpress" in html and "theme" not in html:
        quality_signals["outdated"] += 1
    if "copyright 2020" in html or "copyright 2019" in html or "copyright 2018" in html:
        quality_signals["outdated"] += 1  # Stale copyright year
    if "wix.com" in html or "squarespace" in html:
        quality_signals["modern"] += 1  # Template builders are usually modern enough

    if quality_signals["outdated"] > quality_signals["modern"]:
        lead["website_quality"] = "outdated"
    else:
        lead["website_quality"] = "modern"

    # --- Try to find email address ---
    if not lead.get("email"):
        lead["email"] = try_extract_email(website, resp.text, soup)

    # --- Try to find contact name from About page ---
    if not lead.get("contact_name"):
        lead["contact_name"] = try_extract_contact_name(website, soup)

    # --- Add missing sequence tracking fields ---
    if "email_sequence_step" not in lead:
        lead["email_sequence_step"] = 0
    if "email_sequence_last_sent" not in lead:
        lead["email_sequence_last_sent"] = None

    rate_limit(ENRICHMENT_DELAY)

    lead = score_lead(lead)
    return lead


def try_extract_email(base_url: str, html_text: str, soup: BeautifulSoup) -> Optional[str]:
    """Try to extract a business email from the website."""
    # Regex for email addresses
    email_pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'

    # Exclusions — we don't want generic/spam addresses
    exclude_patterns = [
        "example.com", "sentry.io", "wixpress.com", "googleapis.com",
        "w3.org", "schema.org", "gravatar.com", "wordpress.com",
        "jquery.com", "cloudflare.com", "google.com", "facebook.com",
        "noreply", "no-reply", "donotreply", "unsubscribe",
    ]

    found_emails = set()

    # 1. Check mailto: links first (highest quality)
    for a_tag in soup.select("a[href^='mailto:']"):
        href = a_tag.get("href", "")
        email_match = re.search(email_pattern, href)
        if email_match:
            email = email_match.group(0).lower()
            if not any(ex in email for ex in exclude_patterns):
                found_emails.add(email)

    # 2. Scan page text for email patterns
    page_emails = re.findall(email_pattern, html_text)
    for email in page_emails:
        email = email.lower()
        if not any(ex in email for ex in exclude_patterns):
            found_emails.add(email)

    # 3. Try contact page
    if not found_emails:
        contact_urls = [
            urljoin(base_url, "/contact"),
            urljoin(base_url, "/contact-us"),
            urljoin(base_url, "/get-in-touch"),
        ]
        for contact_url in contact_urls:
            resp = safe_get(contact_url, timeout=8)
            if resp and resp.status_code == 200:
                contact_emails = re.findall(email_pattern, resp.text)
                for email in contact_emails:
                    email = email.lower()
                    if not any(ex in email for ex in exclude_patterns):
                        found_emails.add(email)
                if found_emails:
                    break
                rate_limit(0.5)

    if not found_emails:
        return None

    # Prefer info@, admin@, office@, contact@, or the business domain email
    priority_prefixes = ["info", "admin", "office", "contact", "hello", "enquiries", "enquiry"]
    for prefix in priority_prefixes:
        for email in found_emails:
            if email.startswith(prefix + "@"):
                return email

    # Return the first one found
    return next(iter(found_emails))


def try_extract_contact_name(base_url: str, home_soup: BeautifulSoup) -> Optional[str]:
    """Try to find the owner/contact name from the About page."""
    # Check home page first for common patterns
    for el in home_soup.select("h1, h2, h3, p, .about, .owner, .team-member"):
        text = el.get_text(strip=True)
        # Look for patterns like "Hi, I'm John" or "Owner: John Smith"
        patterns = [
            r"(?:owner|director|founder|manager|hi,?\s*i'?m)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()

    # Try about page
    about_urls = [
        urljoin(base_url, "/about"),
        urljoin(base_url, "/about-us"),
        urljoin(base_url, "/our-team"),
    ]

    for about_url in about_urls:
        resp = safe_get(about_url, timeout=8)
        if not resp or resp.status_code != 200:
            continue

        about_soup = BeautifulSoup(resp.text, "html.parser")
        for el in about_soup.select("h1, h2, h3, p, .about, .owner, .team"):
            text = el.get_text(strip=True)
            patterns = [
                r"(?:owner|director|founder|manager|hi,?\s*i'?m)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
                r"([A-Z][a-z]+\s+[A-Z][a-z]+)\s*(?:—|–|-|,)\s*(?:owner|director|founder|manager)",
            ]
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    return match.group(1).strip()
        rate_limit(0.5)

    return None


# ---------------------------------------------------------------------------
# Lead scoring
# ---------------------------------------------------------------------------

def score_lead(lead: dict) -> dict:
    """
    Score a lead 0–100 based on automation readiness.
    Higher score = better prospect for Velocity AI.
    """
    score = 0

    # --- Review volume (max 25 pts) ---
    reviews = lead.get("google_review_count") or 0
    if reviews >= 100:
        score += 25  # Very established, high call volume
    elif reviews >= 50:
        score += 20
    elif reviews >= 20:
        score += 15
    elif reviews >= 5:
        score += 10
    # Zero reviews = new business, less likely to afford service

    # --- Rating (max 10 pts) ---
    rating = lead.get("google_rating") or 0
    if rating >= 4.5:
        score += 10  # Good reputation, likely busy
    elif rating >= 4.0:
        score += 7
    elif rating >= 3.5:
        score += 3

    # --- No online booking = needs automation (max 20 pts) ---
    if lead.get("has_online_booking") is False:
        score += 20
    elif lead.get("has_online_booking") is None:
        score += 10  # Unknown, still likely needs it

    # --- No chatbot = needs automation (max 10 pts) ---
    if lead.get("has_chatbot") is False:
        score += 10
    elif lead.get("has_chatbot") is None:
        score += 5

    # --- Website quality (max 15 pts) ---
    quality = lead.get("website_quality")
    if quality == "none":
        score += 15  # No website at all — max need
    elif quality == "outdated":
        score += 12
    elif quality == "modern":
        score += 3

    # --- Phone-only contact (max 10 pts) ---
    if lead.get("phone") and not lead.get("email"):
        score += 10  # Relying on phone, needs automation

    # --- Team size / employee count (max 10 pts) ---
    employees = lead.get("employee_count") or 0
    if employees >= 10:
        score += 10  # Can afford the service
    elif employees >= 5:
        score += 7
    elif employees >= 2:
        score += 4

    lead["lead_score"] = min(score, 100)
    return lead


# ---------------------------------------------------------------------------
# Leads file management
# ---------------------------------------------------------------------------

def load_leads() -> list[dict]:
    """Load existing leads from JSON file."""
    if not LEADS_PATH.exists():
        return []
    try:
        with open(LEADS_PATH, "r") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError) as e:
        log.warning(f"Error loading leads.json: {e}")
        return []


def save_leads(leads: list[dict]):
    """Save leads to JSON file."""
    LEADS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LEADS_PATH, "w") as f:
        json.dump(leads, f, indent=2, default=str)
    log.info(f"Saved {len(leads)} leads to {LEADS_PATH}")


def deduplicate(existing: list[dict], new_leads: list[dict]) -> list[dict]:
    """
    Deduplicate new leads against existing ones.
    Match by normalised phone number OR normalised business name.
    """
    existing_phones = set()
    existing_names = set()

    for lead in existing:
        phone = normalise_phone(lead.get("phone", ""))
        if phone:
            existing_phones.add(phone)
        name = normalise_name(lead.get("business_name", ""))
        if name:
            existing_names.add(name)

    unique = []
    for lead in new_leads:
        phone = normalise_phone(lead.get("phone", ""))
        name = normalise_name(lead.get("business_name", ""))

        if phone and phone in existing_phones:
            log.debug(f"Dedup (phone): {lead['business_name']}")
            continue
        if name and name in existing_names:
            log.debug(f"Dedup (name): {lead['business_name']}")
            continue

        unique.append(lead)
        # Add to sets so we don't add duplicates from within new_leads either
        if phone:
            existing_phones.add(phone)
        if name:
            existing_names.add(name)

    return unique


# ---------------------------------------------------------------------------
# Search orchestration
# ---------------------------------------------------------------------------

def search_all_sources(trade: str, location_key: str, limit: int = 20) -> list[dict]:
    """Search all sources for a given trade + location combo."""
    all_leads = []

    # Google Places
    leads = search_google_places(trade, location_key, limit=limit)
    all_leads.extend(leads)

    # Yellow Pages
    leads = search_yellow_pages(trade, location_key, limit=limit)
    all_leads.extend(leads)

    # HiPages
    leads = search_hipages(trade, location_key, limit=limit)
    all_leads.extend(leads)

    # True Local
    leads = search_truelocal(trade, location_key, limit=limit)
    all_leads.extend(leads)

    # Internal dedup (across sources for this search)
    unique = deduplicate([], all_leads)
    log.info(f"Found {len(unique)} unique leads for {trade} in {location_key}")
    return unique


def run_search(trades: list[str], locations: list[str], limit: int = 20) -> list[dict]:
    """Run search across all specified trades and locations."""
    all_new = []

    total_combos = len(trades) * len(locations)
    log.info(f"Searching {total_combos} trade/location combinations...")

    for trade in trades:
        for location_key in locations:
            log.info(f"--- {trade.upper()} in {location_key.upper()} ---")
            leads = search_all_sources(trade, location_key, limit=limit)
            all_new.extend(leads)

    # Dedup across all combos
    all_new = deduplicate([], all_new)
    return all_new


def run_enrichment(leads: list[dict], batch: int = 0, missing_only: bool = False) -> list[dict]:
    """Enrich and re-score leads.

    Args:
        leads: Full list of leads (modified in place).
        batch: If > 0, only process this many leads. Prioritises leads
               missing email addresses, then leads missing websites.
        missing_only: If True, only process leads that don't have an email yet.
    """
    # Build the processing queue
    if missing_only:
        indices = [i for i, l in enumerate(leads) if not l.get("email")]
        log.info(f"Found {len(indices)} leads missing emails (out of {len(leads)} total)")
    else:
        # Prioritise: missing email first, then missing website, then the rest
        no_email = [i for i, l in enumerate(leads) if not l.get("email")]
        no_website = [i for i, l in enumerate(leads) if l.get("email") and not l.get("website")]
        rest = [i for i, l in enumerate(leads) if l.get("email") and l.get("website")]
        indices = no_email + no_website + rest
        log.info(f"Enrichment queue: {len(no_email)} missing email, "
                 f"{len(no_website)} missing website, {len(rest)} complete")

    if batch > 0:
        indices = indices[:batch]
        log.info(f"Batch mode: processing {len(indices)} leads")

    total = len(indices)
    log.info(f"Enriching {total} leads...")
    for count, idx in enumerate(indices, 1):
        log.info(f"[{count}/{total}] {leads[idx]['business_name']}")
        leads[idx] = enrich_lead(leads[idx])
    return leads


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_summary(existing_count: int, new_leads: list[dict], all_leads: list[dict]):
    """Print a summary of the search run."""
    print("\n" + "=" * 60)
    print("  VELOCITY AI — Lead Research Summary")
    print("=" * 60)
    print(f"  Existing leads:  {existing_count}")
    print(f"  New leads found: {len(new_leads)}")
    print(f"  Total leads now: {len(all_leads)}")
    print("-" * 60)

    if new_leads:
        # Sort by score descending
        scored = sorted(new_leads, key=lambda x: x.get("lead_score", 0), reverse=True)
        print("  Top 5 new leads by score:")
        print()
        for i, lead in enumerate(scored[:5], 1):
            score = lead.get("lead_score", 0)
            name = lead["business_name"]
            trade = lead["trade_type"]
            loc = lead["location"]
            source = lead["lead_source"]
            print(f"  {i}. [{score:3d} pts] {name}")
            print(f"     {trade} · {loc} · via {source}")
            phone = lead.get("phone", "")
            website = lead.get("website", "No website")
            print(f"     {phone}  |  {website}")
            print()
    else:
        print("  No new leads found this run.")

    print("=" * 60)


def print_full_summary(leads: list[dict]):
    """Print summary of all leads."""
    print("\n" + "=" * 60)
    print("  VELOCITY AI — Lead Database Summary")
    print("=" * 60)
    print(f"  Total leads: {len(leads)}")
    print()

    # By status
    statuses = {}
    for lead in leads:
        s = lead.get("status", "unknown")
        statuses[s] = statuses.get(s, 0) + 1
    print("  By status:")
    for status, count in sorted(statuses.items()):
        print(f"    {status:20s} {count}")

    # By trade
    print()
    trades = {}
    for lead in leads:
        t = lead.get("trade_type", "Unknown")
        trades[t] = trades.get(t, 0) + 1
    print("  By trade:")
    for trade, count in sorted(trades.items(), key=lambda x: -x[1]):
        print(f"    {trade:20s} {count}")

    # By source
    print()
    sources = {}
    for lead in leads:
        s = lead.get("lead_source", "Unknown")
        sources[s] = sources.get(s, 0) + 1
    print("  By source:")
    for source, count in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"    {source:20s} {count}")

    # Top scored
    scored = sorted(leads, key=lambda x: x.get("lead_score", 0), reverse=True)
    top = [l for l in scored if l.get("lead_score", 0) > 0]
    if top:
        print()
        print("  Top 10 by lead score:")
        for i, lead in enumerate(top[:10], 1):
            print(f"    {i:2d}. [{lead['lead_score']:3d}] {lead['business_name']} ({lead['trade_type']})")

    print("\n" + "=" * 60)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Velocity AI — Lead Research Engine for SEQ trade businesses",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --trade plumbing --location brisbane --limit 10
  %(prog)s --trade electrical --trade roofing --location gold-coast
  %(prog)s --all
  %(prog)s --all --limit 5
  %(prog)s --enrich
  %(prog)s --enrich --batch 10 --missing-only
  %(prog)s --summary
        """,
    )

    parser.add_argument(
        "--trade", action="append", dest="trades",
        choices=TRADE_CATEGORIES,
        help="Trade category to search (can specify multiple)",
    )
    parser.add_argument(
        "--location", action="append", dest="locations",
        help=f"SEQ location to search. Options: {', '.join(SEQ_LOCATIONS.keys())}",
    )
    parser.add_argument(
        "--limit", type=int, default=20,
        help="Max results per source per search (default: 20)",
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Search all trades in all SEQ locations",
    )
    parser.add_argument(
        "--enrich", action="store_true",
        help="Re-enrich and re-score existing leads",
    )
    parser.add_argument(
        "--batch", type=int, default=0,
        help="Limit enrichment to N leads (prioritises leads missing emails). "
             "Use with --enrich. 0 = process all (default: 0)",
    )
    parser.add_argument(
        "--missing-only", action="store_true",
        help="Only enrich leads that don't have an email address yet. "
             "Use with --enrich.",
    )
    parser.add_argument(
        "--summary", action="store_true",
        help="Show summary of current lead database",
    )
    parser.add_argument(
        "--score-only", action="store_true",
        help="Re-score existing leads without web requests",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Search but don't save results",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable debug logging",
    )

    return parser


def resolve_locations(raw: list[str]) -> list[str]:
    """Resolve location aliases to canonical keys."""
    resolved = []
    for loc in raw:
        key = loc.lower().strip().replace(" ", "-")
        canonical = LOCATION_ALIASES.get(key)
        if not canonical:
            log.warning(f"Unknown location '{loc}'. Valid: {', '.join(SEQ_LOCATIONS.keys())}")
            continue
        resolved.append(canonical)
    return resolved


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # --- Summary mode ---
    if args.summary:
        leads = load_leads()
        print_full_summary(leads)
        return

    # --- Score-only mode ---
    if args.score_only:
        leads = load_leads()
        log.info(f"Re-scoring {len(leads)} leads...")
        for i, lead in enumerate(leads):
            leads[i] = score_lead(lead)
        save_leads(leads)
        print_full_summary(leads)
        return

    # --- Enrich mode ---
    if args.enrich:
        leads = load_leads()
        if not leads:
            log.warning("No leads to enrich. Run a search first.")
            return
        leads = run_enrichment(
            leads,
            batch=args.batch,
            missing_only=args.missing_only,
        )
        save_leads(leads)
        print_full_summary(leads)
        return

    # --- Search mode ---
    if args.all:
        trades = TRADE_CATEGORIES
        locations = list(SEQ_LOCATIONS.keys())
    elif args.trades and args.locations:
        trades = args.trades
        locations = resolve_locations(args.locations)
        if not locations:
            parser.error("No valid locations specified.")
    else:
        parser.error("Specify --trade and --location, or use --all. See --help.")

    # Load existing leads
    existing = load_leads()
    existing_count = len(existing)

    # Run search
    new_leads = run_search(trades, locations, limit=args.limit)

    # Deduplicate against existing
    new_leads = deduplicate(existing, new_leads)

    if not args.dry_run and new_leads:
        # Append new leads
        all_leads = existing + new_leads
        save_leads(all_leads)
    else:
        all_leads = existing + new_leads
        if args.dry_run:
            log.info("Dry run — no changes saved.")

    print_summary(existing_count, new_leads, all_leads)


if __name__ == "__main__":
    main()
