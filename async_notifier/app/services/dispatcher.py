# app/services/dispatcher.py
import asyncio
import logging
from app.domain.enums import ChannelType, NotificationStatus
from app.domain.models import NotificationRequest
from app.providers.base import BaseNotificationProvider

logger = logging.getLogger(__name__)

class NotificationDispatcher:
    def __init__(self, providers: dict[ChannelType, BaseNotificationProvider]):
        self._providers = providers
        self._processed_ids: set[str] = set()
        self._lock = asyncio.Lock()

    async def dispatch(self, request: NotificationRequest) -> dict[ChannelType, bool]:
        # 1. Idempotency Check (Guarded by asyncio.Lock)
        async with self._lock:
            if request.id in self._processed_ids:
                logger.warning(f"Duplicate notification attempt blocked: {request.id}")
                return {}
            self._processed_ids.add(request.id)

        # 2. Build list of async coroutines for each requested channel
        tasks = []
        target_channels = []

        for channel in request.channels:
            provider = self._providers.get(channel)
            if provider:
                tasks.append(provider.execute(request))
                target_channels.append(channel)
            else:
                logger.error(f"No provider registered for channel: {channel}")

        if not tasks:
            request.status = NotificationStatus.FAILED
            return {}

        # 3. Parallel Execution across channels
        # return_exceptions=True ensures one failing channel doesn't cancel others
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 4. Process channel results
        channel_results: dict[ChannelType, bool] = {}
        all_succeeded = True

        for channel, result in zip(target_channels, results):
            if isinstance(result, Exception):
                logger.error(f"Channel {channel} failed with error: {result}")
                channel_results[channel] = False
                all_succeeded = False
            else:
                channel_results[channel] = bool(result)
                if not result:
                    all_succeeded = False

        request.status = NotificationStatus.SUCCESS if all_succeeded else NotificationStatus.FAILED
        return channel_results