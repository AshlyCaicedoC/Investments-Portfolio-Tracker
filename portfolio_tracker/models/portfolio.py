from decimal import Decimal

class Portfolio:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.positions= {}
        self.realized_gain = Decimal("0")
