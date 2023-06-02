from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date

import models, schemas


def base_query(db: Session, symbol: str, start_date:date, end_date: date):
    query = db.query(models.FinancialData)

    if symbol is not None:
        query =  query.filter(models.FinancialData.symbol == symbol)

    if start_date is not None:
        query = query.filter(models.FinancialData.date >= start_date)

    if end_date is not None:
        query = query.filter(models.FinancialData.date <= end_date)

    return query


def count_financial_data(db: Session, symbol: str, start_date: date, end_date: date )-> int :
    return base_query(db, symbol, start_date, end_date ).count()


def get_financial_data(db: Session, offset:int = 0, limit: int = 5):
    return db.query(models.FinancialData).order_by(models.FinancialData.date).slice(offset, limit ).limit(limit).all()

def get_financial_data_by_symbol(db: Session, symbol: str, start_date: date, end_date: date, offset:int = 0, limit: int = 10):
    return base_query(db, symbol, start_date, end_date ).offset(offset).limit(limit).all()
