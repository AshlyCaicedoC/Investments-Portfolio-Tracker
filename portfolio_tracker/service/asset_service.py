# this is a service module so it implements logic related to the asset class/domain
from portfolio_tracker.models.asset import Asset
from portfolio_tracker.errors.asset_errors import DuplicateAssetError, AssetNotFound
from portfolio_tracker.database import transaction
from portfolio_tracker.storage import asset_storage
import logging 

logger = logging.getLogger(__name__)


def add_asset(ticker, issuer):
    ticker = ticker.strip().upper() # we added this line to normalize the ticker and make sure if the ticker is written in lower or uppercase, it should be treated as the same 
    issuer = issuer. strip()
    
    with transaction() as session:
        existing=  asset_storage.find_asset_by_ticker(session, ticker)

        if existing is not None:
            raise DuplicateAssetError(f"Asset '{ticker}' already exists")

        asset = Asset(ticker=ticker, issuer=issuer)
        asset_storage.save_asset(session, asset)

    logger.info("Added asset %s", ticker)
    return asset
    

def find_asset(ticker):
    ticker = ticker.strip().upper()
    with transaction() as session:
        asset =  asset_storage.find_asset_by_ticker(session, ticker)

    if asset is None:
        raise AssetNotFound(f"No ticker '{ticker}' exists")

    return asset

def list_assets():
    with transaction() as session:
        assets = asset_storage.list_assets(session)

    return assets