from threading import Lock
from models import RateLimitRule
from strategies.base import RateLimitStrategy
from factory import RateLimitStrategyFactory, AlgorithmType


class RateLimiter:
    """
    Central Manager Facade.
    Coordinates client request evaluation, strategy assignment, and thread synchronization.
    """

    def __init__(self, rule: RateLimitRule, algo_type: AlgorithmType = AlgorithmType.SLIDING_WINDOW_LOG):
        self._rule = rule
        self._strategy: RateLimitStrategy = RateLimitStrategyFactory.create_strategy(algo_type)
        self._lock = Lock()

    def allow_request(self, client_id: str) -> bool:
        """Thread-safe public entry point to evaluate incoming requests."""
        with self._lock:
            return self._strategy.allow_request(client_id, self._rule)