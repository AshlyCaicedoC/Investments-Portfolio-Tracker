
from decimal import Decimal

from portfolio_tracker.models.transaction import Transaction
from portfolio_tracker.models.position import Position
from portfolio_tracker.service.asset_service import find_asset
from portfolio_tracker.service.portfolio_service import view_selected_portfolio
from portfolio_tracker.service.cash_service import cash_account
from portfolio_tracker.errors.transaction_errors import (
    InvalidQuantityError,
    InvalidTransactionPriceError,
    InsufficientFundsError,
    InsufficientSharesError
)

transactions = []


def add_transaction(portfolio, asset, quantity, side, price):
    transaction = Transaction(portfolio, asset, side, quantity, price)
    transactions.append(transaction)
    return transaction


def buy(ticker, quantity, price):
    portfolio = get_selected_portfolio()
    asset = find_asset(ticker)

    quantity = Decimal(str(quantity))
    price = Decimal(str(price))

    if quantity <= 0:
        raise InvalidQuantityError("Quantity must be greater than zero.")

    if price <= 0:
        raise InvalidTransactionPriceError("Purchase price must be greater than zero.")

    total_cost = quantity * price

    if cash_account.balance < total_cost:
        raise InsufficientCashError("You do not have enough cash to complete this purchase.")

    if asset.ticker in portfolio.positions:
        position = portfolio.positions[asset.ticker]

        new_quantity = position.quantity + quantity

        new_average_cost = (
            (position.quantity * position.average_cost) + (quantity * price)
        ) / new_quantity

        position.quantity = new_quantity
        position.average_cost = new_average_cost

    else:
        position = Position(asset.ticker, quantity, price)
        portfolio.positions[asset.ticker] = position

    cash_account.update_balance(-total_cost)

    add_transaction(portfolio, asset, quantity, "BUY", price)

    return position


def sell(ticker, quantity, price):
    portfolio = get_selected_portfolio()
    asset = find_asset(ticker)

    quantity = Decimal(str(quantity))
    price = Decimal(str(price))

    if quantity <= 0:
        raise InvalidQuantityError("Quantity must be greater than zero.")

    if price < 0:
        raise InvalidTransactionPriceError("Selling price cannot be negative.")

    if asset.ticker not in portfolio.positions:
        raise InsufficientSharesError(f"You do not hold any shares of '{ticker}'.")

    position = portfolio.positions[asset.ticker]

    if quantity > position.quantity:
        raise InsufficientSharesError("You cannot sell more shares than you own.")

    realized_gain = (price - position.average_cost) * quantity

    portfolio.realized_gain += realized_gain

    sale_amount = quantity * price
    cash_account.update_balance(sale_amount)

    position.quantity -= quantity

    if position.quantity == 0:
        del portfolio.positions[asset.ticker]

    add_transaction(portfolio, asset, quantity, "SELL", price)

    return realized_gain
