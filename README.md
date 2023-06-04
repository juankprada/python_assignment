## Project Description

Python solution that retrieves AlphaVantage data through its public API, stores it in a local database,
and provides a simple API to retrieve the data paginated according to parameters and some statistical information.

The initial requirements can be found at: https://github.com/G123-jp/python_assignment

### Setup

clone the repository and in the project root folder create a `.env` file as follows:

```
DATABASE_PORT=5432
POSTGRES_PASSWORD=password123
POSTGRES_USER=postgres
POSTGRES_DB=fastapi
POSTGRES_HOST=postgres
POSTGRES_HOSTNAME=db

API_KEY=< Use your personal API Kew here>
```

`API_KEY` is used to interact with the public AlphaVantage API and can be retreived by following the
instructions at their [website](https://www.alphavantage.co/support/#api-key)
