class DuplicatePortfolioError(Exception):
    def __init__(self, message):
        super().__init__(message)

class PortfolioNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)

