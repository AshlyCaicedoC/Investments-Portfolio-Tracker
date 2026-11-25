from decimal import Decimal
 
import pytest
 
from portfolio_tracker.service import cash_service, portfolio_service, transaction_service
from portfolio_tracker.errors.transaction_errors import (
    InvalidQuantityError,
    InvalidTransactionPriceError,
    InsufficientFundsError,
    InsufficientSharesError,
)
from portfolio_tracker.errors.asset_errors import AssetNotFound
from portfolio_tracker.errors.portfolio_errors import PortfolioNotFound

def test_buy_is_recorded(funded_portfolio):
    transaction_service.buy("AAPL", Decimal("10"), Decimal("150"))

    trades = transaction_service.list_transactions()
    assert len(trades) == 1
    assert trades[0].side == "buy"
    assert trades[0].asset.ticker == "AAPL"
    assert trades[0].portfolio.name == "Growth"
    assert trades[0].quantity == Decimal("10")
    assert trades[0].price_per_share == Decimal("150")

def test_buy_takes_cost_from_cash(funded_portfolio):
    # 10,000 - (10 x 150) = 8,500
    transaction_service.buy("AAPL", Decimal("10"), Decimal("150"))
    assert cash_service.get_cash_balance() == Decimal("8500")

def test_buy_using_all_cash_is_allowed(funded_portfolio):
    # 100 x 100 = 10,000, exactly the balance
    transaction_service.buy("AAPL", Decimal("100"), Decimal("100"))
    assert cash_service.get_cash_balance() == Decimal("0")


def test_buy_costing_more_than_cash_is_refused(funded_portfolio):
    # 100 x 100.01 = 10,001, one dollar over
    with pytest.raises(InsufficientFundsError):
        transaction_service.buy("AAPL", Decimal("100"), Decimal("100.01"))

    assert cash_service.get_cash_balance() == Decimal("10000")
    assert transaction_service.list_transactions() == []


def test_buying_zero_shares_is_refused(funded_portfolio):
    with pytest.raises(InvalidQuantityError):
        transaction_service.buy("AAPL", Decimal("0"), Decimal("100"))

    assert cash_service.get_cash_balance() == Decimal("10000")
    assert transaction_service.list_transactions() == []


def test_buying_at_price_zero_is_refused(funded_portfolio):
    with pytest.raises(InvalidTransactionPriceError):
        transaction_service.buy("AAPL", Decimal("10"), Decimal("0"))

    assert cash_service.get_cash_balance() == Decimal("10000")
    assert transaction_service.list_transactions() == []


def test_buying_with_no_portfolio_selected_is_refused(funded_portfolio, monkeypatch):
    monkeypatch.setattr(portfolio_service, "selected_portfolio_id", None)

    with pytest.raises(PortfolioNotFound):
        transaction_service.buy("AAPL", Decimal("1"), Decimal("100"))

    assert cash_service.get_cash_balance() == Decimal("10000")
    assert transaction_service.list_transactions() == []


# selling

def test_sell_adds_sale_amount_to_cash(funded_portfolio):
    # 10,000 - (10 x 100) + (4 x 150) = 9,600
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))
    transaction_service.sell("AAPL", Decimal("4"), Decimal("150"))
    assert cash_service.get_cash_balance() == Decimal("9600")


def test_sell_returns_gain(funded_portfolio):
    # (150 - 100) x 4 = 200
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))
    gain = transaction_service.sell("AAPL", Decimal("4"), Decimal("150"))
    assert gain == Decimal("200")


def test_sell_gain_uses_average_cost(funded_portfolio):
    # average cost (10 x 100 + 10 x 120) / 20 = 110
    # gain (150 - 110) x 5 = 200
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))
    transaction_service.buy("AAPL", Decimal("10"), Decimal("120"))
    gain = transaction_service.sell("AAPL", Decimal("5"), Decimal("150"))
    assert gain == Decimal("200")


def test_selling_all_shares_is_allowed(funded_portfolio):
    # 10,000 - (10 x 100) + (10 x 100) = 10,000
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))
    transaction_service.sell("AAPL", Decimal("10"), Decimal("100"))
    assert cash_service.get_cash_balance() == Decimal("10000")


def test_selling_more_shares_than_held_is_refused(funded_portfolio):
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))

    with pytest.raises(InsufficientSharesError):
        transaction_service.sell("AAPL", Decimal("10.01"), Decimal("100"))

    # 10,000 - (10 x 100) = 9,000, and only the buy is recorded
    assert cash_service.get_cash_balance() == Decimal("9000")
    assert len(transaction_service.list_transactions()) == 1


def test_selling_asset_not_held_is_refused(funded_portfolio):
    with pytest.raises(InsufficientSharesError):
        transaction_service.sell("AAPL", Decimal("1"), Decimal("100"))

    assert cash_service.get_cash_balance() == Decimal("10000")
    assert transaction_service.list_transactions() == []


def test_selling_zero_shares_is_refused(funded_portfolio):
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))

    with pytest.raises(InvalidQuantityError):
        transaction_service.sell("AAPL", Decimal("0"), Decimal("100"))

    assert cash_service.get_cash_balance() == Decimal("9000")
    assert len(transaction_service.list_transactions()) == 1


def test_selling_at_price_zero_is_allowed(funded_portfolio):
    # 10,000 - (10 x 100) + (5 x 0) = 9,000
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))
    transaction_service.sell("AAPL", Decimal("5"), Decimal("0"))
    assert cash_service.get_cash_balance() == Decimal("9000")
    assert len(transaction_service.list_transactions()) == 2


def test_selling_at_negative_price_is_refused(funded_portfolio):
    transaction_service.buy("AAPL", Decimal("10"), Decimal("100"))

    with pytest.raises(InvalidTransactionPriceError):
        transaction_service.sell("AAPL", Decimal("5"), Decimal("-1"))

    assert cash_service.get_cash_balance() == Decimal("9000")
    assert len(transaction_service.list_transactions()) == 1