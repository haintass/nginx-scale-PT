from fastapi import APIRouter

from src.api.v1 import rules, values

common_router = APIRouter()

common_router.include_router(rules.router, prefix="/rules", tags=["Rules"])
common_router.include_router(values.router, prefix="/values", tags=["Values"])
