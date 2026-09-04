import heapq
from threading import Lock
from typing import Optional
from app.models.job import Job

class PriorityJobQueue:
    def __init__(self):
        self._queue: list[Job] = []
        self._lock = Lock()

    def push(self, job:Job)->None:
        with self._lock:
            heapq.heappush(self._queue, job)

    def pop(self) -> Optional[Job]:
        """Safely pops the highest priority job"""
        with self._lock:
            if not self._queue:
                return None
            return heapq.heappop(self._queue)

    def __len__(self) -> int:
        with self._lock:
            return len(self._queue)