from collections import defaultdict
import time
from models import RateLimitRule
from strategies.base import RateLimitStrategy


class FixedWindowStrategy(RateLimitStrategy):
    """
    Fixed Window Counter: Tracks request counts in discrete, non-overlapping time blocks.
    Window ID formula = current_timestamp // time_window_seconds.
    """

    def __init__(self):
        # Key: (client_id, window_id) -> Value: request_count
        self._windows: dict[tuple[str, int], int] = defaultdict(int)

    def allow_request(self, client_id: str, rule: RateLimitRule) -> bool:
        current_time = int(time.time())
        window_id = current_time // rule.time_window_seconds
        key = (client_id, window_id)

        if self._windows[key] < rule.max_requests:
            self._windows[key] += 1
            return True
        return False