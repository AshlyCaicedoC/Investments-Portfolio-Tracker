from decimal import Decimal

from portfolio_tracker.errors.base_error import PortfolioTrackerError


class TradeError(PortfolioTrackerError): # this is a base clase for a buy service rule violation
    

# this is to avoid the placement of a buy order that will exceed the available cash 
class InsufficientFundsError(TradeError):
    
    def __init__(self, required_amount, available_amount):
        self.required_amount = required_amount
        self.available_amount = available_amount
        super().__init__(
            f"Not enough cash: this costs ${required_amount:,.2f} "
            f"but the balance is ${available_amount:,.2f}."
        )

# to avoid selling more shares than the selected portfolio shows 
class InsufficientSharesError(TradeError):
    def __init__(self, ticker: str, requested_quantity: Decimal, held_quantity: Decimal, portfolio_name: str
    ):
        self.ticker = ticker
        self.requested_quantity = requested_quantity
        self.held_quantity = held_quantity
        self.portfolio_name = portfolio_name
        super().__init__(
            f"Cannot sell {requested_quantity:f} shares of {ticker}: "
            f"portfolio '{portfolio_name}' holds only {held_quantity:f}."
        )