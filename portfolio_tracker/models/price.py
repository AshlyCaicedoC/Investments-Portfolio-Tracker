from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from portfolio_tracker.database import Base


class Price(Base):
    __tablename__ = "prices"
    # the database rejects a negative price, even if a bug skips the Python check
    __table_args__ = (
        CheckConstraint("price >= 0", name="price_not_negative"),
    )

    # each asset has at most one current price, so the asset's id is also this table's key
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), primary_key=True)
    price: Mapped[Decimal] = mapped_column(Numeric(14, 4))

    asset: Mapped["Asset"] = relationship(back_populates="price")