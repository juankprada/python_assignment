import os, sys
import datetime
import logging
import psycopg2
import requests
import json

from datetime import datetime, date, timedelta
from pydantic import BaseSettings

# Somewhat prettier logs
logging.basicConfig(format="%(asctime)s[%(levelname)s] - %(message)s ", datefmt="%d-%b-%y %H:%M:%S", level=logging.DEBUG)


class Settings(BaseSettings):
    """ Settings class that maps the contents of '.env' file"""

    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str
    API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()



def persist_data(db: psycopg2.extensions.connection, symbol: str, daily_series: dict[str, dict]):
    '''
    Stores in DB the daily stock information provided for every symbol.

    Arguments:
        db (psycopg2.connection): Database connection handler.
        symbol (str): The symbol that identifies company behind the stocks.
        daily_series (dict[str, dict]): Dictionary of daily movement of stock information.
    '''

    logging.debug(f"Persisting data for {symbol}")

    # We use list comprehension to create a list of values from the source dictionar.
    data = [(symbol.strip(), date, values["1. open"], values["4. close"], values["6. volume"]) for (date, values) in daily_series.items()]

    cursor = db.cursor()

    # let's try to store all entries in a single statement.
    try:
        cursor.executemany("""
        INSERT INTO financial_data (symbol, date, open_price, close_price, volume)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (symbol, date)
        DO UPDATE
        SET open_price = EXCLUDED.open_price, close_price = EXCLUDED.close_price, volume = EXCLUDED.volume;
        """, data)
    except Exception:
        db.rollback()
        logging.error("Writing records for '{symbol}' failed")
        raise
    else:
        db.commit()




def populate_database(db: psycopg2.extensions.connection, symbols: list[str]):
    '''
    Calls the Alpha Vantage REST API to retrieve the daily series of entries
    for every symbol specified as parameter. After parsing the response data
    And stores the parsed data in the database

    Arguments:
        db (psycopg2.extensions.connection): Database connection handler.
        symbols (list[str]): a list of strings containing the symbols to process.
    '''

    # Return if symbols is empty
    if len(symbols) == 0:
        logging.debug("Nothing to process")
        return

    # Define the date range used to process data
    date_end = date.today()
    last_week = date_end - timedelta(weeks=2)
    date_start = last_week - timedelta(days=last_week.weekday())


    logging.debug(f"Processing data from {date_start} until {date_end}")

    # Retrieve stock information for every simbol. Processe it and store it in DB
    for symbol in symbols:

        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=compact&apikey={settings.API_KEY}"

        response = requests.get(url)

        if response.status_code == 200:
            daily_series = response.json()["Time Series (Daily)"]
            # Filter entries according to date range
            filtered_daily_series = dict(filter(lambda elem: ( date_start <= datetime.strptime(elem[0], '%Y-%m-%d').date() < date_end), daily_series.items()))

            persist_data(db, symbol, filtered_daily_series)

        else:
            #TODO: hanle this error better
            #NOTE: This API doesn't handle HTTPS codes correctly. Even when errors ocurr like passing no API KEY the response status code is 200
            # Currently I see no way to handle API error responses other than by manually validating the data.
            logging.warning("API call failed with HTTP status {0}", response.status_code)



def setup_db_table(db: psycopg2.extensions.connection):
    '''
    Executes the contents of the file 'schema.sql'. The logic and management of the schema
    is leveraged to the SQL script.

    Arguments:
       db (psycopg2.extensions.connection): DB connection handler.
    '''

    logging.debug("Creating database table based on schema file")
    with db.cursor() as cursor:
        try:
            with open("schema.sql") as schema_file:
                cursor.execute(schema_file.read())
                db.commit()
        except Exception as e:
            logging.error("Error creating schema!")
            logging.error("The process cannot continue without database schema.")
            logging.error("Shutting down.")
            logging.error(e)
            db.close()
            sys.exit(1)



def setup_db_connection() -> psycopg2.extensions.connection:
    '''
    Sets up a database connection to a Postgres SQL server
    Connection parameters are retrieved from envionment settings.
    Make sure the following environment variables are set before calling this function:
     - POSTGRES_HOSTNAME
     - DATABASE_PORT
     - POSTGRES_DB
     - POSTGRES_USER
     - POSTGRES_PASSWORD

    Returns:
       connection (psycopg2.extensions.connection) Handler to the connection to the posgres DB.
    '''

    connection = None
    logging.error(f'Connecting to {settings.POSTGRES_HOSTNAME}, {settings.DATABASE_PORT}, {settings.POSTGRES_USER}')
    try:
        connection = psycopg2.connect(
            host=settings.POSTGRES_HOSTNAME,
            port=settings.DATABASE_PORT,
            database=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD)

    except psycopg2.OperationalError as e:
        logging.error('Unable to connect!\n {0}').format(e)

    return connection


if __name__ == "__main__":

    # Setup DB
    connection = setup_db_connection()


    if connection is None:
        logging.error("Could not connect to the database. Shutting down.")
        sys.exit(1)

    populate_database(connection, ["IBM", "AAPL"])
