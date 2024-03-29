import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVICE_URL = os.getenv("SERVICE_URL", "http://127.0.0.1:8000")
    REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    ELASTIC_HOST = os.getenv("ELASTIC_HOST", "127.0.0.1")
    ELASTIC_PORT = int(os.getenv("ELASTIC_PORT", "9200"))
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = ".env"


settings: Settings = Settings()
