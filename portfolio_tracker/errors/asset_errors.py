# the only thinh thata is needed to turn a regular class into an exception classis to inherit the exception class
# exception is a class that exits python
from portfolio_tracker.errors.base_error import PortfolioTrackerError


class DuplicateAssetError(PortfolioTrackerError):
    pass

class AssetNotFound(PortfolioTrackerError):
    pass

class InvalidPriceError(PortfolioTrackerError):
    pass