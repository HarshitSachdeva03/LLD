from app.models.domain import Vehicle, ParkingSpot
from app.strategies.base import SpotAllocationStrategy
from app.models.enums import SpotSize, SpotStatus, VehicleType

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

    def get_spots(
        self,
        spot_id: str|None = None,
        floor_num: int|None = None,
        spot_status: SpotStatus|None = None,
        spot_size: SpotSize|None = None,
        vehicle_type: VehicleType|None = None
    )->list[ParkingSpot]:
        filtered_spots = []
        for spot in self.spots:
            vehicle_match = True
            if vehicle_type:
                if not spot.parked_vehicle or spot.parked_vehicle.vehicle_type != vehicle_type:
                    vehicle_match = False
            if (
                (not spot_id or spot.spot_id == spot_id) and
                (not floor_num or spot.floor_number == floor_num) and
                (not spot_status or spot.status == spot_status) and
                (not spot_size or spot.spot_size == spot_size) and
                (vehicle_match)
            ):
                filtered_spots.append(spot)
        return filtered_spots
