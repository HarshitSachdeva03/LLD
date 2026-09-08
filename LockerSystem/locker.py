from compartment import Compartment, Size
from AccessToken import AccessToken
import random

class Locker:
    def __init__(self, compartments: list[Compartment]):
        self._compartments = compartments
        self.access_token_mapping: dict[str, AccessToken] = {}

    def deposit_package(self, size:Size):
        compartment = self.get_available_compartment(size)
        if not compartment:
            raise Exception(f"No available compartment of size: {size}")
        compartment.open()
        compartment.markOccupied()
        access_token = self.generate_token(compartment)
        self.access_token_mapping[access_token.get_code()] = access_token
        return access_token.get_code()

    def get_available_compartment(self, size:Size):
        for comp in self._compartments:
            if comp.getSize() == size and not comp.isOccupied():
                return comp
        return None
    
    def generate_token(self, compartment):
        code = f"{random.randint(0, 999999):06d}"        
        return AccessToken(code, compartment)
    
    def pickup(self, token):
        if not token:
            raise Exception("Invalid access token code") 
        access_token = self.access_token_mapping.get(token)
        if not access_token:
            raise Exception("Invalid access token code")
        if access_token.isExpired():
            raise Exception("Access token has expired")
        compartment = access_token.get_compartment()
        compartment.open()
        self._clear_deposit(access_token)

    def openExpired(self):
        pass

    def _clear_deposit(self, access_token:AccessToken):
        compartment = access_token.get_compartment()
        compartment.markFree()
        self.access_token_mapping.pop(access_token.get_code(), None)