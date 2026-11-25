from decimal import Decimal
from portfolio_tracker.service.price_service import get_price
from portfolio_tracker.models.portfolio import Portfolio
from portfolio_tracker.errors.portfolio_errors import DuplicatePortfolioError, PortfolioNotFound, PortfolioNotEmptyError
from portfolio_tracker.database import transaction
from portfolio_tracker.storage import portfolio_storage, transaction_storage
from portfolio_tracker.models.position import Position
selected_portfolio_id = None


def create_portfolio(name, description):
    name = name.strip()
    description = description. strip()

    with transaction() as session:
        existing= portfolio_storage.find_portfolio_by_name(session, name)

        if existing is not None:
            raise DuplicatePortfolioError(
                f"A portfolio named '{name}' already exists"
            )
        portfolio = Portfolio(name=name, description=description)
        portfolio_storage.save_portfolio(session, portfolio)

    return portfolio 

def calculate_positions(transactions):
    # replays the trades in the order they happened to rebuild what is held now
    positions = {}
    realized_gain = Decimal("0")

    for transaction in transactions:
        ticker = transaction.asset.ticker
        quantity = transaction.quantity
        price = transaction.price_per_share

        if transaction.side == "buy":
            if ticker in positions:
                position = positions[ticker]
                total_cost = (position.quantity * position.average_cost) + (quantity * price)
                position.quantity = position.quantity + quantity
                position.average_cost = total_cost / position.quantity
            else:
                positions[ticker] = Position(ticker, quantity, price)

        elif transaction.side == "sell":
            position = positions[ticker]
            realized_gain += (price - position.average_cost) * quantity
            position.quantity = position.quantity - quantity

            # a fully sold asset is no longer a holding
            if position.quantity == 0:
                del positions[ticker]

    return positions, realized_gain

def find_portfolio(name):
    name = name.strip().lower()

    with transaction() as session:
        portfolio= portfolio_storage.find_portfolio_by_name(session, name)

    if portfolio is None:
        raise PortfolioNotFound(
            f"No portfolio with name '{name}' exists"
        )
    return portfolio


def view_all_portfolios():
    with transaction() as session:
        portfolios = portfolio_storage.list_portfolios(session)

    return portfolios


def select_portfolio(name):
    global selected_portfolio_id
    portfolio = find_portfolio(name)
    selected_portfolio_id= portfolio.id
    return portfolio


def view_selected_portfolio():
    if selected_portfolio_id is None:
        raise PortfolioNotFound("No portfolio has been selected")
    with transaction() as session:
        portfolio = portfolio_storage.find_portfolio_by_id(session, selected_portfolio_id)

    # the selected portfolio could have been deleted since it was selected
    if portfolio is None:
        raise PortfolioNotFound("The selected portfolio no longer exists")

    return portfolio

def delete_portfolio(name):
    global selected_portfolio_id

    name = name.strip().lower()

    with transaction() as session:
        portfolio = portfolio_storage.find_portfolio_by_name(session, name)

        if portfolio is None:
            raise PortfolioNotFound(
                f"No portfolio with name '{name}' exists"
            )

        if portfolio.transactions:
            raise PortfolioNotEmptyError(
                f"Cannot delete '{portfolio.name}' because it has transactions"
            )

        portfolio_storage.delete_portfolio(session, portfolio)

    if selected_portfolio_id == portfolio.id:
        selected_portfolio_id = None

def get_portfolio_summary():
    portfolio = view_selected_portfolio()
    
    with transaction() as session:
        transactions = transaction_storage.list_transactions_for_portfolio(session, portfolio)

    positions, realized_gain = calculate_positions(transactions)

    rows = []
    total_market_value = Decimal("0")
    total_unrealized_gain = Decimal("0")

    for position in positions.values():
        current_price = get_price(position.ticker)

        # if the user has not set a price for this asset yet, we cannot value it
        if current_price is None:
            market_value = None
            unrealized_gain = None
        else:
            market_value = position.quantity * current_price
            unrealized_gain = (current_price - position.average_cost) * position.quantity
            total_market_value += market_value
            total_unrealized_gain += unrealized_gain

        rows.append({
            "ticker": position.ticker,
            "quantity": position.quantity,
            "average_cost": position.average_cost,
            "current_price": current_price,
            "market_value": market_value,
            "unrealized_gain": unrealized_gain,
        })

    return {
        "portfolio": portfolio,
        "rows": rows,
        "total_market_value": total_market_value,
        "total_unrealized_gain": total_unrealized_gain,
        "realized_gain": realized_gain,
    }


