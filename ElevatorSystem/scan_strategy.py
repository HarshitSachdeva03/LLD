from models import ElevatorCar, Direction, DispatchStrategy

class ScanDispatchStrategy(DispatchStrategy):
    """
    Implements the LOOK algorithm. The elevator services all requests in one 
    direction before reversing.
    """
    
    def determine_next_floor(self, car: ElevatorCar) -> int | None:
        if not car.target_floors:
            return None
            
        if car.direction == Direction.UP:
            # Find closest requested floor above or at current floor
            above_floors = [f for f in car.target_floors if f >= car.current_floor]
            if above_floors:
                return min(above_floors)
            # If no floors above, reverse direction implicitly by returning max below
            return max(car.target_floors)
            
        elif car.direction == Direction.DOWN:
            # Find closest requested floor below or at current floor
            below_floors = [f for f in car.target_floors if f <= car.current_floor]
            if below_floors:
                return max(below_floors)
            # If no floors below, reverse direction implicitly
            return min(car.target_floors)
            
        else:
            # If IDLE, just go to the absolute nearest requested floor
            return min(car.target_floors, key=lambda f: abs(f - car.current_floor))