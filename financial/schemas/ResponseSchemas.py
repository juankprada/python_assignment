from pydantic import BaseModel
from datetime import date

class FinancialDataResponse(BaseModel):
    """ Financial Data response Model """
    data: list = []
    pagination: dict | None = None
    info: dict | None = None

class StatisticsResponse(BaseModel):
    """ Statistics Response Model """
    data: dict | None = None
    info: dict | None = None
