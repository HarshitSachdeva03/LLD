from app.strategies.base import SpotAllocationStrategy
from app.models.domain import Vehicle, ParkingSpot
from app.models.enums import SpotStatus

class LowestFloorFirstStrategy(SpotAllocationStrategy):
    def find_spot(self, spots:list[ParkingSpot], vehicle:Vehicle)->ParkingSpot | None:
        for spot in spots:
            if spot.status == SpotStatus.AVAILABLE and spot.can_fit_vehicle(vehicle):
                return spot
        return None