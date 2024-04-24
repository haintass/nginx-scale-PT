from fastapi import Depends
from redis.asyncio import Redis
from structlog import get_logger

from src.core.config.app_settings import AppSettings
from src.db.redis import get_redis
from src.schemas.rules import RulesRead, RulesWrite
from src.services.redis_base import RedisBaseService

logger = get_logger(__name__)
config = AppSettings()


class RulesService:
    def __init__(self, redis: Redis):
        self.redis = RedisBaseService(db=redis)

    async def add_rules(self, name: str, rules: RulesWrite) -> None:
        """Метод добавляет новые правила в redis"""
        await self.redis.hmset(name=name, mapping=rules.dict())

    async def get_rules(self, name: str) -> RulesRead:
        """Метод возвращает правила из redis"""
        data = await self.redis.hgetall(name=name)
        return RulesRead(data)

    async def delete_rule(self, name: str, rule_name: str) -> None:
        """Метод удаляет правило из redis по rule name"""
        await self.redis.hdel(name, rule_name)


def get_rules_service(
    redis: Redis = Depends(get_redis),
) -> RulesService:
    return RulesService(redis=redis)
