from abc import ABC, abstractmethod
from models import RateLimitRule


class RateLimitStrategy(ABC):
    """Interface defining the strategy contract for rate limiters."""

    @abstractmethod
    def allow_request(self, client_id: str, rule: RateLimitRule) -> bool:
        """Determines if a request for a client_id is allowed under the given rule."""
        pass