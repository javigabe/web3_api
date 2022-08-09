from . import Token

class LpInfo:
    def __init__(self, address: str, token0: Token, token1: Token, amount_token0 = None, amount_token1 = None, price: int = None):
        self.address = address
        self.token0 = token0
        self.token1 = token1
        self.price = price
        self.amount_token0 = amount_token0
        self.amount_token1 = amount_token1

    def getAddress(self) -> str:
        return self.address
    
    def getToken0(self) -> Token:
        return self.token0

    def getToken1(self) -> Token:
        return self.token1

    def getPrice(self) -> float:
        return self.price

    def getAmountToken0(self) -> float:
        return self.amount_token0

    def getAmountToken1(self) -> float:
        return self.amount_token1

    def setPrice(self, price):
        self.price = price
    
    def setAmountToken0(self, amount: int):
        self.amount_token0 = amount
    
    def setAmountToken1(self, amount: int):
        self.amount_token1 = amount