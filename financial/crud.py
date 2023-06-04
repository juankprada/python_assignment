from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date

from financial import models, schemas


def base_query(db: Session, symbol: str, start_date:date, end_date: date):
    """
    Base query used used by other functions to retrieve financial data
    based on optional paramters.

    Arguments:
        db (Session): SQLAlchemy database session.
        symbol (str): Stock identifier.
        start_date (date): Start date to search from.
        end_date (date): End date to search to.

    Returns:
        SQLAlchemy Query.
    """
    query = db.query(models.FinancialData)

    if symbol is not None:
        query =  query.filter(models.FinancialData.symbol == symbol)

    if start_date is not None:
        query = query.filter(models.FinancialData.date >= start_date)

    if end_date is not None:
        query = query.filter(models.FinancialData.date <= end_date)

    return query


def count_financial_data(db: Session, symbol: str, start_date: date, end_date: date )-> int :
    """
    Query to count the number of entries that matches the specified criteria.

    Arguments:
        db (Session): SQLAlchemy database session.
        symbol (str): Stock identifier.
        start_date (date): Start date to search from.
        end_date (date): End date to search to.

    Returns:
        count (int): The number of records in DB that matches the criteria
    """
    return base_query(db, symbol, start_date, end_date ).count()


def get_financial_data_by_symbol(db: Session, symbol: str, start_date: date, end_date: date, offset:int = 0, limit: int = 10):
    """
    Query to count the number of entries that matches the specified criteria.

    Arguments:
        db (Session): SQLAlchemy database session.
        symbol (str): Stock identifier.
        start_date (date): Start date to search from.
        end_date (date): End date to search to.

    Returns:
        count (int): The number of records in DB that matches the criteria
    """
    return base_query(db, symbol, start_date, end_date ).order_by(models.FinancialData.date).offset(offset).limit(limit).all()
