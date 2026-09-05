from fastapi import APIRouter, Depends, HTTPException
from app.schemas import ParkVehicleRequest, ParkingResponse, ParkingSpotResponse
from app.models.domain import Vehicle
from app.services.manager import ParkingLotManager
from app.dependencies import get_manager
from app.models.enums import SpotStatus, VehicleType, SpotSize

router = APIRouter()

@router.post("/park", response_model=ParkingResponse)
def park_vehicle(request: ParkVehicleRequest, manager: ParkingLotManager = Depends(get_manager)):
    vehicle = Vehicle(license_plate=request.license_plate, vehicle_type=request.vehicle_type)

    spot = manager.park_vehicle(vehicle)

    if not spot:
        raise HTTPException(status_code=400, detail="Lot is full for this vehicle type.")

    return ParkingResponse(message="Parked successfully", spot_id=spot.spot_id)

@router.post("/unpark/{spot_id}", response_model=ParkingResponse)
def unpark_vehicle(spot_id:str, manager: ParkingLotManager = Depends(get_manager)):
    vehicle = manager.unpark_vehicle(spot_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Spot is empty or not found")
    return ParkingResponse(message=f"Vehicle {vehicle.license_plate} unparked", spot_id=spot_id)

@router.get("/spots", response_model=list[ParkingSpotResponse])
def get_spots(
    spot_id: str|None = None,
    floor_num: int|None = None,
    spot_status: SpotStatus|None = None,
    spot_size: SpotSize|None = None,
    vehicle_type: VehicleType|None = None,
    manager: ParkingLotManager = Depends(get_manager)
):
    return manager.get_spots(spot_id, floor_num, spot_status, spot_size, vehicle_type)
    
