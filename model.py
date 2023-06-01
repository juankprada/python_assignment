from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import BigInteger
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry

class Base(DeclarativeBase):
    pass



class FinancialData(Base):
    __tablename__ = "financial_data"

    symbol: Mapped[str] = mapped_column(String, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date(), primarey_key=True)

    open_price: Mapped[float] = mapped_column(Numeric)
    close_price: Mapped[float] = mapped_column(Numeric)
    volume: Mapped[int] = mapped_column(BigInteger)
