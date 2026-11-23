from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from portfolio_tracker.database import Base


class Asset(Base):
    __tablename__ = "assets"

    # id has no business meaning, it only identifies the row
    id: Mapped[int] = mapped_column(name = "id", primary_key=True, auto_increment)
    # the ticker is the business identifier, so the database protects it as unique
    ticker: Mapped[str] = mapped_column(name= "ticker", unique=True, nullable=False)
    issuer: Mapped[str] = mapped_column(String(10), unique= True)

    transactions: Mapped[list["Transaction"]] = relationship(lazy="selectin")
    price: Mapped["Price | None"] = relationship(lazy="selectin")

    def __str__(self):
        return f"[Ticker:{self.ticker} | Name: {self.issuer}]"
