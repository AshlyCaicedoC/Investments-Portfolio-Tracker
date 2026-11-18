from portfolio_tracker.models.portfolio import Portfolio
from portfolio_tracker.errors.portfolio_errors import DuplicatePortfolioError, PortfolioNotFound


portfolios = {} # will be replaced with real persistance when we introduce databases 

# we will create a model 
def create_portfolio(name, description):
    if name in portfolios:
        raise DuplicatePortfolioError(f"A portfolio named '{name}' already exists")
    portfolios[name]= Portfolio(name, description)

def find_portfolio(name):
    if name in portfolios:
        return portfolios[name]
    else:
        raise PortfolioNotFound(f"No Portfolio with name '{name}' exists")