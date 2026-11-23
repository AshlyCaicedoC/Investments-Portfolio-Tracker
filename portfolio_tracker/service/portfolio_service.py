from decimal import Decimal
from portfolio_tracker.models.portfolio import Portfolio
from portfolio_tracker.service.price_service import get_price
from portfolio_tracker.models.portfolio import Portfolio
from portfolio_tracker.errors.portfolio_errors import DuplicatePortfolioError, PortfolioNotFound, PortfolioNotEmptyError


portfolios = {} # will be replaced with real persistance when we introduce databases 

selected_portfolio = None


def create_portfolio(name, description):
    name = name.strip()

    if name.lower() in portfolios:
        raise DuplicatePortfolioError(
            f"A portfolio named '{name}' already exists"
        )

    portfolios[name.lower()] = Portfolio(name, description)


def find_portfolio(name):
    name = name.strip().lower()

    if name in portfolios:
        return portfolios[name]
    else:
        raise PortfolioNotFound(
            f"No portfolio with name '{name}' exists"
        )


def view_all_portfolios():
    return list(portfolios.values())


def select_portfolio(name):
    global selected_portfolio

    selected_portfolio = find_portfolio(name)
    return selected_portfolio


def view_selected_portfolio():
    if selected_portfolio is None:
        raise PortfolioNotFound("No portfolio has been selected")

    return selected_portfolio


def delete_portfolio(name):
    global selected_portfolio

    name = name.strip().lower()

    if name not in portfolios:
        raise PortfolioNotFound(
            f"No portfolio with name '{name}' exists"
        )

    portfolio = portfolios[name]

    if portfolio.positions:
        raise PortfolioNotEmptyError(
            f"Cannot delete '{portfolio.name}' because it still has positions"
        )

    if selected_portfolio == portfolio:
        selected_portfolio = None

    del portfolios[name]


def get_portfolio_summary():
    portfolio = view_selected_portfolio()

    rows = []
    total_market_value = Decimal("0")
    total_unrealized_gain = Decimal("0")

    for position in portfolio.positions.values():
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
        "realized_gain": portfolio.realized_gain,
    }


