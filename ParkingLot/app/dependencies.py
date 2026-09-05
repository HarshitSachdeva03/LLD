from app.services.manager import ParkingLotManager
from app.strategies.allocation import LowestFloorFirstStrategy
from app.models.domain import ParkingSpot
from app.models.enums import SpotSize

spots = [
    ParkingSpot("A1", 1, SpotSize.COMPACT),
    ParkingSpot("A2", 1, SpotSize.LARGE),
    ParkingSpot("B1", 2, SpotSize.SMALL)
]

# wire strategy into manager
manager = ParkingLotManager(spots, LowestFloorFirstStrategy())

def get_manager()->ParkingLotManager:
    """Dependency provider for fastapi routes"""
    return manager

