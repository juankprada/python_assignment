import math

from datetime import datetime, date
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, status, Request, Response, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, Annotated

from financial import schemas, crud, models
from financial.database import get_db


# Start our FastAPI app
app = FastAPI(
    title="Financial API",
    description="API done for python assignment."
)



@app.exception_handler(ValueError)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc) -> JSONResponse:
    """
    Exception handler for Validation errors.

    Returns:
        JSONResponse object and HTTP status 400.
    """
    # Map validation errors to a somewhat more readable format
    result = [ {err["loc"][-1] : err["msg"] } for err in exc.errors()]

    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"info": { "error" : result } }),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Exception handler for internal errors.

    Returns:
        JSONResponse object and HTTP status 500
    """
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({"info": {"error" : "Internal Server Error"}})
    )



@app.get("/api/financial_data", response_model=schemas.FinancialDataResponse, response_model_exclude_unset=True)
async def get_financial_data(
        params: Annotated[schemas.GetFinancialDataParams,  Depends(schemas.GetFinancialDataParams)],
        db:Session = Depends(get_db)):
    """
    Returns a list of finanal data from the requested symbol.
    The data is provided based on the date range defined in the Request Parameters.
    Additional parameters for pagination can be provided.

    Arguments:
        symbol (str): Company Identifier for the request.
        start_date (str): Supported format is YYYY-MM-DD.
        end_date (str): Supported format is YYYY-MM-DD. Should be a date after start_date.
        limit (int): Number of records returned per page.
        page (int): Requested page number.

    Returns:
        JSONResponse object with the following structure:
        data:
            - symbol
            - date
            - open_price
            - close_price
            - volume
        info:
            - error
        pagination:
            - count
            - limit
            - page
            - pages
    """

    # Get the total amount of records that match the query criteria.
    record_count = crud.count_financial_data(db, params.symbol, params.start_date, params.end_date)

    data = []
    pagination = { }
    # Avoid doing unnecesary things if no data was return before.
    if record_count != 0:

        # Calculate the right offset based on page param and the limit of entries per page.
        offset = max(0,(params.page -1)) * params.limit
        current_page = params.page

        # Actualy retrieve the page data
        data = crud.get_financial_data_by_symbol(db, params.symbol, params.start_date, params.end_date, offset=offset, limit=params.limit)

        # Set pagination information based on query params and retrieve data.
        pagination["count"] = record_count
        pagination["page"] = current_page
        pagination["limit"] = params.limit
        pagination["pages"] = math.ceil(record_count / params.limit)

        # No particular error message set
        if len(data) == 0:
            info = {"error" :"No records on this page"}
        else:
            info = {"error" :""}

    else:
        # Let the client know that no entries were found.
        info={"error" :"No entries found with the provided criteria."}

    # Set response object
    response = schemas.FinancialDataResponse()
    response.data = data
    response.pagination = pagination
    response.info = info

    return response



@app.get("/api/statistics")
async def get_statistics(
        params: Annotated[schemas.GetStatisticsParams, Depends(schemas.GetStatisticsParams)],
        db:Session = Depends(get_db)):
    """
    Get the statistical data for one particular company for the specified date range.

    Arguments:
        symbol (str): Identifier for the company.
        start_date (str): Supported format is YYYY-MM-DD.
        end_date (str): Supported format is YYYY-MM-DD. Should be a date after start_date.

    Returns:
        JSONResponse object with the following structure.
        data:
            - start_date
            - end_date
            - symbol
            - average_daily_open_price
            - average_daily_close_price
            - average_daily_volume
        info:
            - error
    """

    # Retrieve the financial data from DB
    data_list = crud.get_financial_data_by_symbol(db, params.symbol, params.start_date, params.end_date)

    count = len(data_list)

    data = {}

    # Avoid doing calculations if no data.
    if count != 0 :
        # Map our values to make it easy to calculate the averages.
        open_prices = map(lambda data: float(data.open_price), data_list)
        close_prices = map(lambda data: float(data.close_price), data_list)
        volumes = map(lambda data: float(data.volume), data_list)

        # Set statistical data
        data = {
            "start_date": params.start_date,
            "end_date": params.end_date,
            "symbol": params.symbol,
            "average_daily_open_price": round(math.fsum(open_prices) / count, 3 ),
            "average_daily_close_price": round(math.fsum(close_prices) / count, 3),
            "average_daily_volume": round(math.fsum(volumes) / count, 3)
        }
        info = {"error" :""}
    else:
        info = {"error" : f"No records were found for symbol: {params.symbol} on the reqested date range."}

    #Set
    response = schemas.StatisticsResponse()
    response.data = data
    response.info = info

    return response
