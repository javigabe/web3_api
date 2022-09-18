from typing import Dict
from .Token import Token

class LpInfo:
    def __init__(self, address: str, token0: Token, token1: Token, percentage_token0: float = None, percentage_token1: float = None, price: int = None):
        self.address = address
        self.token0 = token0
        self.token1 = token1
        self.price = price
        self.percentage_token0 = percentage_token0
        self.percentage_token1 = percentage_token1

    def getAddress(self) -> str:
        return self.address
    
    def getToken0(self) -> Token:
        return self.token0

    def getToken1(self) -> Token:
        return self.token1

    def getPrice(self) -> float:
        return self.price

    def getPercentageToken0(self) -> float:
        return self.percentage_token0

    def getPercentageToken1(self) -> float:
        return self.percentage_token1

    def setPrice(self, price):
        self.price = price
    
    def setPercentageToken0(self, amount: int):
        self.percentage_token0 = amount
    
    def setPercetangeToken1(self, amount: int):
        self.percentage_token1 = amount

    def toJson(self, lp_tokens) -> Dict:
        return {
            'token0': {
                'amount': (self.getPercentageToken0() * lp_tokens * self.getPrice()) / self.getToken0().getPrice(),
                'price': self.getToken0().getPrice(),
                'symbol': self.getToken0().getName(),
                'address': self.getToken0().getTokenAddress()
            },
            'token1': {
                'amount': (self.getPercentageToken1() * lp_tokens * self.getPrice()) / self.getToken1().getPrice(),
                'price': self.getToken1().getPrice(),
                'symbol': self.getToken1().getName(),
                'address': self.getToken1().getTokenAddress()
            }
        }