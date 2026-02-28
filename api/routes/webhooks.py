from fastapi import APIRouter, Request, Header
from typing import Optional

from api.core.config import get_settings
from api.core.logging import get_logger

router = APIRouter()
settings = get_settings()
logger = get_logger(__name__)


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: Optional[str] = Header(None),
):
    """Handle Stripe webhook events for payment processing."""
    payload = await request.body()

    if not settings.STRIPE_WEBHOOK_SECRET:
        logger.warning("stripe_webhook_received_but_no_secret_configured")
        return {"status": "ignored", "reason": "webhook secret not configured"}

    try:
        import stripe

        stripe.api_key = settings.STRIPE_SECRET_KEY
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, settings.STRIPE_WEBHOOK_SECRET
        )

        event_type = event["type"]
        logger.info("stripe_webhook_received", event_type=event_type)

        if event_type == "checkout.session.completed":
            session = event["data"]["object"]
            logger.info(
                "payment_completed",
                customer_email=session.get("customer_email"),
                amount=session.get("amount_total"),
            )

        elif event_type == "customer.subscription.deleted":
            subscription = event["data"]["object"]
            logger.info(
                "subscription_cancelled",
                customer=subscription.get("customer"),
            )

        elif event_type == "invoice.payment_failed":
            invoice = event["data"]["object"]
            logger.warning(
                "payment_failed",
                customer=invoice.get("customer"),
            )

        return {"status": "processed", "event_type": event_type}

    except Exception as e:
        logger.error("stripe_webhook_error", error=str(e))
        return {"status": "error", "message": str(e)}
