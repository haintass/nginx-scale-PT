import logging

import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title="nginx-scale-PT",
    redoc_url="/api/redoc",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    version=1.0,
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
    return await http_exception_handler(
        request,
        HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error"),
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        log_level=logging.DEBUG,
    )
