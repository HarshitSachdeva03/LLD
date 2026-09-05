from app.models.domain import Vehicle, ParkingSpot
from app.strategies.base import SpotAllocationStrategy

class ParkingLotManager:
    def __init__(self, spots: list[ParkingSpot], strategy: SpotAllocationStrategy):
        self.spots = spots
        self.strategy = strategy

    def park_vehicle(self, vehicle: Vehicle) -> ParkingSpot | None:
        max_retries = 3
        for _ in range(max_retries):
            candidate_spot = self.strategy.find_spot(self.spots, vehicle)
            if not candidate_spot:
                return None
            if candidate_spot.park(vehicle):
                return candidate_spot
        return None

    def unpark_vehicle(self, spot_id:str)->Vehicle|None:
        for spot in self.spots:
            if spot.spot_id == spot_id:
                return spot.unpark()
        return None