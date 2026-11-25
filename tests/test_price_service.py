from decimal import Decimal

import pytest

from portfolio_tracker.service import asset_service, price_service
from portfolio_tracker.errors.asset_errors import AssetNotFound, InvalidPriceError


def test_price_can_be_set_and_read():
    asset_service.add_asset("AAPL", "Apple Inc.")
    price_service.set_price("AAPL", Decimal("190.25"))
    assert price_service.get_price("AAPL") == Decimal("190.25")

def test_new_price_replaces_the_old_one():
    asset_service.add_asset("AAPL", "Apple Inc.")
    price_service.set_price("AAPL", Decimal("190"))
    price_service.set_price("AAPL", Decimal("200"))
    assert price_service.get_price("AAPL") == Decimal("200")

def test_asset_with_no_price_returns_none():
    asset_service.add_asset("AAPL", "Apple Inc.")
    assert price_service.get_price("AAPL") is None

def test_negative_price_is_refused():
    asset_service.add_asset("AAPL", "Apple Inc.")
    price_service.set_price("AAPL", Decimal("190"))

    with pytest.raises(InvalidPriceError):
        price_service.set_price("AAPL", Decimal("-1"))

    assert price_service.get_price("AAPL") == Decimal("190")