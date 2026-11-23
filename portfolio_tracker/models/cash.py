from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from portfolio_tracker.database import Base

class CashAccount(Base):
    __tablename__ = "cash_account"
# the database rejects 
    __table_args__ = (
        CheckConstraint("balance >= 0", name="ck_cash_balance_not_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[Decimal] = mapped_column(Numeric(14, 2), name="ck_cash_balance_not_negative")