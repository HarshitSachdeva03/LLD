from collections import defaultdict, deque
import time
from models import RateLimitRule
from strategies.base import RateLimitStrategy


class SlidingWindowLogStrategy(RateLimitStrategy):
    """
    Sliding Window Log: Maintains timestamps of executed requests per client
    to enforce smooth rate limits across moving continuous time frames.
    """

    def __init__(self):
        # Key: client_id -> Value: double-ended queue of request timestamps
        self._client_logs: dict[str, deque] = defaultdict(deque)

    def allow_request(self, client_id: str, rule: RateLimitRule) -> bool:
        now = time.time()
        window_start = now - rule.time_window_seconds
        logs = self._client_logs[client_id]

        # Evict outdated request timestamps outside the active window
        while logs and logs[0] <= window_start:
            logs.popleft()

        if len(logs) < rule.max_requests:
            logs.append(now)
            return True
        return False