from portfolio_tracker.models.transaction import Transaction 

transactions = []

def add_transaction( portfolio, asset, quantity, side, price):
    transactions.append(Transaction(portfolio, asset, quantity, side, price))

class TransactionService:
    def __init__(
        self,
        asset_service: AssetService,
        portfolio_service: PortfolioService,
        cash_service: CashService,
    ):
        self._asset_service = asset_service
        self._portfolio_service = portfolio_service
        self._cash_service = cash_service

    def buy(self, ticker: str, quantity: Decimal, price_per_share: Decimal) -> Transaction:
        portfolio = self._portfolio_service.get_selected_portfolio()
        asset = self._asset_service.get_asset(ticker)
        require_positive(quantity, "quantity")
        require_positive(price_per_share, "price per share")

        # Debit first: if cash is short this raises before the position is touched,
        # so a refused buy never leaves the portfolio half-updated.
        self._cash_service.debit(quantity * price_per_share)

        position = portfolio.positions.setdefault(asset.ticker, Position(ticker=asset.ticker))
        position.average_cost = _weighted_average_cost(position, quantity, price_per_share)
        position.quantity += quantity

        transaction = Transaction(
            side=TradeSide.BUY,
            ticker=asset.ticker,
            quantity=quantity,
            price_per_share=price_per_share,
            executed_at=datetime.now(),
        )
        portfolio.transactions.append(transaction)
        logger.info(
            "Bought %s %s at %s in '%s'", quantity, asset.ticker, price_per_share, portfolio.name
        )
        return transaction

    def sell(self, ticker: str, quantity: Decimal, price_per_share: Decimal) -> Transaction:
        portfolio = self._portfolio_service.get_selected_portfolio()
        asset = self._asset_service.get_asset(ticker)
        require_positive(quantity, "quantity")
        require_non_negative(price_per_share, "price per share")

        position = portfolio.positions.get(asset.ticker)
        held_quantity = position.quantity if position else Decimal("0")
        if quantity > held_quantity:
            raise InsufficientSharesError(asset.ticker, quantity, held_quantity, portfolio.name)

        # Average cost is unchanged by a sell; only the quantity drops.
        realized_gain = (price_per_share - position.average_cost) * quantity
        position.quantity -= quantity
        if position.quantity == 0:
            # Closed positions leave the view; their realized gain stays in the portfolio total.
            del portfolio.positions[asset.ticker]

        portfolio.realized_gain += realized_gain
        self._cash_service.credit(quantity * price_per_share)

        transaction = Transaction(
            side=TradeSide.SELL,
            ticker=asset.ticker,
            quantity=quantity,
            price_per_share=price_per_share,
            executed_at=datetime.now(),
            realized_gain=realized_gain,
        )
        portfolio.transactions.append(transaction)
        logger.info(
            "Sold %s %s at %s in '%s' (realized gain %s)",
            quantity, asset.ticker, price_per_share, portfolio.name, realized_gain,
        )
        return transaction


def _weighted_average_cost(position: Position, added_quantity: Decimal, price_per_share: Decimal) -> Decimal:
    total_cost = position.average_cost * position.quantity + added_quantity * price_per_share
    return total_cost / (position.quantity + added_quantity)