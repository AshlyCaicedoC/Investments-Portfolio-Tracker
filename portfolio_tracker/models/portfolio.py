from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from portfolio_tracker.database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(String(255))

    # deleting a portfolio also deletes its trade history (and so its realized gains)
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="portfolios",
        cascade="all, delete-orphan",
        lazy= 'selectin')
