from dataclasses import dataclass
from threading import Lock
from app.models.enums import VehicleType, SpotSize, SpotStatus

@dataclass
class Vehicle:
    license_plate: str
    vehicle_type: VehicleType

class ParkingSpot:
    def __init__(self, spot_id:str, floor_number:int, spot_size:SpotSize):
        self.spot_id = spot_id
        self.floor_number = floor_number
        self.spot_size = spot_size
        self.status: SpotStatus = SpotStatus.AVAILABLE
        self.parked_vehicle: Vehicle | None = None
        self._lock = Lock() #spot-level lock

    def can_fit_vehicle(self, vehicle: Vehicle) -> bool:
        match self.spot_size:
            case SpotSize.SMALL:
                return vehicle.vehicle_type == VehicleType.MOTORCYCLE
            case SpotSize.COMPACT:
                return vehicle.vehicle_type in (VehicleType.MOTORCYCLE, VehicleType.CAR)
            case SpotSize.LARGE:
                return True
        return False

    def park(self, vehicle: Vehicle) -> bool:
        """Thread-safe state transition: Available->Occupied"""
        with self._lock:
            if self.status != SpotStatus.AVAILABLE or not self.can_fit_vehicle(vehicle):
                return False
            self.parked_vehicle = vehicle
            self.status = SpotStatus.OCCUPIED
            return True

    def unpark(self) -> Vehicle | None:
        with self._lock:
            if self.status != SpotStatus.OCCUPIED or self.parked_vehicle is None:
                return None
            vehicle = self.parked_vehicle
            self.parked_vehicle = None
            self.status = SpotStatus.AVAILABLE
            return vehicle