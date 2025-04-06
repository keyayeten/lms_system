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
        env_path = "content_parser/.env"
        config_path = "content_parser/config.json"


settings = Settings()