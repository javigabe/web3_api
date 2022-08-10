from audioop import add


class Token:
    def __init__(self, address, name, price=None):
        self.address = address
        self.name = name
        self.price = price

    def getTokenAddress(self):
        return self.address

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price
    
    def setPrice(self, price):
        self.price = price
