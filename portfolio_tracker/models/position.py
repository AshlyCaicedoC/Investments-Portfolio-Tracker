from decimal import Decimal 

class Position:
    def __init__(self, ticker, quantity, average_cost):
        self.ticker = ticker
        self.quantity = quantity
        self.average_cost = average_cost