from __future__ import annotations

import datetime
import os

from pydantic import BaseSettings, validator, Field
from sqlalchemy.engine import URL

BASE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


class Config(BaseSettings):
    TITLE: str = "Tasks API"
    DESCRIPTION: str = "..."
    VERSION: str = "0.1.0"
    DEBUG: bool = Field(default=False)
    TESTING: bool = Field(default=False)
    SECRET_KEY: str

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str = Field(default="localhost")
    DATABASE_PORT: int = Field(default=3306)
    DATABASE_NAME: str = Field(default="hive")
    ALCHEMICAL_DATABASE_URI: str | URL | None = None

    @validator("ALCHEMICAL_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, value: str | None, values: dict):
        if values.get("TESTING"):
            return "sqlite:///:memory:"

        if isinstance(value, str):
            return value

        return str(URL.create(
            "mysql+pymysql",
            username=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASSWORD"),
            host=values.get("DATABASE_HOST"),
            port=values.get("DATABASE_PORT"),
            database=values.get("DATABASE_NAME"),
            query={"charset": "utf8"}
        ))

    CACHE_TYPE: str = Field(default="RedisCache")
    CACHE_REDIS_HOST: str = Field(default="localhost")
    CACHE_REDIS_PORT: int = Field(default=6379)
    CACHE_REDIS_PASSWORD: str = Field(default="")
    CACHE_REDIS_DB: str = Field(default="0")

    CORS_ALLOW_HEADERS: str = "Content-Type, Authorization"
    CORS_EXPOSE_HEADERS: str = "Content-Disposition"

    FILES_DIRECTORY = os.path.join(BASE_DIRECTORY, "protected")

    class Config:
        case_sensitive = True
