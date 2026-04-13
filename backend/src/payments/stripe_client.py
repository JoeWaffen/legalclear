import stripe
from src.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeClient:
    def __init__(self):
        self.secret = settings.STRIPE_SECRET_KEY

    def create_payment_intent(self, price_usd: int, session_id: str, user_email: str, metadata: dict) -> dict:
        if not self.secret:
            return {"client_secret": "mock_secret", "payment_intent_id": "mock_pi"}
        try:
            intent = stripe.PaymentIntent.create(
                amount=price_usd * 100,
                currency='usd',
                receipt_email=user_email,
                metadata={**metadata, "session_id": session_id}
            )
            return {"client_secret": intent.client_secret, "payment_intent_id": intent.id}
        except Exception as e:
            return {"error": str(e)}

    def create_subscription_checkout(self, user_email: str, user_id: str, success_url: str, cancel_url: str) -> dict:
        if not self.secret:
            return {"checkout_url": "http://mock-checkout.com", "session_id": "mock_cs"}
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': settings.STRIPE_SUBSCRIPTION_PRICE_ID,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=user_email,
                client_reference_id=user_id
            )
            return {"checkout_url": session.url, "session_id": session.id}
        except Exception as e:
            return {"error": str(e)}

    def create_or_get_customer(self, email: str) -> str:
        if not self.secret: return "cus_mock"
        try:
            customers = stripe.Customer.list(email=email, limit=1)
            if customers.data:
                return customers.data[0].id
            new_customer = stripe.Customer.create(email=email)
            return new_customer.id
        except Exception:
            return "cus_mock_fallback"

    def cancel_subscription(self, subscription_id: str) -> bool:
        if not self.secret: return True
        try:
            stripe.Subscription.modify(subscription_id, cancel_at_period_end=True)
            return True
        except Exception:
            return False

    def verify_webhook(self, payload: bytes, sig_header: str) -> dict:
        if not self.secret: return json.loads(payload)
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except Exception as e:
            raise ValueError(f"Invalid webhook: {e}")

    def get_payment_status(self, payment_intent_id: str) -> str:
        if not self.secret: return "succeeded"
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return intent.status
        except Exception:
            return "unknown"
