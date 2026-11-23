# this is a service module so it implements logic related to the asset class/domain


from portfolio_tracker.models.asset import Asset
from portfolio_tracker.errors.asset_errors import DuplicateAssetError, AssetNotFound
assets = {}

def add_asset(ticker, name):
    ticker = ticker.strip().upper() # we added this line to normalize the ticker and make sure if the ticker is written in lower or uppercase, it should be treated as the same 
    if ticker in assets:
        raise DuplicateAssetError(f"Asset '{ticker}' already exists")
    assets[ticker] = Asset(ticker,name)

def find_asset(ticker):
    ticker = ticker.strip().upper()
    if ticker in assets:
        return assets[ticker]
    else:
        raise AssetNotFound(f"No ticker '{ticker}' exists")