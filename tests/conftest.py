from decimal import Decimal 

import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from portfolio_tracker import database
from portfolio_tracker.service import portfolio_service, price_service
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