import time
from threading import Lock
from typing import Any, Optional
from models import CacheEntry


class ThreadSafeKVStore:
    """An in-memory key-value store supporting TTL and concurrent access."""

    def __init__(self):
        self._store: dict[str, CacheEntry] = {}
        self._lock = Lock()

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """Saves a key-value pair with an optional Time-To-Live (TTL)."""
        expires_at = time.time() + ttl_seconds if ttl_seconds else None
        entry = CacheEntry(value, expires_at)

        # The 'with' block acts as a Context Manager to safely release the lock[cite: 2]
        with self._lock:
            self._store[key] = entry

    def get(self, key: str) -> Optional[Any]:
        """Retrieves a value, handling TTL expiration lazily."""
        with self._lock:
            entry = self._store.get(key)
            if not entry:
                return None
            
            # Lazy Eviction: Delete the key only when someone tries to access an expired one
            if entry.is_expired():
                del self._store[key]
                return None
                
            return entry.value