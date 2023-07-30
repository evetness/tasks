from __future__ import annotations

import os

from pydantic import BaseSettings, RedisDsn, validator, Field

BASE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


class Config(BaseSettings):
    """
    For generating a `SECRET_KEY` use the following command:
        $ python3 -c "import secrets; print(secrets.token_urlsafe(32));"
    """
    TITLE: str = "Tasks API"
    DESCRIPTION: str = "..."
    DEBUG: bool = Field(default=False, env='FLASK_DEBUG')
    TESTING: bool = Field(default=False, env='FLASK_TESTING')
    DISABLE_AUTH: bool = Field(default=False)
    SECRET_KEY: str
    LOG_LEVEL: str = Field(default="INFO")

    ALCHEMICAL_DATABASE_URI: str

    CACHE_DEFAULT_TIMEOUT: int = Field(default=0)
    CACHE_TYPE: str = Field(default="RedisCache")
    CACHE_REDIS_URL: RedisDsn

    CORS_ALLOW_HEADERS: str | None
    CORS_EXPOSE_HEADERS: str | None
    CORS_ORIGINS: str | None

    @validator("CORS_ALLOW_HEADERS", "CORS_ORIGINS")
    def convert_separeted_string_to_list_of_string(cls, value: str | None):
        if not value:
            return None
        return [item.strip() for item in value.split(",")]
    
    LOGS_DIRECTORY: str = Field(default=os.path.abspath(os.path.join(os.sep, 'var', 'log')))

    class Config:
        case_sensitive = True
        env_prefix = "FLASK_"
