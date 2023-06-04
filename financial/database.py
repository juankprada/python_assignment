from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from financial.settings import Settings

# Get envionment settings to setup DB Connection
settings = Settings()

SQLALCHEMY_DB_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}/{settings.POSTGRES_DB}"

# Setup SQLAlchemy database connection
engine = create_engine(
    SQLALCHEMY_DB_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Provide a DB sesson
def get_db():
    """ Get Database Session """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
