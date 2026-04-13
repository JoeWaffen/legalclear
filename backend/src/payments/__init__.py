from .stripe_client import StripeClient

def check_access(user: dict, session: dict) -> dict:
    if user.get('subscription_status') == 'active':
        return {"allowed": True, "reason": "Subscription active", "payment_type": "subscription"}
    elif not user.get('free_doc_used'):
        return {"allowed": True, "reason": "Free document available", "payment_type": "free"}
    elif session.get('payment_status') == 'paid':
        return {"allowed": True, "reason": "Pay-as-you-go paid", "payment_type": "payg"}
    else:
        return {"allowed": False, "reason": "Payment required", "payment_type": "none"}
