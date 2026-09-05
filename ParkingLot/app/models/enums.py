from enum import Enum

class VehicleType(str, Enum):
    MOTORCYCLE = "MOTORCYCLE"
    CAR = "CAR"
    TRUCK = "TRUCK"

class SpotSize(str, Enum):
    SMALL= "SMALL"
    COMPACT = "COMPACT"
    LARGE = "LARGE"

class SpotStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"

