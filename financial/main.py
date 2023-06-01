from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_root():
    return {"Hello": "World"}


@app.get("/api/financial_data")
def get_financial_data(query: Union[str, None] = None):
    return """{
    "data": [
        {
            "symbol": "IBM",
            "date": "2023-01-05",
            "open_price": "153.08",
            "close_price": "154.52",
            "volume": "62199013",
        },
        {
            "symbol": "IBM",
            "date": "2023-01-06",
            "open_price": "153.08",
            "close_price": "154.52",
            "volume": "59099013"
        },
        {
            "symbol": "IBM",
            "date": "2023-01-09",
            "open_price": "153.08",
            "close_price": "154.52",
            "volume": "42399013"
        }
    ],
    "pagination": {
        "count": 20,
        "page": 2,
        "limit": 3,
        "pages": 7
    },
    "info": {'error': ''}
    }
    """
