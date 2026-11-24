from sqlalchemy import select
from sqlalchemy.orm import joinedload

from portfolio_tracker.models.transaction import Transaction


def save_transaction(session, transaction):
    session.add(transaction)


def list_transactions(session):
    # joinedload brings each transaction's portfolio and asset in the same query,
    # so the CLI can still read transaction.portfolio.name after the session closes
    return session.scalars(
        select(Transaction)
        .options(joinedload(Transaction.portfolio), joinedload(Transaction.asset))
        .order_by(Transaction.trade_date, Transaction.id)
    ).all()


def list_transactions_for_portfolio(session, portfolio):
    # in the order they happened, so the service can replay them to calculate positions
    return session.scalars(
        select(Transaction)
        .options(joinedload(Transaction.asset))
        .where(Transaction.portfolio_id == portfolio.id)
        .order_by(Transaction.trade_date, Transaction.id)
    ).all()
