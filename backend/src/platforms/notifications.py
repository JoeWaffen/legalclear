import httpx
from src.core.config import settings

class NotificationService:
    def __init__(self):
        pass

    async def send(self, user_id: str, title: str, message: str, data: dict = None) -> dict:
        print(f"[NOTIFICATION LOG] To: {user_id} | {title} | {message}")
        platform = settings.MESSAGING_PLATFORM
        
        # MESSAGING SLOT
        # if platform == 'whatsapp': return await self.send_whatsapp(...)
        
        return {
            "sent": True,
            "method": "log",
            "message": message
        }

    async def send_push(self, expo_token: str, title: str, body: str, data: dict = None) -> dict:
        url = "https://exp.host/--/api/v2/push/send"
        payload = {
            "to": expo_token,
            "title": title,
            "body": body,
            "data": data or {}
        }
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=payload)
                return {"sent": resp.status_code == 200, "ticket": resp.json()}
        except Exception as e:
            return {"sent": False, "error": str(e)}

    async def notify_document_ready(self, user_id: str, document_id: str, lang: str = 'en') -> dict:
        title = "Document Ready" if lang == 'en' else "Documento Listo"
        message = f"Your document analysis is ready." if lang == 'en' else f"El análisis de su documento está listo."
        return await self.send(user_id, title, message, {"document_id": document_id})

    async def notify_payment_confirmed(self, user_id: str, lang: str = 'en') -> dict:
        title = "Payment Confirmed" if lang == 'en' else "Pago Confirmado"
        message = "Thank you! Payment received." if lang == 'en' else "¡Gracias! Pago recibido."
        return await self.send(user_id, title, message)
