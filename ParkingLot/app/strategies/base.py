from abc import ABC, abstractmethod
from app.models.domain import ParkingSpot, Vehicle

class SpotAllocationStrategy(ABC):
    """Interface for contract"""

    @abstractmethod
    def find_spot(self, spots: list[ParkingSpot], vehicle: Vehicle) -> ParkingSpot | None:
        """Returns optimal spot"""
        pass
        