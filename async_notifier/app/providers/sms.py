from app.providers.base import BaseNotificationProvider
import asyncio
import logging
from app.domain.models import NotificationRequest

logger = logging.getLogger(__name__)

class TwilioSMSProvider(BaseNotificationProvider):
    async def send(self, request: NotificationRequest) -> bool:
        await asyncio.sleep(0.2) #simulate I/O latency
        logger.info(f"[SMS -> {request.user_id}] {request.message}")
        return True