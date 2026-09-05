from fastapi import APIRouter, Depends, HTTPException
from app.schemas import ParkVehicleRequest, ParkingResponse
from app.models.domain import Vehicle
from app.services.manager import ParkingLotManager
from app.dependencies import get_manager

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
