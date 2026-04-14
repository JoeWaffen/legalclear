from supabase import create_client, Client
from src.core.config import settings
import uuid
import datetime

class DatabaseManager:
    def __init__(self):
        self.url: str = settings.SUPABASE_URL
        self.key: str = settings.SUPABASE_SERVICE_KEY
        if self.url and self.key:
            self.supabase: Client = create_client(self.url, self.key)
        else:
            self.supabase = None

    def get_or_create_user(self, email: str, preferred_language: str = 'en') -> dict:
        if not self.supabase:
            return {"id": str(uuid.uuid4()), "email": email, "subscription_status": "free", "free_doc_used": False, "preferred_language": preferred_language}
        try:
            res = self.supabase.table('users').select('*').eq('email', email).execute()
            if res.data:
                return res.data[0]
            new_user = {"email": email, "preferred_language": preferred_language}
            res = self.supabase.table('users').insert(new_user).execute()
            return res.data[0]
        except Exception:
            return {"id": str(uuid.uuid4()), "email": email, "subscription_status": "free", "free_doc_used": False}

    def update_user_subscription(self, user_id: str, status: str, subscription_id: str):
        if not self.supabase: return
        self.supabase.table('users').update({
            "subscription_status": status,
            "subscription_id": subscription_id
        }).eq("id", user_id).execute()

    def get_user(self, user_id: str) -> dict:
        if not self.supabase: return {"id": user_id, "subscription_status": "free"}
        try:
            res = self.supabase.table('users').select('*').eq('id', user_id).execute()
        except Exception:
            return {"id": user_id, "subscription_status": "free"}
        if not res.data:
            try:
                new_user = {"id": user_id, "email": f"{user_id}@demo.com"}
                res = self.supabase.table('users').insert(new_user).execute()
                return res.data[0]
            except Exception:
                return {"id": user_id, "subscription_status": "free"}
        return res.data[0]

    def mark_free_doc_used(self, user_id: str):
        if not self.supabase: return
        self.supabase.table('users').update({"free_doc_used": True}).eq("id", user_id).execute()

    def save_push_token(self, user_id: str, expo_token: str, platform: str):
        if not self.supabase: return
        self.supabase.table('push_tokens').insert({
            "user_id": user_id, "expo_token": expo_token, "platform": platform
        }).execute()

    def create_session(self, user_id: str, filename: str, token_count: int, price_tier: str, price_usd: int, payment_type: str) -> str:
        s_id = str(uuid.uuid4())
        if not self.supabase: return s_id
        try:
            self.supabase.table('sessions').insert({
                "id": s_id, "user_id": user_id, "document_filename": filename,
                "document_token_count": token_count, "price_tier": price_tier,
                "price_paid_usd": price_usd, "payment_type": payment_type
            }).execute()
        except Exception:
            pass
        return s_id

    def update_payment_status(self, session_id: str, status: str, payment_intent: str = None, subscription_id: str = None):
        if not self.supabase: return
        update_data = {"payment_status": status}
        if payment_intent: update_data["stripe_payment_intent"] = payment_intent
        if subscription_id: update_data["stripe_subscription_id"] = subscription_id
        self.supabase.table('sessions').update(update_data).eq("id", session_id).execute()

    def get_session(self, session_id: str) -> dict:
        if not self.supabase: return {"id": session_id}
        try:
            res = self.supabase.table('sessions').select('*').eq('id', session_id).execute()
            return res.data[0] if res.data else {}
        except Exception:
            return {"id": session_id}

    def create_document(self, session_id: str, document_text: str = '') -> str:
        d_id = str(uuid.uuid4())
        if not self.supabase: return d_id
        try:
            self.supabase.table('documents').insert({
                "id": d_id, "session_id": session_id, "document_text": document_text
            }).execute()
        except Exception:
            pass
        return d_id

    def save_results(self, document_id: str, classification: dict, explanation: dict, form_guide: dict, risk_scan: dict, expungement_guide: dict, escalation: dict, language: str):
        if not self.supabase: return
        try:
            self.supabase.table('documents').update({
                "classification": classification, "explanation": explanation,
                "form_guide": form_guide, "risk_scan": risk_scan,
                "expungement_guide": expungement_guide, "escalation": escalation,
                "language": language, "status": "complete"
            }).eq("id", document_id).execute()
        except Exception:
            pass

    def update_document_status(self, document_id: str, status: str):
        if not self.supabase: return
        self.supabase.table('documents').update({"status": status}).eq("id", document_id).execute()

    def get_document(self, document_id: str) -> dict:
        if not self.supabase: return {"id": document_id, "status": "complete"}
        try:
            res = self.supabase.table('documents').select('*').eq('id', document_id).execute()
            return res.data[0] if res.data else {}
        except Exception:
            return {"id": document_id, "status": "complete"}

    def get_user_documents(self, user_id: str, limit: int = 20) -> list:
        if not self.supabase: return []
        res = self.supabase.table('sessions').select('id, documents(*)').eq('user_id', user_id).limit(limit).execute()
        return res.data

    def save_message(self, document_id: str, role: str, content: str, language: str) -> str:
        m_id = str(uuid.uuid4())
        if not self.supabase: return m_id
        self.supabase.table('chat_messages').insert({
            "id": m_id, "document_id": document_id, "role": role,
            "content": content, "language": language
        }).execute()
        return m_id

    def get_history(self, document_id: str) -> list:
        if not self.supabase: return []
        res = self.supabase.table('chat_messages').select('*').eq('document_id', document_id).order('created_at').execute()
        return res.data

    def log_usage(self, category: str, jurisdiction: str, language: str, price_tier: str, processing_time: float):
        if not self.supabase: return
        self.supabase.table('usage_stats').insert({
            "document_category": category, "jurisdiction": jurisdiction,
            "language": language, "price_tier": price_tier,
            "processing_time_seconds": processing_time
        }).execute()
