from portfolio_tracker.errors.base_error import PortfolioTrackerError


class NegativeCashBalanceError(PortfolioTrackerError):
    pass

class InvalidDepositError(PortfolioTrackerError):
    pass
    