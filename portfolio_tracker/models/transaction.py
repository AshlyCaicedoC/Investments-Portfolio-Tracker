from datetime import datetime

class Transaction:
    def __init__(self, portfolio, asset, side, quantity, price, datetime):
        self.portfolio = portfolio
        self.asset = asset
        self.side = side
        self.quantity = quantity
        self.price = price 
        self.datetime = datetime.now()