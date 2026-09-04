import time
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class CacheEntry:
    """Represents a single entry in the key-value store."""
    value: Any
    expires_at: Optional[float]

    def is_expired(self) -> bool:
        """Checks if the current time has passed the expiration timestamp."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at