from datetime import datetime
from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship 

from portfolio_tracker.database import Base

class Transaction(Base):
    __tablename__ = " transactions"

     __table_args__ = (
        CheckConstraint("side IN ('buy', 'sell')", name="ck_transaction_side"),
        CheckConstraint("quantity > 0", name="ck_transaction_quantity_positive"),
        CheckConstraint("price >= 0", name="ck_transaction_price_not_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id"))
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    side: Mapped[str] = mapped_column(Enum("buy", "sell"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 4))
    price_per_share: Mapped[Decimal] = mapped_column(Numeric(14, 4))
    trade_datedatetime: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


    # deleting a portfolio also deletes its trade history (and so its realized gains)
    portfolio: Mapped["portfolios"] = relationship(back_populates="transactions", lazy="selectin")
    asset: Mapped["assets"] = relationship(back_populates="transactions", lazy='selectin')