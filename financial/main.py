from typing import Any, Dict, Union
from pydantic import BaseModel


from fastapi import FastAPI, status, Request, Response, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session

from database import SessionLocal, engine

import crud, models, schemas
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = FastAPI(
    title="Financial API",
    description="API done for python assignment."
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=418,
        content={"info": { "error" : f"Oops! {exc.name} did something. There goes a rainbow..."} },
    )


@app.get("/api/financial_data", response_model=schemas.ResponseModel, response_model_exclude_unset=True)
def get_financial_data(start_date: str = None,
                             end_date: str = None,
                             symbol: str = None,
                             page: int = 1,
                             limit: int = 5,
                       db:Session = Depends(get_db)):

    # Make paginagion work and set minimium offset as 0
    record_count = crud.count_financial_data(db, symbol, start_date, end_date)

    if record_count == 0:
        return null

    current_page = max(1,page)
    offset = max(0,(page -1)) * limit



    response = schemas.ResponseModel()

    response.data = crud.get_financial_data_by_symbol(db, symbol, start_date, end_date, offset=offset, limit=limit)
    response.pagination = schemas.PaginationModel(
        count=record_count,
        page=current_page,
        limit=limit,
        pages=(record_count / limit))
    response.info = {"error": "none"}


    return response



@app.get("/api/status", tags=["api"])
async def report_status():
    ''' Check the status of the API '''
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"info": "API is working"}
    )

@app.get("/api")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
