from fastapi.testclient import TestClient
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker, declarative_base

from financial.main import app
from financial.database import Base, get_db
from financial.models import FinancialData
from financial.crud import count_financial_data
from datetime import date

SQLALCHEMY_DB_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def pre_populate_test_db():

    entries = []
    entries.append(FinancialData(symbol="IBM", date=date(2020, 1, 1), open_price=3.14, close_price=3.18, volume=2.232))
    entries.append(FinancialData(symbol="IBM", date=date(2020, 1, 2), open_price=3.15, close_price=3.19, volume=2.233))
    entries.append(FinancialData(symbol="IBM", date=date(2020, 1, 3), open_price=3.16, close_price=3.20, volume=2.234))
    entries.append(FinancialData(symbol="IBM", date=date(2020, 1, 4), open_price=3.17, close_price=3.21, volume=2.235))
    entries.append(FinancialData(symbol="AAPL", date=date(2020, 1, 1), open_price=3.14, close_price=3.18, volume=2.232))
    entries.append(FinancialData(symbol="AAPL", date=date(2020, 1, 2), open_price=3.14, close_price=3.19, volume=2.233))
    entries.append(FinancialData(symbol="AAPL", date=date(2020, 1, 3), open_price=3.14, close_price=3.20, volume=2.234))

    with next(override_get_db()) as db:
        db.add_all(entries)
        db.commit()


    count = count_financial_data(next(get_db()), "IBM", date(2020, 1, 1), date(2020, 1, 4))
    print(f"Inserted {count} records")


def clear_test_db():
    with next(override_get_db()) as db:
        db.query(FinancialData).delete()
        db.commit()

    count = count_financial_data(next(get_db()), "IBM", date(2020, 1, 1), date(2020, 1, 4))
    print(f"Existing: {count} records")

client = TestClient(app)





def test_get_financial_data():
    pre_populate_test_db()
    response = client.get("/api/financial_data?&start_date=2020-01-01&end_date=2020-01-04&symbol=IBM&limit=2")

    clear_test_db()

    assert response.json() == {
        "data": [
            {
                "date": "2020-01-01",
                "open_price": 3.14,
                "volume": 2.232,
                "close_price": 3.18,
                "symbol": "IBM"
            },
            {
                "date": "2020-01-02",
                "open_price": 3.15,
                "volume": 2.233,
                "close_price": 3.19,
                "symbol": "IBM"
            }
        ],
        "pagination": {
            "count": 4,
            "page": 1,
            "limit": 2,
            "pages": 2
        },
        "info": {
            "error": ""
        }
    }

def test_get_financial_data_no_data():
    pre_populate_test_db()
    response = client.get("/api/financial_data?&start_date=2020-02-01&end_date=2020-02-04&symbol=IBM&limit=2")

    clear_test_db()

    assert response.json() == {
        "data": [],
        "pagination": {},
        "info": {
            "error": "No entries found with the provided criteria."
        }
    }


def test_get_statiscs_fail_request_validation_error_start_date():
    pre_populate_test_db()

    response = client.get("/api/financial_data?&start_date=2020&end_date=2020-02-04&symbol=IBM&limit=2")

    clear_test_db()

    assert response.status_code == 400
    assert response.json() == {
        "info": {
            "error": [
                {
                    "start_date": "Incorrect data format, should be YYYY-MM-DD"
                }
            ]
        }
    }

def test_get_statiscs_fail_request_validation_error_end_date():
    pre_populate_test_db()

    response = client.get("/api/financial_data?&start_date=2020-01-01&end_date=02-04&symbol=IBM&limit=2")

    clear_test_db()

    assert response.status_code == 400
    assert response.json() == {
        "info": {
            "error": [
                {
                    "end_date": "Incorrect data format, should be YYYY-MM-DD"
                }
            ]
        }
    }

def test_get_statiscs_fail_request_validation_error_symbol():
    pre_populate_test_db()

    response = client.get("/api/financial_data?&start_date=2020-01-01&end_date=02-04&symbol=I&limit=2")

    clear_test_db()

    assert response.status_code == 400
    assert response.json() == {
        "info": {
            "error": [
                {
                    "end_date": "Incorrect data format, should be YYYY-MM-DD"
                }
            ]
        }
    }



def test_get_statiscs_success():
    pre_populate_test_db()

    response = client.get("/api/statistics?symbol=IBM&start_date=2020-01-01&end_date=2020-01-04")

    clear_test_db()

    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "start_date": "2020-01-01",
            "end_date": "2020-01-04",
            "symbol": "IBM",
            "average_daily_open_price": 3.155,
            "average_daily_close_price": 3.195,
        "average_daily_volume": 2.234
        },
         "info": {
            "error": ""
         }
    }




def test_get_statiscs_fail_symbol_missing():
    pre_populate_test_db()
    response = client.get("/api/statistics?start_date=2023-05-01&end_date=2023-06-01")

    clear_test_db()

    assert response.status_code == 400
    assert response.json() == {
        "info": {
            "error": [
                {
                    "symbol": "field required"
                }
            ]
        }
    }



def test_get_statiscs_fail_date_missing():
    pre_populate_test_db()
    response = client.get("/api/statistics?symbol=IBM")

    clear_test_db()

    assert response.status_code == 400
    assert response.json() == {
        "info": {
            "error": [
                {
                    "start_date": "field required"
                },
                {
                    "end_date": "field required"
                }
            ]
        }
    }
