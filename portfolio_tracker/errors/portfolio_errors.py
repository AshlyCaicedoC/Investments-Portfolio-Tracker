from portfolio_tracker.errors.base_error import PortfolioTrackerError

class DuplicatePortfolioError(PortfolioTrackerError):
    def __init__(self, message):
        super().__init__(message)

class PortfolioNotFound(PortfolioTrackerError):
    def __init__(self, message):
        super().__init__(message)

class PortfolioNotEmptyError(PortfolioTrackerError):
    def __init__(self, message):
        super().__init__(message)
    

