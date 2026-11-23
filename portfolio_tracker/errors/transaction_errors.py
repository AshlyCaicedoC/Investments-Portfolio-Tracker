from portfolio_tracker.errors.base_error import PortfolioTrackerError

class InvalidQuantityError(PortfolioTrackerError):
    pass

class InvalidTransactionPriceError(PortfolioTrackerError):
    pass

class InsufficientFundsError(PortfolioTrackerError):
    pass # this is to avoid the placement of a buy order that will exceed the available cash

class InsufficientSharesError(PortfolioTrackerError):
    pass # to avoid selling more shares than the selected portfolio shows