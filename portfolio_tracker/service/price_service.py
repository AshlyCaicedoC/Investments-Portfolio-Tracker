import logging
from decimal import Decimal
from portfolio_tracker.service.asset_service import find_asset
from portfolio_tracker.errors.asset_errors import InvalidPriceError

logger = logging.getLogger(__name__)

prices = {}

def set_price(ticker, price):
    asset = find_asset(ticker)
    price = Decimal(str(price))

    if price < 0:
        raise InvalidPriceError(f"Price must be zero or more, got {price}")

    prices[asset.ticker] = price
    logger.info("Set price of %s to %s", asset.ticker, price)

def get_price(ticker):
    ticker = ticker.strip().upper()
    return prices.get(ticker)