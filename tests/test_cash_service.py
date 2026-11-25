from decimal import Decimal

import pytest

from portfolio_tracker.service import cash_service
from portfolio_tracker.errors.cash_errors import InvalidDepositError


def test_balance_starts_at_zero():
    assert cash_service.get_cash_balance() == Decimal("0")


def test_deposit_adds_to_balance():
    # 0 + 250 = 250
    cash_service.deposit_cash(Decimal("250"))
    assert cash_service.get_cash_balance() == Decimal("250")


def test_deposits_add_up():
    # 100 + 50.25 = 150.25
    cash_service.deposit_cash(Decimal("100"))
    cash_service.deposit_cash(Decimal("50.25"))
    assert cash_service.get_cash_balance() == Decimal("150.25")


def test_deposit_of_zero_is_refused():
    cash_service.deposit_cash(Decimal("100"))

    with pytest.raises(InvalidDepositError):
        cash_service.deposit_cash(Decimal("0"))

    assert cash_service.get_cash_balance() == Decimal("100")


def test_negative_deposit_is_refused():
    cash_service.deposit_cash(Decimal("100"))

    with pytest.raises(InvalidDepositError):
        cash_service.deposit_cash(Decimal("-50"))

    assert cash_service.get_cash_balance() == Decimal("100")