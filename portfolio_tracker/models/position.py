from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from portfolio_tracker.database import Base

class Position:
    def __init__(self, ticker, quantity, average_cost):
        self.ticker = ticker
        self.quantity = quantity
        self.average_cost = average_cost