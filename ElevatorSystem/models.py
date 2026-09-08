from enum import Enum
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

class Direction(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE"

class ElevatorState(str, Enum):
    IDLE = "IDLE"
    MOVING = "MOVING"
    MAINTENANCE = "MAINTENANCE"

@dataclass
class ElevatorCar:
    """Represents the physical elevator cabin and its internal state."""
    car_id: str
    current_floor: int = 0
    direction: Direction = Direction.IDLE
    state: ElevatorState = ElevatorState.IDLE
    
    # We use a set for O(1) lookups to track which floors are requested
    target_floors: set[int] = field(default_factory=set)

    def add_stop(self, floor: int) -> None:
        """Registers a floor request inside the car."""
        self.target_floors.add(floor)
        
    def complete_stop(self, floor: int) -> None:
        """Removes a floor from the queue once serviced."""
        self.target_floors.discard(floor)

class DispatchStrategy(ABC):
    """Interface enforcing the contract for elevator routing algorithms."""

    @abstractmethod
    def determine_next_floor(self, car: ElevatorCar) -> int | None:
        """
        Evaluates the car's current state and pending target floors, 
        returning the next floor it should move to.
        """
        pass