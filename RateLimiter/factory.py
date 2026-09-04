from enum import Enum
from strategies.base import RateLimitStrategy
from strategies.fixed_window import FixedWindowStrategy
from strategies.sliding_window import SlidingWindowLogStrategy


class AlgorithmType(Enum):
    FIXED_WINDOW = "fixed_window"
    SLIDING_WINDOW_LOG = "sliding_window_log"


class RateLimitStrategyFactory:
    """Factory for instantiating rate limiting strategies dynamically."""

    _strategies: dict[AlgorithmType, type[RateLimitStrategy]] = {
        AlgorithmType.FIXED_WINDOW: FixedWindowStrategy,
        AlgorithmType.SLIDING_WINDOW_LOG: SlidingWindowLogStrategy,
    }

    @classmethod
    def create_strategy(cls, algo_type: AlgorithmType) -> RateLimitStrategy:
        strategy_cls = cls._strategies.get(algo_type)
        if not strategy_cls:
            raise ValueError(f"Unsupported algorithm type: {algo_type}")
        return strategy_cls()