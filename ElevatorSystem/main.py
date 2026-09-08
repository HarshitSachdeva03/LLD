from controller import ElevatorController
from models import ElevatorCar, ElevatorState
from scan_strategy import ScanDispatchStrategy

if __name__ == "__main__":
    # 1. Initialize the core entity 
    car = ElevatorCar(car_id="Elevator-A", current_floor=0)
    
    # 2. Instantiate the specific routing algorithm
    strategy = ScanDispatchStrategy()
    
    # 3. Inject dependencies into the central manager facade
    controller = ElevatorController(car=car, strategy=strategy)
    
    print("--- Initiating Elevator Simulation ---")
    
    # 4. Simulate simultaneous button presses before movement starts
    controller.request_elevator(3)
    controller.request_elevator(7)
    controller.request_elevator(1)
    
    # 5. Run the event loop to process state transitions
    for tick in range(20):
        print(f"\n[Tick {tick}]")
        controller.step()
        
        # Mid-way simulation: A new request comes in while the elevator is moving
        if tick == 3:
            print("\n[System] ** NEW REQUEST: Floor 1 **")
            controller.request_elevator(1)
            
        # Exit condition
        if car.state == ElevatorState.IDLE and not car.target_floors:
            print("\n[System] All requests serviced. Returning to standby.")
            break