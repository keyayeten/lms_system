from utils.config import DefaultSettings
from pydantic import BaseModel, Field


class AppSettings(BaseModel):
    host: str = Field(default=..., alias="host")
    port: int = Field(default=..., alias="port")


class PostgeSettings(BaseModel):
    url: str = Field(default=..., alias="url")


class Settings(DefaultSettings):
    DEBUG: bool = False
    app: AppSettings = Field(...)
    database: PostgeSettings = Field(...)


settings = Settings()
