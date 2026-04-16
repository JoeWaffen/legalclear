import logging

class NotificationService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def send_push(self, user_id: str, title: str, message: str):
        self.logger.info(f"Push Notification sent to {user_id}: {title} - {message}")
        return True
