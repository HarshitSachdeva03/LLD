from models import ElevatorCar, Direction, ElevatorState, DispatchStrategy

class ElevatorController:
    """
    Central Manager Facade.
    Coordinates client request evaluation and strategy assignment.
    """
    
    def __init__(self, car: ElevatorCar, strategy: DispatchStrategy):
        self.car = car
        # Dependency Injection: The manager doesn't care WHICH algorithm it uses
        self.strategy = strategy
        
    def request_elevator(self, floor: int) -> None:
        """Registers a button press from a hallway or inside the car."""
        self.car.add_stop(floor)
        print(f"[System] Button pressed for floor {floor}")
        
    def step(self) -> None:
        """
        Simulates one time-step of the elevator's movement. 
        In a real system, a background worker or chron job would call this repeatedly.
        """
        next_floor = self.strategy.determine_next_floor(self.car)
        
        # 1. Handle Empty Queue
        if next_floor is None:
            if self.car.state != ElevatorState.IDLE:
                print("[Elevator] Queue empty. Transitioning to IDLE.")
            self.car.direction = Direction.IDLE
            self.car.state = ElevatorState.IDLE
            return
            
        # 2. Handle Arrival
        if self.car.current_floor == next_floor:
            print(f"[Elevator] Arrived at floor {self.car.current_floor}. Doors opening.")
            self.car.complete_stop(self.car.current_floor)
            # We keep the current direction so the SCAN algorithm continues moving forward
            return
            
        # 3. Handle Movement
        self.car.state = ElevatorState.MOVING
        if next_floor > self.car.current_floor:
            self.car.direction = Direction.UP
            self.car.current_floor += 1
        elif next_floor < self.car.current_floor:
            self.car.direction = Direction.DOWN
            self.car.current_floor -= 1
            
        print(f"[Elevator] Moving {self.car.direction.value}... currently passing floor {self.car.current_floor}")