# importing every model here means "import portfolio_tracker.models" registers all tables at once
from portfolio_tracker.models.asset import Asset
from portfolio_tracker.models.portfolio import Portfolio
from portfolio_tracker.models.transaction import Transaction
from portfolio_tracker.models.cash import CashAccount
