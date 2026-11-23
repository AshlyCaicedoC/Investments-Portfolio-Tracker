from decimal import Decimal

from sqlalchemy import select

from portfolio_tracker.models.cash import CashAccount


def get_cash_account(session):
    # the app has one shared cash account; the first time the app runs the table is empty,
    # so we create the account with a zero balance
    account = session.scalar(select(CashAccount))

    if account is None:
        account = CashAccount(balance=Decimal("0.00"))
        session.add(account)
        # flush sends the INSERT now (inside the same transaction) so the row exists,
        # but it is only made permanent when the business operation commits
        session.flush()

    return account
    