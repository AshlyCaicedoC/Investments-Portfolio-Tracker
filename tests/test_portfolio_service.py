import pytest 
from sqlalchemy import URL, create_engine
from portfolio_tracker import database
from portfolio_tracker.service import portfolio_service
from portfolio_tracker.errors.portfolio_errors import (
    DuplicatePortfolioError,
    PortfolioNotFound,
    PortfolioNotEmptyError,
)

def test_created_portfolio_creates_it():
    portfolio_service.create_portfolio("Tech", "Growth stocks")
    assert portfolio_service.find_portfolio("Tech").description == "Growth stocks"

def test_duplicate_portfolio_name_is_refused_no_matter_the_loweruppercase():
    portfolio_service.create_portfolio("Pasive Income", "dividend stocks")

    with pytest.raises(DuplicatePortfolioError):
        portfolio_service.create_portfolio("PASivE iNcOmE", "Another one")

    portfolios = portfolio_service.view_all_portfolios()
    assert len(portfolios) == 1
    assert portfolios[0].description == "dividend stocks"
    