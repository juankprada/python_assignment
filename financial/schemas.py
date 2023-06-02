from typing import Dict
from pydantic import BaseModel
from datetime import date

class FinancialData(BaseModel):
    symbol: str
    date: date
    open_price: str
    close_price: str
    volume: str

    class Config:
        orm_mode = True

class PaginationModel(BaseModel):
    count: int
    page: int
    limit: int
    pages: int

class ResponseModel(BaseModel):
    data: list[FinancialData] = []
    pagination: Dict | None = None
    info: Dict | None = None
