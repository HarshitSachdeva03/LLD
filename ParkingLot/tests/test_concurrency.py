import concurrent.futures
from app.models.domain import ParkingSpot, Vehicle
from app.models.enums import SpotSize, VehicleType

def test_spot_lock_prevents_double_parking():
    # 1. Initialize a single spot and a vehicle
    spot = ParkingSpot(spot_id="A1", floor_number=1, spot_size=SpotSize.COMPACT)
    vehicle = Vehicle(license_plate="RACE-001", vehicle_type=VehicleType.CAR)

    def attempt_to_park():
        """Worker function for the thread pool."""
        return spot.park(vehicle)

    results = []
    
    # 2. Simulate concurrent thread execution across multiple worker threads[cite: 1]
    # Using 'with' ensures the executor automatically cleans up and joins the threads[cite: 1]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit 3 identical parking tasks to the thread pool simultaneously[cite: 1]
        futures = [executor.submit(attempt_to_park) for _ in range(3)]
        
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    # 3. Assert our threading.Lock held up under pressure
    assert results.count(True) == 1, "Only one thread should have successfully parked"
    assert results.count(False) == 2, "The other two threads should have been blocked"
    assert spot.parked_vehicle == vehicle