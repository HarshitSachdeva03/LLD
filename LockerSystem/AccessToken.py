from compartment import Compartment
from datetime import datetime
class AccessToken:
    def __init__(self, code, compartment:Compartment):
        self._code = code
        self._compartment = compartment
        self.created_at = datetime.now()
    def isExpired(self):
        delta = datetime.now() - self.created_at
        return delta.days > 7
    def get_code(self):
        return self._code
    def get_compartment(self):
        return self._compartment
