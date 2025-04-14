from pydantic import BaseModel, Field
from utils.config import DefaultSettings


class RabbiMQSettings(BaseModel):
    rabbit_url: str = Field(...)
    rabbit_host: str = Field(...)
    rabbit_port: int = Field(...)


class PostgeSettings(BaseModel):
    url: str = Field(...)
    user: str = Field(...)
    password: str = Field(...)
    db_name: str = Field(...)


class RedisSettings(BaseModel):
    redis_host: str = Field(...)
    redis_port: int = Field(...)

    @property
    def redis_url(self):
        return f"redis://{self.redis_host}:{self.redis_port}"


class Settings(DefaultSettings):
    DEBUG: bool = False

    rabbit: RabbiMQSettings
    database: PostgeSettings
    redis: RedisSettings

    class Config:
        extra = "ignore"
        env_path = "content_parser/.env"
        config_path = "content_parser/config.json"


settings = Settings()
