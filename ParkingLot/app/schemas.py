from pydantic import BaseModel
from app.models.enums import VehicleType, SpotStatus, SpotSize
from app.models.domain import Vehicle

class ParkVehicleRequest(BaseModel):
    license_plate: str
    vehicle_type: VehicleType

class ParkingResponse(BaseModel):
    message: str
    spot_id: str|None = None

class ParkingSpotResponse(BaseModel):
    spot_id: str
    floor_number: int
    spot_size: SpotSize
    status: SpotStatus
    parked_vehicle: Vehicle|None = None