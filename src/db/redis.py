from redis.asyncio import ConnectionPool, Redis

# Соединение с redis происходит в main.py на этапе инициализации fastapi приложения
redis: Redis = None  # type: ignore
pool: ConnectionPool = None  # type: ignore


# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    return redis
