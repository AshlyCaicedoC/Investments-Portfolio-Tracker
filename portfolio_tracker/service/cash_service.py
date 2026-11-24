import logging
from decimal import Decimal

from portfolio_tracker.database import transaction
from portfolio_tracker.storage import cash_storage
from portfolio_tracker.errors.cash_errors import InvalidDepositError

logger = logging.getLogger(__name__)


def deposit_cash(amount):
    amount = Decimal(str(amount))

    if amount <= 0:
        raise InvalidDepositError("Deposit amount must be greater than zero.")

    with transaction() as session:
        account = cash_storage.get_cash_account(session)
        # no save call needed: the session sees the change and writes the UPDATE on commit
        account.balance = account.balance + amount
        new_balance = account.balance

    logger.info("Deposited %s, new balance %s", amount, new_balance)
    return new_balance


def get_cash_balance():
    with transaction() as session:
        account = cash_storage.get_cash_account(session)
        return account.balance
