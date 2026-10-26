# this is a service module so it implements logic related to the asset class/domain

from portfolio_tracker.models.asset import Asset
from portfolio_tracker.errors.asset_errors import DuplicateAssetError, AssetNotFound
assets = {}

def add_asset(ticker, issuer):
    if ticker in assets:
        raise DuplicateAssetError(f"Asset '{ticker}' already exists")
    assets[ticker] = Asset(ticker,issuer)

def find_asset(ticker):
    if ticker in assets:
        return assets[ticker]
    else:
        raise AssetNotFound(f"No ticker '{ticker}' exists")