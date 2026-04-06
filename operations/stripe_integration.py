#!/usr/bin/env python3
"""
Velocity AI — Stripe Integration Module
==========================================
Handles all Stripe interactions: customers, subscriptions, payments,
checkout sessions, and webhook processing.

Usage:
    from stripe_integration import StripeManager
    sm = StripeManager()

    # Create a customer
    customer = sm.create_customer("John Smith", "john@example.com", metadata={"trade": "plumber"})

    # Create a checkout session for setup deposit + subscription
    session = sm.create_checkout_session(
        customer_id=customer.id,
        tier="professional",
        billing="monthly",
    )

    # Manage subscriptions
    sub = sm.get_subscription(subscription_id)
    sm.cancel_subscription(subscription_id)

    # Process webhook events
    event = sm.verify_webhook(payload, sig_header)
"""

import os
import logging
from typing import Optional

import stripe

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
except ImportError:
    pass

log = logging.getLogger("stripe-integration")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "")

# Price IDs — mapped from Stripe sandbox setup
# These are populated from the test environment. Update when switching to live.
PRICE_IDS = {
    # Monthly subscriptions
    "starter_monthly": "price_1TJ7WZIwmeZH7II9pYW4Zsx1",
    "professional_monthly": "price_1TJ7WbIwmeZH7II9ocZmjVrF",
    "enterprise_monthly": "price_1TJ7WdIwmeZH7II9R4QQ9yYs",
    # Annual subscriptions (10% discount)
    "starter_annual": "price_1TJ7WZIwmeZH7II9YnAvV2us",
    "professional_annual": "price_1TJ7WbIwmeZH7II9HRT3ePOD",
    "enterprise_annual": "price_1TJ7WeIwmeZH7II9NQQ5BWL0",
    # Setup deposits (50%)
    "starter_setup_deposit": "price_1TJ7WaIwmeZH7II97pvhM3tl",
    "professional_setup_deposit": "price_1TJ7WcIwmeZH7II9swaxqKdI",
    "enterprise_setup_deposit": "price_1TJ7WeIwmeZH7II9DVcprb98",
    # Setup final payments (50%)
    "starter_setup_final": "price_1TJ7WaIwmeZH7II9BS0nqpz9",
    "professional_setup_final": "price_1TJ7WdIwmeZH7II9QE7l3xqQ",
    "enterprise_setup_final": "price_1TJ7WfIwmeZH7II9IOc0ReOJ",
    # Add-ons (recurring)
    "extra_voice_minutes": "price_1TJ7WgIwmeZH7II9i1POrr7C",
    "outbound_calling": "price_1TJ7WgIwmeZH7II9KC3r5Sm5",
    "google_ads": "price_1TJ7WhIwmeZH7II9LK7vLQ0p",
    "social_media": "price_1TJ7WiIwmeZH7II9QS9n9cCv",
    # Add-ons (one-time)
    "website_build": "price_1TJ7WiIwmeZH7II9NJLzuynW",
    "custom_integration": "price_1TJ7WjIwmeZH7II9QYP6oBtD",
    "training_session": "price_1TJ7WkIwmeZH7II9G47If8ua",
    "annual_audit": "price_1TJ7WkIwmeZH7II9wh2euyJP",
}

VALID_TIERS = ("starter", "professional", "enterprise")
VALID_BILLING = ("monthly", "annual")


# ---------------------------------------------------------------------------
# Stripe Manager
# ---------------------------------------------------------------------------

class StripeManager:
    """Manages all Stripe operations for Velocity AI."""

    # -- Customer Management --

    def create_customer(
        self,
        name: str,
        email: str,
        phone: str = "",
        metadata: Optional[dict] = None,
    ) -> stripe.Customer:
        """Create a new Stripe customer."""
        params = {
            "name": name,
            "email": email,
            "metadata": metadata or {},
        }
        if phone:
            params["phone"] = phone

        customer = stripe.Customer.create(**params)
        log.info(f"Created customer: {customer.id} ({name}, {email})")
        return customer

    def get_customer(self, customer_id: str) -> stripe.Customer:
        """Retrieve a customer by ID."""
        return stripe.Customer.retrieve(customer_id)

    def find_customer_by_email(self, email: str) -> Optional[stripe.Customer]:
        """Find an existing customer by email."""
        results = stripe.Customer.list(email=email, limit=1)
        return results.data[0] if results.data else None

    def update_customer(self, customer_id: str, **kwargs) -> stripe.Customer:
        """Update customer fields (name, email, metadata, etc.)."""
        customer = stripe.Customer.modify(customer_id, **kwargs)
        log.info(f"Updated customer: {customer_id}")
        return customer

    # -- Checkout Sessions --

    def create_checkout_session(
        self,
        customer_id: str,
        tier: str,
        billing: str = "monthly",
        success_url: str = "https://velocityai.com.au/welcome?session_id={CHECKOUT_SESSION_ID}",
        cancel_url: str = "https://velocityai.com.au/pricing",
        include_setup_deposit: bool = True,
    ) -> stripe.checkout.Session:
        """
        Create a Stripe Checkout session for a new customer sign-up.

        This combines the setup deposit (one-time) with the subscription
        in a single checkout flow.
        """
        if tier not in VALID_TIERS:
            raise ValueError(f"Invalid tier: {tier}. Must be one of {VALID_TIERS}")
        if billing not in VALID_BILLING:
            raise ValueError(f"Invalid billing: {billing}. Must be one of {VALID_BILLING}")

        sub_price_key = f"{tier}_{billing}"
        sub_price_id = PRICE_IDS.get(sub_price_key)
        if not sub_price_id:
            raise ValueError(f"No price found for {sub_price_key}")

        line_items = []

        # Add setup deposit if requested
        if include_setup_deposit:
            deposit_price_id = PRICE_IDS.get(f"{tier}_setup_deposit")
            if deposit_price_id:
                line_items.append({"price": deposit_price_id, "quantity": 1})

        # Add subscription
        line_items.append({"price": sub_price_id, "quantity": 1})

        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=line_items,
            mode="subscription" if not include_setup_deposit else "subscription",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "tier": tier,
                "billing": billing,
                "service": "velocity-ai",
            },
            subscription_data={
                "metadata": {
                    "tier": tier,
                    "billing": billing,
                },
            },
        )
        log.info(f"Created checkout session: {session.id} for customer {customer_id} ({tier}/{billing})")
        return session

    def create_payment_link(
        self,
        tier: str,
        billing: str = "monthly",
        include_setup_deposit: bool = True,
    ) -> stripe.PaymentLink:
        """Create a reusable payment link for a tier (shareable via email/SMS)."""
        if tier not in VALID_TIERS:
            raise ValueError(f"Invalid tier: {tier}")

        line_items = []

        if include_setup_deposit:
            deposit_price_id = PRICE_IDS.get(f"{tier}_setup_deposit")
            if deposit_price_id:
                line_items.append({"price": deposit_price_id, "quantity": 1})

        sub_price_id = PRICE_IDS.get(f"{tier}_{billing}")
        line_items.append({"price": sub_price_id, "quantity": 1})

        link = stripe.PaymentLink.create(
            line_items=line_items,
            metadata={"tier": tier, "billing": billing},
            after_completion={"type": "redirect", "redirect": {"url": "https://velocityai.com.au/welcome"}},
        )
        log.info(f"Created payment link: {link.url} ({tier}/{billing})")
        return link

    # -- Subscription Management --

    def create_subscription(
        self,
        customer_id: str,
        tier: str,
        billing: str = "monthly",
        addon_keys: Optional[list] = None,
    ) -> stripe.Subscription:
        """Create a subscription directly (e.g. after manual payment collection)."""
        price_key = f"{tier}_{billing}"
        price_id = PRICE_IDS.get(price_key)
        if not price_id:
            raise ValueError(f"No price found for {price_key}")

        items = [{"price": price_id}]

        # Add any add-ons
        if addon_keys:
            for key in addon_keys:
                addon_price = PRICE_IDS.get(key)
                if addon_price:
                    items.append({"price": addon_price})

        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=items,
            metadata={"tier": tier, "billing": billing},
        )
        log.info(f"Created subscription: {subscription.id} for {customer_id} ({tier}/{billing})")
        return subscription

    def get_subscription(self, subscription_id: str) -> stripe.Subscription:
        """Retrieve a subscription by ID."""
        return stripe.Subscription.retrieve(subscription_id)

    def update_subscription_tier(
        self,
        subscription_id: str,
        new_tier: str,
        billing: str = "monthly",
    ) -> stripe.Subscription:
        """Upgrade or downgrade a subscription to a different tier."""
        sub = stripe.Subscription.retrieve(subscription_id)
        new_price_id = PRICE_IDS.get(f"{new_tier}_{billing}")
        if not new_price_id:
            raise ValueError(f"No price for {new_tier}_{billing}")

        # Find the main subscription item (not add-ons)
        main_item = None
        for item in sub["items"]["data"]:
            if item["price"]["metadata"].get("type") != "addon":
                main_item = item
                break

        if not main_item:
            raise ValueError("Could not find main subscription item")

        updated = stripe.Subscription.modify(
            subscription_id,
            items=[{"id": main_item.id, "price": new_price_id}],
            metadata={"tier": new_tier, "billing": billing},
            proration_behavior="create_prorations",
        )
        log.info(f"Updated subscription {subscription_id}: → {new_tier}/{billing}")
        return updated

    def add_addon_to_subscription(
        self,
        subscription_id: str,
        addon_key: str,
    ) -> stripe.Subscription:
        """Add an add-on to an existing subscription."""
        addon_price = PRICE_IDS.get(addon_key)
        if not addon_price:
            raise ValueError(f"Unknown add-on: {addon_key}")

        updated = stripe.Subscription.modify(
            subscription_id,
            items=[{"price": addon_price}],
        )
        log.info(f"Added add-on {addon_key} to subscription {subscription_id}")
        return updated

    def cancel_subscription(
        self,
        subscription_id: str,
        at_period_end: bool = True,
    ) -> stripe.Subscription:
        """Cancel a subscription (default: at end of current billing period)."""
        if at_period_end:
            sub = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True,
            )
            log.info(f"Subscription {subscription_id} set to cancel at period end")
        else:
            sub = stripe.Subscription.cancel(subscription_id)
            log.info(f"Subscription {subscription_id} cancelled immediately")
        return sub

    def reactivate_subscription(self, subscription_id: str) -> stripe.Subscription:
        """Reactivate a subscription that was set to cancel at period end."""
        sub = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=False,
        )
        log.info(f"Subscription {subscription_id} reactivated")
        return sub

    # -- One-Time Payments (Setup fees, add-ons) --

    def charge_setup_final(
        self,
        customer_id: str,
        tier: str,
    ) -> stripe.PaymentIntent:
        """Charge the final 50% setup fee (triggered on go-live, Day 14)."""
        price_id = PRICE_IDS.get(f"{tier}_setup_final")
        if not price_id:
            raise ValueError(f"No setup final price for {tier}")

        # Look up the price to get the amount
        price = stripe.Price.retrieve(price_id)

        intent = stripe.PaymentIntent.create(
            amount=price.unit_amount,
            currency="aud",
            customer=customer_id,
            description=f"Velocity AI {tier.title()} — Final Setup Payment (50%)",
            metadata={"tier": tier, "type": "setup_final"},
        )
        log.info(f"Created payment intent for setup final: {intent.id} ({tier})")
        return intent

    def create_invoice_for_onetime(
        self,
        customer_id: str,
        price_key: str,
        description: str = "",
    ) -> stripe.Invoice:
        """Create and send an invoice for a one-time charge (e.g. website build)."""
        price_id = PRICE_IDS.get(price_key)
        if not price_id:
            raise ValueError(f"Unknown price key: {price_key}")

        # Add invoice item
        stripe.InvoiceItem.create(
            customer=customer_id,
            price=price_id,
            description=description,
        )

        # Create and finalize invoice
        invoice = stripe.Invoice.create(
            customer=customer_id,
            auto_advance=True,  # Auto-finalize and send
            metadata={"type": "onetime", "item": price_key},
        )
        log.info(f"Created invoice {invoice.id} for {price_key}")
        return invoice

    # -- Webhook Processing --

    def verify_webhook(self, payload: str, sig_header: str) -> stripe.Event:
        """Verify and parse a Stripe webhook event."""
        if not STRIPE_WEBHOOK_SECRET:
            log.warning("STRIPE_WEBHOOK_SECRET not set — skipping signature verification")
            return stripe.Event.construct_from(
                __import__("json").loads(payload), stripe.api_key
            )

        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
        return event

    def handle_webhook_event(self, event: stripe.Event) -> dict:
        """
        Process a Stripe webhook event and return action details.

        Returns:
            dict with keys: status, action, details
        """
        event_type = event.type
        data = event.data.object

        handlers = {
            "checkout.session.completed": self._handle_checkout_completed,
            "customer.subscription.created": self._handle_subscription_created,
            "customer.subscription.updated": self._handle_subscription_updated,
            "customer.subscription.deleted": self._handle_subscription_deleted,
            "invoice.paid": self._handle_invoice_paid,
            "invoice.payment_failed": self._handle_invoice_payment_failed,
            "payment_intent.succeeded": self._handle_payment_succeeded,
            "payment_intent.payment_failed": self._handle_payment_failed,
            "customer.created": self._handle_customer_created,
            "customer.updated": self._handle_customer_updated,
        }

        handler = handlers.get(event_type)
        if handler:
            return handler(data)

        log.info(f"Unhandled event type: {event_type}")
        return {"status": "ignored", "action": "none", "event": event_type}

    # -- Webhook Event Handlers --

    def _handle_checkout_completed(self, session) -> dict:
        email = session.get("customer_details", {}).get("email", "")
        name = session.get("customer_details", {}).get("name", "")
        tier = session.get("metadata", {}).get("tier", "unknown")
        amount = (session.get("amount_total", 0) or 0) / 100

        log.info(f"Checkout completed: {name} ({email}) — ${amount:.2f} AUD [{tier}]")

        return {
            "status": "processed",
            "action": "onboarding_triggered",
            "customer_email": email,
            "customer_name": name,
            "tier": tier,
            "amount": amount,
        }

    def _handle_subscription_created(self, subscription) -> dict:
        customer_id = subscription.get("customer", "")
        tier = subscription.get("metadata", {}).get("tier", "unknown")
        status = subscription.get("status", "")

        log.info(f"Subscription created: {subscription.get('id')} [{tier}] status={status}")

        return {
            "status": "processed",
            "action": "subscription_created",
            "subscription_id": subscription.get("id"),
            "customer_id": customer_id,
            "tier": tier,
            "subscription_status": status,
        }

    def _handle_subscription_updated(self, subscription) -> dict:
        log.info(f"Subscription updated: {subscription.get('id')} status={subscription.get('status')}")
        return {
            "status": "processed",
            "action": "subscription_updated",
            "subscription_id": subscription.get("id"),
            "subscription_status": subscription.get("status"),
        }

    def _handle_subscription_deleted(self, subscription) -> dict:
        customer_id = subscription.get("customer", "")
        log.info(f"Subscription cancelled: {subscription.get('id')} customer={customer_id}")

        return {
            "status": "processed",
            "action": "churn_flagged",
            "subscription_id": subscription.get("id"),
            "customer_id": customer_id,
        }

    def _handle_invoice_paid(self, invoice) -> dict:
        email = invoice.get("customer_email", "")
        amount = (invoice.get("amount_paid", 0) or 0) / 100

        log.info(f"Invoice paid: {email} — ${amount:.2f} AUD")

        return {
            "status": "processed",
            "action": "payment_recorded",
            "customer_email": email,
            "amount": amount,
            "invoice_id": invoice.get("id"),
        }

    def _handle_invoice_payment_failed(self, invoice) -> dict:
        email = invoice.get("customer_email", "")
        amount = (invoice.get("amount_due", 0) or 0) / 100

        log.warning(f"Payment failed: {email} — ${amount:.2f} AUD")

        return {
            "status": "processed",
            "action": "payment_failed",
            "customer_email": email,
            "amount": amount,
            "invoice_id": invoice.get("id"),
            "next_attempt": invoice.get("next_payment_attempt"),
        }

    def _handle_payment_succeeded(self, intent) -> dict:
        amount = (intent.get("amount", 0) or 0) / 100
        log.info(f"Payment succeeded: ${amount:.2f} AUD")
        return {
            "status": "processed",
            "action": "payment_succeeded",
            "amount": amount,
            "payment_intent_id": intent.get("id"),
        }

    def _handle_payment_failed(self, intent) -> dict:
        amount = (intent.get("amount", 0) or 0) / 100
        log.warning(f"Payment failed: ${amount:.2f} AUD")
        return {
            "status": "processed",
            "action": "payment_failed",
            "amount": amount,
            "payment_intent_id": intent.get("id"),
            "error": intent.get("last_payment_error", {}).get("message", ""),
        }

    def _handle_customer_created(self, customer) -> dict:
        log.info(f"Customer created: {customer.get('id')} ({customer.get('email')})")
        return {
            "status": "processed",
            "action": "customer_created",
            "customer_id": customer.get("id"),
            "email": customer.get("email"),
        }

    def _handle_customer_updated(self, customer) -> dict:
        log.info(f"Customer updated: {customer.get('id')}")
        return {
            "status": "processed",
            "action": "customer_updated",
            "customer_id": customer.get("id"),
        }


# ---------------------------------------------------------------------------
# Convenience functions (module-level)
# ---------------------------------------------------------------------------

_manager = None

def get_manager() -> StripeManager:
    """Get or create the singleton StripeManager."""
    global _manager
    if _manager is None:
        _manager = StripeManager()
    return _manager


def get_price_id(key: str) -> str:
    """Look up a price ID by key name."""
    return PRICE_IDS.get(key, "")


def list_available_prices() -> dict:
    """Return all available price keys grouped by category."""
    return {
        "subscriptions": {
            "monthly": {t: PRICE_IDS[f"{t}_monthly"] for t in VALID_TIERS},
            "annual": {t: PRICE_IDS[f"{t}_annual"] for t in VALID_TIERS},
        },
        "setup_fees": {
            "deposit": {t: PRICE_IDS[f"{t}_setup_deposit"] for t in VALID_TIERS},
            "final": {t: PRICE_IDS[f"{t}_setup_final"] for t in VALID_TIERS},
        },
        "addons": {
            k: v for k, v in PRICE_IDS.items()
            if k not in [f"{t}_{b}" for t in VALID_TIERS for b in ("monthly", "annual", "setup_deposit", "setup_final")]
        },
    }
