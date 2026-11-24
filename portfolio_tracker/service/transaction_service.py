import logging
from decimal import Decimal
from portfolio_tracker.service.portfolio_service import view_selected_portfolio, calculate_positions
from portfolio_tracker.models.transaction import Transaction

from portfolio_tracker.service.asset_service import find_asset
from portfolio_tracker.database import transaction
from portfolio_tracker.storage import cash_storage, transaction_storage
from portfolio_tracker.errors.transaction_errors import (
    InvalidQuantityError,
    InvalidTransactionPriceError,
    InsufficientFundsError,
    InsufficientSharesError
)

logger = logging.getLogger(__name__)



def add_transaction(portfolio, asset, side, quantity, price_per_share):
    trade = Transaction(portfolio_id=portfolio.id, asset_id=asset.id, side=side,
                         quantity=quantity, price_per_share=price_share_share)
    
    with transaction() as session:
       transaction_storage.save_transaction(session, trade)

    return trade

def list_transactions():
    with transaction() as session:
        return transaction_storage.list_transactions(session)

def buy(ticker, quantity, price):
    portfolio = view_selected_portfolio()
    asset = find_asset(ticker)

    quantity = Decimal(str(quantity))
    price = Decimal(str(price))

    if quantity <= 0:
        raise InvalidQuantityError("Quantity must be greater than zero.")

    if price <= 0:
        raise InvalidTransactionPriceError("Purchase price must be greater than zero.")

    total_cost = quantity * price

    with transaction() as session:
        account = cash_storage.get_cash_account(session)

        if account.balance < total_cost:
            raise InsufficientFundsError("You do not have enough cash to complete this purchase.")

        account.balance = account.balance - total_cost
        trade = add_transaction(session, portfolio, asset, "buy", quantity, price)

    logger.info("Bought %s %s at %s in '%s'", quantity, asset.ticker, price, portfolio.name)
    return trade


def sell(ticker, quantity, price):
    portfolio = view_selected_portfolio()
    asset = find_asset(ticker)

    quantity = Decimal(str(quantity))
    price = Decimal(str(price))

    if quantity <= 0:
        raise InvalidQuantityError("Quantity must be greater than zero.")

    if price < 0:
        raise InvalidTransactionPriceError("Selling price cannot be negative.")
    
    with transaction() as session:
        transactions = transaction_storage.list_transactions_for_portfolio(session, portfolio)
        positions, _ = calculate_positions(transactions)

        if asset.ticker not in positions:
            raise InsufficientSharesError(f"You do not hold any shares of '{ticker}'.")

        position = portfolio.positions[asset.ticker]

        if quantity > position.quantity:
            raise InsufficientSharesError("You cannot sell more shares than you own.")

        realized_gain = (price - position.average_cost) * quantity
        sale_amount = quantity * price

        account = cash_storage.get_cash_account(session)
        account.balance = account.balance + sale_amount

        add_transaction(session, portfolio, asset, "sell", quantity, price)

    logger.info("Sold %s %s at %s in '%s', realized %s",
                quantity, asset.ticker, price, portfolio.name, realized_gain)
    return realized_gain
