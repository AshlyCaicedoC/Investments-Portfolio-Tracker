from datetime import datetime
from decimal import Decimal 

class Transaction:
    def __init__(self, portfolio, asset, side, quantity, price):
        self.portfolio = portfolio
        self.asset = asset
        self.side = side
        self.quantity = Decimal(str(quantity))
        self.price = Decimal(str(price))
        self.datetime = datetime.now()

