# storage module: only saves and returns assets. It never decides if something is an error,
# that is the service's job. It never commits, the business operation decides that.
from sqlalchemy import select

from portfolio_tracker.models.asset import Asset


def find_asset_by_ticker(session, ticker):
    # returns the asset, or None if it does not exist
    return session.scalar(select(Asset).where(Asset.ticker == ticker))


def list_assets(session):
    return session.scalars(select(Asset).order_by(Asset.ticker)).all()


def save_asset(session, asset):
    session.add(asset)