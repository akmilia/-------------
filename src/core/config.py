from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', validate_default=False, extra='ignore')

    # App info
    APP_NAME: str = 'Backend'
    APP_DESCRIPTION: str = 'API for the services'
    DEBUG: bool = Field(default=False)

    # Database
    DATABASE_URL: str = Field(default='sqlite:///sql.db')

    # Redis
    REDIS_URL: str = Field(default='redis://localhost:6379/0')


settings = Settings()
