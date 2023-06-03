from typing import Any, Dict, Union, Annotated
from pydantic import BaseModel


from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, status, Request, Response, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from datetime import datetime, date
from database import SessionLocal, engine
from schemas import GetStatisticsParams, GetFinancialDataParams, FinancialDataResponse, StatisticsResponse

import crud, models

import math

import logging


logging.basicConfig(format="[%(levelname)s]-%(asctime)s\t %(message)s ", datefmt="%d-%b-%y %H:%M:%S", level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


# Start our FastAPI app
app = FastAPI(
    title="Financial API",
    description="API done for python assignment."
)


# Provide a DB sesson
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.exception_handler(ValueError)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"info": { "error" : exc.errors() } }),
    )




@app.get("/api/financial_data", response_model=FinancialDataResponse, response_model_exclude_unset=True)
async def get_financial_data(
        params: Annotated[GetFinancialDataParams,  Depends(GetFinancialDataParams)],
        db:Session = Depends(get_db)):

    # Make paginagion work and set minimium offset as 0
    record_count = crud.count_financial_data(db, params.symbol, params.start_date, params.end_date)

    if record_count == 0:
        return JSONResponse(status_code=200, content={"info": {"error" :"No entries found with the provided criteria."}})

    current_page = max(1, params.page)
    offset = max(0,(params.page -1)) * params.limit

    response = FinancialDataResponse()

    response.data = crud.get_financial_data_by_symbol(db, params.symbol, params.start_date, params.end_date, offset=offset, limit=params.limit)
    response.pagination = {
        "count": record_count,
        "page": current_page,
        "limit": params.limit,
        "pages": math.ceil(record_count / params.limit)
    }

    response.info = {"error": ""}


    sample1 = GetFinancialDataParams()
    sample1.symbol = "IBM"

    sample2 = GetFinancialDataParams()
    sample2.symbol = "APP"

    logging.info(f"Sample1: {sample1.symbol}, Sample2: {sample2.symbol}")

    return response



@app.get("/api/statistics")
async def get_statistics(
        params: Annotated[GetStatisticsParams, Depends(GetStatisticsParams)],
        db:Session = Depends(get_db)):


    data_list = crud.get_financial_data_by_symbol(db, params.symbol, params.start_date, params.end_date)

    count = len(data_list)

    if count != 0 :
        open_prices = map(lambda data: float(data.open_price), data_list)
        close_prices = map(lambda data: float(data.close_price), data_list)
        volumes = map(lambda data: float(data.volume), data_list)

        response_data = {
            "start_date": params.start_date,
            "end_date": params.end_date,
            "symbol": params.symbol,
            'average_daily_open_price': math.fsum(open_prices) / count,
            'average_daily_close_price': math.fsum(close_prices) / count,
            'average_daily_volume': math.fsum(volumes) / count
        }
        info = { "error" : ""}
    else:
        response_data = {}
        info = { "error" : f"No records were found for symbol: {params.symbol} on the reqested date range."}


    response = StatisticsResponse()
    response.data = response_data
    response.info = info

    return response
