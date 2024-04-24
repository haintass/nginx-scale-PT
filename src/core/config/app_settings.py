from pydantic import Field

from src.core.config import Settings
from src.core.config.redis_settings import RedisSettings


class AppSettings(Settings):
    app_name: str
    app_version: str

    redis_db: RedisSettings = Field(default_factory=RedisSettings)
