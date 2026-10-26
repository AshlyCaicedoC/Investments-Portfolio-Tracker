# the only thinh thata is needed to turn a regular class into an exception classis to inherit the exception class
# exception is a class that exits python
from portfolio_tracker.errors.base_error import PortfolioTrackerError


class DuplicateAssetError(Exception):
    def __init__(self, message):
        super(). __init__(message)

class AssetNotFound(Exception):
    def __init__(self, message):
        super(). __init__(message)

class InvalidPriceError(PortfolioTrackerError):
    def __init__(self, message):
        super().__init__(message)