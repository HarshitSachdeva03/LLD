from abc import ABC, abstractmethod
import asyncio
import logging
from app.domain.models import NotificationRequest

logger = logging.getLogger(__name__)

class BaseNotificationProvider(ABC):
    def __init__(self, max_concurrency: int = 5):
        self._semaphore = asyncio.Semaphore(max_concurrency)

    @abstractmethod
    async def send(self, request: NotificationRequest) -> bool:
        pass

    async def execute(self, request:NotificationRequest) -> bool:
        async with self._semaphore:
            try:
                return await self.send(request)
            except Exception as e:
                logger.error(f"[{self.__class__.__name__}] Execution failed: {e}")
                return False       