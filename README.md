## Project Description

Python solution that retrieves AlphaVantage data through its public API, stores it in a local database,
and provides a simple API to retrieve the data paginated according to parameters and some statistical information.

The initial requirements can be found at: https://github.com/G123-jp/python_assignment


### Prerequisites

Make sure `docker` and `docker-composer` are installed on your machine.


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

The rest of the environment variables are setup to match the configuration of the database included in the Docker image

For each environment feel free to modify these parameters as required as the Postgres database will also use these.


### Build Docker Image
Execute the following command:

`docker-compose up`

After it finishes running both the database and the API service should be running.
The schema of the database is handled directly by Postrgress on the Docker Image. 
The `schema.sql` file is mapped as volume in the Docker image to the path `/docker-entrypoint-initdb.d/`.
Postgres uses this path and executes all scripts within it once.


### Prepare the initial data
At this point no data has been pre-loaded into the database. So we are going to populate the database by
running the `get_raw_data.py` python script:

```bash
docker exec financial-api python get_raw_data.py
```

When the script finishes it will be possible to find data through the API.


### Testing the API

At this point it is possible to test the API through `CURL` or a web browser.

Examples in curl:

**financial_data endpoint**
```bash
curl --location 'http://localhost:5000/api/financial_data?null=null&start_date=2023-05-10&end_date=2023-06-05&symbol=IBM&limit=2'
```


**statistics endpoint**
```bash
url --location 'http://localhost:5000/api/statistics?start_date=2023-05-01&end_date=2023-06-01&symbol=IBM'
```

## Tech Stack

### Software versions

* Python 3.10
* Docker 20.10.23-ce, build 6051f1429
* Docker Compose version 2.18.1
* PostgreSQL 15.3-alpine (as provided by Postgres official Dockerhub image)


### Python Dependencies

* pytest: Used for unit and integration tests
* psycopg2-binary: Used for DB connectivity
* requests: Used for consuming Alphavantage API
* fastapi: Used to build the API.
* uvicorn: ASGI web server used to run the FastAPI application
* pydantic: Used for data validation.
* pydantic[dotenv]: Used to retrieve .env files
* SQLAlchemy: Used to interact with the DB in the API.
* httpx: Needed for Integraton tests.

**Regarding get_raw_data.py Script**

The script was first part to be developed. It was intended to be simple and
have few dependncies and that is why `psycopg2` was used to handle the interaction with the Posgres Database.

Never the less a few dependencies were used as utilities for logging and environment settings handle (pydantic's Basesettings).

All interaction with the Database is done through regular `SQL`.

**Regarding the API**

After launching the Docker image it is possible to access the API documentation at (http://localhost:5000/docs )
or at (http://localhost:5000/redoc).

**Note:** Please note that documentation is not complete. A beter effort can be made to provide better API documentation.


The API was done using `FastAPI`. The reason for selecting over `Flask` or other alternatives is its simplicity, speed,
perfomance and (last but not least) familiarity with the framework. FastAPI also allows out of the box concurrency, provides
depenency injection, automatic documenation based on **OpenAPI** and integration with `pydantic` for data valiation.


**Regarding Interaction with the Database on the API**
*SQLAlchemy* was chosen instead of direct *SQL* commands as it provides an easy way to interact with the Database through
its *ORM* implementation. It is certainly less efficient than direct SQL calls, but due to the nature of this API
it was considered that extra perfomance gains would not benefit the project in a significant way.

That being said, if we wanted to increase the perfomance of the API (specially the statistics endpoint), It
is recommened to switch to pure SQL commands directly (either through SQLAlchemy or for less overhead, psycopg2).

An extra perfomance gain can be obtained by leveraging the calculation of the statiscis data to the database
instead of doing it in code.


### Tests

Some unit tests and integration tests were made for this api and it can be executed with the following command

```bash
docker exec financial-api pytest
```

These test cover mostly API endpoints and some logic applied to Query params validations.
They can be improved and better organized.
