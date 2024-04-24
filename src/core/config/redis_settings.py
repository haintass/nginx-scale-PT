from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    url: str

    model_config = SettingsConfigDict(env_prefix="REDIS_")
