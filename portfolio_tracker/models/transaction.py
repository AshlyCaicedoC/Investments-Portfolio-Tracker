from datetime import datetime
from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Numeric, CheckConstraint, Datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship 

from portfolio_tracker.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_transaction_quantity_positive"),
        CheckConstraint("price_per_share >= 0", name="ck_transaction_price_not_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolios.id"))
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"))
    side: Mapped[str] = mapped_column(Enum("buy", "sell"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 4))
    price_per_share: Mapped[Decimal] = mapped_column(Numeric(14, 4))
    trade_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


    # deleting a portfolio also deletes its trade history (and so its realized gains)
    portfolio: Mapped["Portfolio"] = relationship(back_populates="transactions", lazy="selectin")
    asset: Mapped["Asset"] = relationship(back_populates="transactions", lazy='selectin')