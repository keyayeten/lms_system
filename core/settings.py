from utils.config import DefaultSettings
from pydantic import BaseModel, Field


class AppSettings(BaseModel):
    host: str = Field(default=..., alias="host")
    port: int = Field(default=..., alias="port")


class PostgeSettings(BaseModel):
    url: str = Field(default=..., alias="url")
    user: str = Field(default=..., alias="user")
    password: str = Field(default=..., alias="password")
    db_name: str = Field(default=..., alias="db_name")


class Settings(DefaultSettings):
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"

    app: AppSettings = Field(...)
    database: PostgeSettings = Field(...)


settings = Settings()
