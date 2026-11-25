import pytest 
from sqlalchemy import URL, create_engine
from decimal import Decimal

from portfolio_tracker import database
from portfolio_tracker.service import portfolio_service, transaction_service, asset_service
from portfolio_tracker.errors.portfolio_errors import (
    DuplicatePortfolioError,
    PortfolioNotFound,
    PortfolioNotEmptyError,
)

def test_created_portfolio_creates_it():
    portfolio_service.create_portfolio("Tech", "Growth stocks")
    assert portfolio_service.find_portfolio("Tech").description == "Growth stocks"

def test_duplicate_portfolio_name_is_refused_no_matter_the_loweruppercase():
    portfolio_service.create_portfolio("Pasive Income", "dividend stocks")

    with pytest.raises(DuplicatePortfolioError):
        portfolio_service.create_portfolio("PASivE iNcOmE", "Another one")

    portfolios = portfolio_service.view_all_portfolios()
    assert len(portfolios) == 1
    assert portfolios[0].description == "dividend stocks"

def test_unknown_portfolio_is_not_found():
    with pytest.raises(PortfolioNotFound):
        portfolio_service.find_portfolio("Income")


def test_viewing_with_nothing_selected_is_refused():
    portfolio_service.create_portfolio("Growth", "Tech stocks")

    with pytest.raises(PortfolioNotFound):
        portfolio_service.view_selected_portfolio()


# deleting

def test_empty_portfolio_can_be_deleted():
    portfolio_service.create_portfolio("Growth", "Tech stocks")
    portfolio_service.delete_portfolio("Growth")
    assert portfolio_service.view_all_portfolios() == []


def test_deleting_unknown_portfolio_is_refused():
    portfolio_service.create_portfolio("Growth", "Tech stocks")

    with pytest.raises(PortfolioNotFound):
        portfolio_service.delete_portfolio("Income")

    assert len(portfolio_service.view_all_portfolios()) == 1


def test_portfolio_with_trades_cannot_be_deleted(funded_portfolio):
    transaction_service.buy("AAPL", Decimal("1"), Decimal("100"))

    with pytest.raises(PortfolioNotEmptyError):
        portfolio_service.delete_portfolio("Growth")

    assert portfolio_service.find_portfolio("Growth").name == "Growth"
    assert len(transaction_service.list_transactions()) == 1


def test_new_portfolio_is_not_selected_after_deleting_the_selected_one():
    portfolio_service.create_portfolio("Growth", "Tech stocks")
    portfolio_service.select_portfolio("Growth")
    portfolio_service.delete_portfolio("Growth")
    portfolio_service.create_portfolio("Income", "Dividends")

    with pytest.raises(PortfolioNotFound):
        portfolio_service.view_selected_portfolio()


# summary calculations

def test_average_cost_blends_purchase_prices(funded_portfolio, set_prices):
    # (10 x 100 + 10 x 120) / 20 = 110
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))
    transaction_service.buy("AAPL", Decimal("10"), Decimal("120"))
    set_prices({"AAPL": Decimal("130")})

    summary = portfolio_service.get_portfolio_summary()
    assert summary["rows"][0]["average_cost"] == Decimal("110")


def test_selling_does_not_change_average_cost(funded_portfolio, set_prices):
    # average stays (10 x 100 + 10 x 120) / 20 = 110 after selling 5
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))
    transaction_service.buy("AAPL", Decimal("10"), Decimal("120"))
    transaction_service.sell("AAPL", Decimal("5"), Decimal("150"))
    set_prices({"AAPL": Decimal("130")})

    summary = portfolio_service.get_portfolio_summary()
    assert summary["rows"][0]["average_cost"] == Decimal("110")


def test_market_value_is_quantity_times_current_price(funded_portfolio, set_prices):
    # 10 x 130 = 1,300
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))
    set_prices({"AAPL": Decimal("130")})

    summary = portfolio_service.get_portfolio_summary()
    assert summary["rows"][0]["market_value"] == Decimal("1300")


def test_unrealized_gain_uses_current_price_minus_average_cost(funded_portfolio, set_prices):
    # (130 - 100) x 10 = 300
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))
    set_prices({"AAPL": Decimal("130")})

    summary = portfolio_service.get_portfolio_summary()
    assert summary["rows"][0]["unrealized_gain"] == Decimal("300")


def test_totals_add_up_across_assets(funded_portfolio, set_prices):
    # AAPL: 10 x 130 = 1,300 value, (130 - 100) x 10 = 300 gain
    # MSFT: 5 x 180 = 900 value, (180 - 200) x 5 = -100 gain
    # totals: 1,300 + 900 = 2,200 and 300 - 100 = 200
    asset_service.add_asset("MSFT", "Microsoft")
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))
    transaction_service.buy("MSFT", Decimal("5"), Decimal("200"))
    set_prices({"AAPL": Decimal("130"), "MSFT": Decimal("180")})

    summary = portfolio_service.get_portfolio_summary()
    assert summary["total_market_value"] == Decimal("2200")
    assert summary["total_unrealized_gain"] == Decimal("200")


def test_asset_without_price_is_left_out_of_totals(funded_portfolio, set_prices):
    # only AAPL has a price: 10 x 130 = 1,300 and (130 - 100) x 10 = 300
    asset_service.add_asset("MSFT", "Microsoft")
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))
    transaction_service.buy("MSFT", Decimal("5"), Decimal("200"))
    set_prices({"AAPL": Decimal("130")})

    summary = portfolio_service.get_portfolio_summary()
    assert summary["total_market_value"] == Decimal("1300")
    assert summary["total_unrealized_gain"] == Decimal("300")


def test_realized_gain_adds_up_all_sales(funded_portfolio, set_prices):
    # average cost 100
    # first sale: (130 - 100) x 2 = 60
    # second sale: (90 - 100) x 1 = -10
    # total: 60 - 10 = 50
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))
    transaction_service.sell("AAPL", Decimal("2"), Decimal("130"))
    transaction_service.sell("AAPL", Decimal("1"), Decimal("90"))
    set_prices({"AAPL": Decimal("100")})

    summary = portfolio_service.get_portfolio_summary()
    assert summary["realized_gain"] == Decimal("50")


def test_fully_sold_asset_is_not_a_holding(funded_portfolio, set_prices):
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))
    transaction_service.sell("AAPL", Decimal("10"), Decimal("120"))
    set_prices({"AAPL": Decimal("120")})

    summary = portfolio_service.get_portfolio_summary()
    assert summary["rows"] == []
    # (120 - 100) x 10 = 200 is still counted as realized
    assert summary["realized_gain"] == Decimal("200")


def test_summary_only_shows_the_selected_portfolio(funded_portfolio, set_prices):
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))
    portfolio_service.create_portfolio("Income", "Dividends")
    portfolio_service.select_portfolio("Income")
    set_prices({"AAPL": Decimal("100")})

    summary = portfolio_service.get_portfolio_summary()
    assert summary["rows"] == []


    