from . import Token

class LpInfo:
    def __init__(self, address: str, token0: Token, token1: Token, price: int = None):
        self.address = address
        self.token0 = token0
        self.token1 = token1
        self.price = price

    def get_address(self):
        return self.address
    
    def get_token0(self):
        return self.token0

    def get_token1(self):
        return self.token1

    def get_price(self):
        return self.price

    def set_price(self, price):
        self.price = price