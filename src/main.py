import logging
from contextlib import asynccontextmanager
from typing import Any

import redis.asyncio as async_redis
import structlog
import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import ORJSONResponse

from src.api.v1 import common_router
from src.core import logger
from src.core.config.app_settings import AppSettings
from src.db import redis as redis_app

# Настройки приложения
app_config = AppSettings()
log = structlog.get_logger()


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> Any:
    # Подключаемся к базам при старте сервера
    # Подключиться можем при работающем event-loop
    # Поэтому логика подключения происходит в асинхронной функции
    redis_app.pool = async_redis.ConnectionPool.from_url(
        app_config.redis_db.url,
        decode_responses=True,
    )

    redis_app.redis = async_redis.Redis(connection_pool=redis_app.pool)

    yield

    # Отключаемся от баз при выключении сервера
    await redis_app.pool.disconnect()


app = FastAPI(
    title=app_config.app_name,
    redoc_url="/api/redoc",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    version=app_config.app_version,
    lifespan=lifespan,
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
    return await http_exception_handler(
        request,
        HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error"),
    )


app.include_router(common_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        log_config=logger.LOGGING,
        log_level=logging.DEBUG,
    )
