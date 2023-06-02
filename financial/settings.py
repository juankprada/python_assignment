from pydantic import BaseSettings

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
        env_file = '.env', '../.env'
