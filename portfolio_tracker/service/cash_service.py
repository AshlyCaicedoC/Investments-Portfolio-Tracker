from portfolio_tracker.models.cash import CashAccount
from portfolio_tracker.errors.cash_errors import InvalidDepositError

cash_account = CashAccount()


def deposit_cash(amount):
    if amount <= 0:
        raise InvalidDepositError("Deposit amount must be greater than zero.")

    cash_account.update_balance(amount)


def get_cash_balance():
    return cash_account.balance
