from pydantic import BaseModel, validator
from datetime import date
from fastapi import Query


class GetStatisticsParams(BaseModel):
    '''
    Model used to define the Query parameters for Get Statistics Data endpoint.

    Extends BaseModel from pydantic and provides Query validation for each of the fields.

    Arguments:
       symbol (str): The identifier of the stocks
       start_date (str): String with the start date value.
       end_date (str): String with the end date value.
       page (int): The page requested. Default is 1
       limit (int): Number of records to retrieve by page. Default is 5
    '''

    symbol: str = Query(min_length=3, max_length=3, title="Identifier of the stock")
    start_date: str = Query(title="Search entries from this date")
    end_date: str = Query(title="Search eantries until this date")

    @validator('start_date', 'end_date')
    def start_date_validation(cls, v):
        if v is None:
            return v

        try:
            date.fromisoformat(v)
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD" )

        return v



class GetFinancialDataParams(BaseModel):
    '''
    Model used to define the Query parameters for Get Financial Data endpoint.

    Extends BaseModel from pydantic and provides Query validation for each of the fields.

    Arguments:
       symbol (str): The identifier of the stocks
       start_date (str): String with the start date value.
       end_date (str): String with the end date value.
       page (int): The page requested. Default is 1
       limit (int): Number of records to retrieve by page. Default is 5
    '''
    symbol: str | None = Query(None, min_length=3, max_length=3, title="Identifier of the stock")
    start_date: str | None = Query(None, title="Search entries from this date")
    end_date: str | None = Query(None, title="Search eantries until this date")
    page: int | None = Query(1, gt=0, title="Page number. Used for Pagination.")
    limit: int | None = Query(5, gt=1,title="Number of records to retrieve by page")

    @validator('start_date', 'end_date')
    def start_date_validation(cls, v):
        if v is None:
            return v

        try:
            date.fromisoformat(v)
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD" )

        return v



class FinancialData(BaseModel):
    symbol: str
    date: date
    open_price: float
    close_price: float
    volume: float

    class Config:
        orm_mode = True

class PaginationModel(BaseModel):
    count: int
    page: int
    limit: int
    pages: int


class FinancialDataResponse(BaseModel):
    data: list[FinancialData] = []
    pagination: PaginationModel | None = None
    info: dict | None = None




class StatisticsResponse(BaseModel):
    data: dict | None = None
    info: dict | None = None
