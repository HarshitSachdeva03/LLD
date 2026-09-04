from dataclasses import dataclass

@dataclass(frozen=True)
class RateLimitRule:
    """Configuration model for rate limits."""
    max_requests: int
    time_window_seconds: int