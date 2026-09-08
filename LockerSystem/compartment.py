from enum import Enum
class Size(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class Compartment:
    def __init__(self, size:Size):
        self._size = size
        self._occupied = False
    def getSize(self):
        return self._size
    def isOccupied(self):
        return self._occupied
    def markOccupied(self):
        self._occupied = True
    def markFree(self):
        self._occupied = False
    def open(self):
        print("Compartment opened")