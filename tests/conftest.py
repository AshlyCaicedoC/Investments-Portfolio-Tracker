from decimal import Decimal 

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from portfolio_tracker import database
from portfolio_tracker.service import portfolio_service, price_service, asset_service, cash_service
import portfolio_tracker.models



@pytest.fixture(autouse=True)
def empty_db(monkeypatch):
    # connect to an in-memory database instead of the real one
    engine = create_engine("sqlite://")
    database.Base.metadata.create_all(engine)
    # transaction() asks SessionLocal for every session, so point it at the test engine
    monkeypatch.setattr(database, "SessionLocal", sessionmaker(bind=engine, expire_on_commit=False))

    # the selected portfolio and the current prices live in Python variables, not in the
    # database, so a fresh database doesn't reset them; without these two lines a test
    # could see the selection or prices left behind by an earlier test
    monkeypatch.setattr(portfolio_service, "selected_portfolio_id", None)
    monkeypatch.setattr(price_service, "prices", {})

    yield
    engine.dispose()

@pytest.fixture
def set_prices(monkeypatch):
    # replaces the price source with prices the test chooses
    def _set(fake_prices):
         monkeypatch.setattr(portfolio_service, "get_price", lambda ticker: fake_prices.get(ticker))
    return _set

@pytest.fixture
def funded_portfolio():
    # 10,000 in cash, a portfolio called Growth already selected, and AAPL added as an asset
    cash_service.deposit_cash(Decimal("10000"))
    portfolio_service.create_portfolio("Growth", "Tech stocks")
    portfolio_service.select_portfolio("Growth")
    asset_service.add_asset("AAPL", "Apple Inc.")