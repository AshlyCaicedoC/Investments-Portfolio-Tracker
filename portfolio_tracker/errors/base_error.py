# this base error will allow my cli file to catch any of my custom errors in one line 

class PortfolioTrackerError(Exception):
    def __init__(self, message):
        super(). __init__(message)
