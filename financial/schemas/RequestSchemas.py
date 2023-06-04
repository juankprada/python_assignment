from pydantic import BaseModel, root_validator
from datetime import date, timedelta
from fastapi import Query

from pydantic.errors import PydanticValueError
from pydantic.error_wrappers import ErrorWrapper
from fastapi.exceptions import RequestValidationError


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

    symbol: str = Query(title="Identifier of the stock")
    start_date: str = Query(title="Search entries from this date")
    end_date: str = Query(title="Search eantries until this date")

    @root_validator()
    def dates_cross_validation(cls, values):
        cross_validate_dates(values["start_date"], values["end_date"])

        return values


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
    symbol: str | None = Query(None, title="Identifier of the stock")
    start_date: str | None = Query(None, title="Search entries from this date")
    end_date: str | None = Query(None, title="Search eantries until this date")
    page: int | None = Query(1, gt=0, title="Page number. Used for Pagination.")
    limit: int | None = Query(5, gt=1,title="Number of records to retrieve by page")


    @root_validator()
    def dates_cross_validation(cls, values):
        cross_validate_dates(values["start_date"], values["end_date"])

        return values




class DateFormatError(PydanticValueError):
    msg_template = "Incorrect data format, should be YYYY-MM-DD"

class DateRangeError(PydanticValueError):
    msg_template = "start_date should be before end_date."


def cross_validate_dates(start_date, end_date):

    field1 = "start_date"
    field2 = "end_date"

    s_date = date_format_validation(start_date, field1)
    e_date = date_format_validation(end_date, field2)


    if s_date is None or e_date is None:
        return

    if (e_date - s_date) < timedelta(0) :
        raise RequestValidationError( errors=[
            ErrorWrapper(
                DateRangeError(),
                loc=(f"{field1},{field2}")
            )
        ])


def date_format_validation(v, field):
    result = None

    if v is not None:
        try:
            result = date.fromisoformat(v)
        except ValueError:
            raise RequestValidationError(errors=[
                ErrorWrapper(
                    DateFormatError(),
                    loc=(field)
                )
            ])


    return result
