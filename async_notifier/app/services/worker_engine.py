import asyncio
import logging
from app.domain.models import NotificationRequest
from app.services.dispatcher import NotificationDispatcher

logger = logging.getLogger(__name__)

class NotificationWorkerEngine:
    """
    Manages an in-memory asyncio.Queue and a pool of non-blocking worker coroutines.
    """
    def __init__(
        self, 
        dispatcher: NotificationDispatcher, 
        queue_size: int = 100, 
        num_workers: int = 3
    ):
        self._dispatcher = dispatcher
        self._queue: asyncio.Queue[NotificationRequest] = asyncio.Queue(maxsize=queue_size)
        self._num_workers = num_workers
        self._workers: list[asyncio.Task] = []
        self._is_running = False

    async def enqueue(self, request: NotificationRequest) -> bool:
        """
        Producer method: Pushes a request into the queue without blocking.
        Handles backpressure via queue maxsize.
        """
        try:
            self._queue.put_nowait(request)
            return True
        except asyncio.QueueFull:
            logger.error(f"Notification queue is full! Rejected request {request.id}")
            return False

    async def start(self) -> None:
        """Spawns background worker coroutines onto the event loop."""
        self._is_running = True
        for i in range(self._num_workers):
            # Schedules worker coroutine concurrently in background
            task = asyncio.create_task(self._worker_loop(worker_id=i))
            self._workers.append(task)
        logger.info(f"Started {self._num_workers} background notification workers.")

    async def _worker_loop(self, worker_id: int) -> None:
        """Consumer loop: Polling queue and delegating to dispatcher."""
        while self._is_running:
            try:
                # Non-blocking timeout allows checking self._is_running flag
                request = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                
                logger.info(f"[Worker-{worker_id}] Picked up request {request.id}")
                await self._dispatcher.dispatch(request)
                
                # Signal to queue that task processing is complete
                self._queue.task_done()
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[Worker-{worker_id}] Error processing request: {e}")

    async def stop(self) -> None:
        """Gracefully shuts down worker tasks after draining queue."""
        self._is_running = False
        # Block until all items in queue are processed (task_done called)
        await self._queue.join()
        
        # Cancel running worker tasks
        for worker in self._workers:
            worker.cancel()
        
        # Safely await all cancellations
        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()
        logger.info("Notification worker engine shut down cleanly.")