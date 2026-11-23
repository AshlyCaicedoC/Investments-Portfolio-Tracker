from portfolio_tracker.models.portfolio import Portfolio
from portfolio_tracker.errors.portfolio_errors import DuplicatePortfolioError, PortfolioNotFound


portfolios = {} # will be replaced with real persistance when we introduce databases 

selected_portfolio = None


def create_portfolio(name, description):
    name = name.strip()

    if name.lower() in portfolios:
        raise DuplicatePortfolioError(
            f"A portfolio named '{name}' already exists"
        )

    portfolios[name.lower()] = Portfolio(name, strategy)


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
