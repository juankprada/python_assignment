from sqlalchemy import Boolean, Column, Float, String, Date, Integer

from financial.database import Base

class FinancialData(Base):
    """ Model class that maps financial_data DB table """

    __tablename__ = "financial_data"

    symbol = Column(String, primary_key=True, index=True)
    date = Column(Date, primary_key=True, index=True)
    open_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)
