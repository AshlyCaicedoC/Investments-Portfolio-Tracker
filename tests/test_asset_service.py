import pytest

from portfolio_tracker.service import asset_service
from portfolio_tracker.errors.asset_errors import DuplicateAssetError, AssetNotFound


def test_added_asset_can_be_found():
    asset_service.add_asset("AAPL", "Apple Inc.")
    asset = asset_service.find_asset("AAPL")
    assert asset.issuer == "Apple Inc."


def test_ticker_is_saved_in_uppercase():
    asset_service.add_asset("aapl", "Apple Inc.")
    assert asset_service.find_asset("AAPL").ticker == "AAPL"


def test_find_ignores_ticker_case():
    asset_service.add_asset("AAPL", "Apple Inc.")
    assert asset_service.find_asset("aapl").ticker == "AAPL"


def test_duplicate_ticker_is_refused():
    asset_service.add_asset("AAPL", "Apple Inc.")

    with pytest.raises(DuplicateAssetError):
        asset_service.add_asset("AAPL", "Another name")

    assets = asset_service.list_assets()
    assert len(assets) == 1
    assert assets[0].issuer == "Apple Inc."


def test_duplicate_ticker_in_lowercase_is_refused():
    asset_service.add_asset("AAPL", "Apple Inc.")

    with pytest.raises(DuplicateAssetError):
        asset_service.add_asset("aapl", "Apple Inc.")

    assert len(asset_service.list_assets()) == 1


def test_unknown_ticker_is_not_found():
    with pytest.raises(AssetNotFound):
        asset_service.find_asset("MSFT")


def test_assets_are_listed_by_ticker():
    asset_service.add_asset("MSFT", "Microsoft")
    asset_service.add_asset("AAPL", "Apple Inc.")
    tickers = [asset.ticker for asset in asset_service.list_assets()]
    assert tickers == ["AAPL", "MSFT"]