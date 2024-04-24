from typing import Any, Union

import structlog
from fastapi import Depends, HTTPException, status
from redis.asyncio import Redis

from src.db.redis import get_redis

logger = structlog.get_logger(__name__)


class RedisBaseService:
    def __init__(self, db: Redis) -> None:
        self.db = db

    async def get(self, *, key: str) -> Any:
        """Return the value at `key` name, or `None` if the key doesn't exist"""
        return await self.db.get(key)

    async def set(self, *, key: str, value: Union[str, bytes]) -> None:
        """Set `value` with key `key`"""
        try:
            await self.db.set(key, value)
        except Exception as error:
            logger.error(f"SET to Redis error: {error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Не удалось записать данные в Redis"
            )

        logger.info("SET to Redis is done", key=f"{key}")

    async def hmset(
        self,
        mapping: dict[str, Any] | None = None,
        *,
        name: str,
    ) -> None:
        """Set key to value within hash ``name`` for each corresponding
        key and value from the ``mapping`` dict."""
        try:
            await self.db.hmset(name=name, mapping=mapping)  # type: ignore
        except Exception as error:
            logger.error(f"HMSET to Redis error: {error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Не удалось записать данные в Redis"
            )

        logger.info("HMSET to Redis is done", name=f"{name}")

    async def hgetall(self, *, name: str) -> dict[str, Any]:
        """Return a Python dict of the hash's name/value pairs"""
        try:
            return await self.db.hgetall(name)  # type: ignore
        except Exception as error:
            logger.error(f"HGETALL Redis error: {error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Не удалось получить данные из Redis"
            )

    async def hdel(self, name: str, *keys: str) -> None:
        """Delete ``keys`` from hash ``name``"""
        await self.db.hdel(name, *keys)  # type: ignore

    async def delete(self, *names: str) -> None:
        """Delete one or more keys specified by ``names``"""
        await self.db.delete(*names)


def get_cache(redis: Redis = Depends(get_redis)) -> RedisBaseService:
    return RedisBaseService(db=redis)
