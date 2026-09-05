import asyncio
import logging
from app.domain.models import NotificationRequest
from app.providers.base import BaseNotificationProvider

logger = logging.getLogger(__name__)

class SendGridEmailProvider(BaseNotificationProvider):
    async def send(self, request: NotificationRequest) -> bool:
        # Simulate network latency (I/O operation)
        await asyncio.sleep(0.3)
        logger.info(f"[EMAIL -> {request.user_id}] {request.message}")
        return True