from pydantic import BaseModel, Field
from utils.config import DefaultSettings


class AppSettings(BaseModel):
    host: str = Field(...)
    port: int = Field(...)


class RabbiMQSettings(BaseModel):
    rabbit_url: str = Field(...)
    rabbit_host: str = Field(...)
    rabbit_port: int = Field(...)


class PostgeSettings(BaseModel):
    url: str = Field(...)
    user: str = Field(...)
    password: str = Field(...)
    db_name: str = Field(...)


class AuthSettings(BaseModel):
    secret_key: str = Field(...)
    algorithm: str = Field(...)
    access_token_expire_minutes: int = Field(...)


class Settings(DefaultSettings):
    DEBUG: bool = False

    app: AppSettings
    database: PostgeSettings
    rabbit: RabbiMQSettings
    auth: AuthSettings

    class Config:
        extra = "ignore"
        env_path = "web/.env"
        config_path = "web/config.json"


settings = Settings()
