from decimal import Decimal
from portfolio_tracker.errors.cash_errors import NegativeCashBalanceError


class CashAccount:
    def __init__(self):
        self.balance = Decimal("0")

    def update_balance(self, amount):
        new_balance = self.balance + Decimal(str(amount))

        if new_balance < 0:
            raise NegativeCashBalanceError("Cash balance cannot be negative.")
        
        self.balance = new_balance