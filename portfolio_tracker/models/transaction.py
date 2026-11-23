from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from portfolio_tracker.database import Base

class Portfolio(Base):
    __tablename__ = "portfolios"

     id: Mapped[int] = mapped_column(primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id"))
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    side: Mapped[str] = mapped_column(Enum("buy", "sell"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 4))
    price_per_share: Mapped[Decimal] = mapped_column(Numeric(14, 4))
    trade_date: Mapped[date]

    # deleting a portfolio also deletes its trade history (and so its realized gains)
    portfolio: Mapped[Portfolio] = relationship()
    asset: Mapped[Asset] = relationship(lazy='selectin')