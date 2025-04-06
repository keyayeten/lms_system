from pydantic import BaseModel, Field
from utils.config import DefaultSettings


class AppSettings(BaseModel):
    host: str = Field(...)
    port: int = Field(...)


class PostgeSettings(BaseModel):
    url: str = Field(...)
    user: str = Field(...)
    password: str = Field(...)
    db_name: str = Field(...)


class Settings(DefaultSettings):
    DEBUG: bool = False

    app: AppSettings
    database: PostgeSettings

    class Config:
        extra = "ignore"
        env_path = "web/.env"
        config_path = "web/config.json"


settings = Settings()
