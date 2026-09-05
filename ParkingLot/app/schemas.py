from pydantic import BaseModel
from app.models.enums import VehicleType

class ParkVehicleRequest(BaseModel):
    license_plate: str
    vehicle_type: VehicleType

class ParkingResponse(BaseModel):
    message: str
    spot_id: str|None = None