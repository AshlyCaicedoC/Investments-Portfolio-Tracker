class Portfolio:
    def __init__(self, name, description):
        # the .strip().upper() is to gurantee that no matter if the customer
        # writes the name in lower or uppercase, it will point to the same portfolio 
        self.name = name
        self.description = description
        # will help identify what specific position are we holding in specific portfolio
        #per each asset hled within it
        self.positions= {}
        self.realized_gain = Decimal("0")
