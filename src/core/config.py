import os

from logging import config as logging_config
from pydantic import BaseSettings
from src.core.logger import LOGGING


class Settings(BaseSettings):
    logging_config.dictConfig(LOGGING)
    PROJECT_NAME = os.getenv("PROJECT_NAME", "movies")
    REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    ELASTIC_HOST = os.getenv("ELASTIC_HOST", "127.0.0.1")
    ELASTIC_PORT = int(os.getenv("ELASTIC_PORT", 9200))
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")

    class Config:
        env_file = ".env"


settings = Settings()