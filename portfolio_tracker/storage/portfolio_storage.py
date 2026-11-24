from sqlalchemy import select

from portfolio_tracker.models.portfolio import Portfolio
from sqlalchemy import func, select


def find_portfolio_by_name(session, name):
    # compares in lowercase so "Growth" and "growth" find the same portfolio
    # (MySQL already ignores case, but other databases like SQLite do not)
    return session.scalar(
        select(Portfolio).where(func.lower(Portfolio.name) == name.lower())
    )


def find_portfolio_by_id(session, portfolio_id):
    # returns the portfolio, or None if it does not exist
    return session.get(Portfolio, portfolio_id)


def list_portfolios(session):
    return session.scalars(select(Portfolio).order_by(Portfolio.name)).all()


def save_portfolio(session, portfolio):
    session.add(portfolio)


def delete_portfolio(session, portfolio):
    # the relationship's cascade also deletes this portfolio's transactions
    session.delete(portfolio)
