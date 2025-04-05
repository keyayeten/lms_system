from utils.config import DefaultSettings
from pydantic import BaseModel, Field


class PostgeSettings(BaseModel):
    url = Field(default=..., alias="url")


class Settings(DefaultSettings):
    DEBUG: bool = False
    database: PostgeSettings = Field(...)


settings = Settings()
