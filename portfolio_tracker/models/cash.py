from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Decimal, ForeignKey, Numeric

from portfolio_tracker.database import Base

class CashAccount(Base):
    __tablename__ = "cash_account"
# the database rejects 
    __table_args__ = (
        CheckConstraint("balance >= 0", name="balance"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[Decimal] = mapped_column(Numeric(14, 2), name="balance")