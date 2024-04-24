from fastapi import APIRouter, Depends, Response, status
from structlog import get_logger

from src.core.config.app_settings import AppSettings
from src.core.constants import RedisKeys
from src.schemas.rules import RulesRead, RulesWrite
from src.services.rules import RulesService, get_rules_service

router = APIRouter()

app_config = AppSettings()
logger = get_logger(__name__)


@router.post("/", response_model=RulesRead)
async def add_rules(
    *,
    rules_service: RulesService = Depends(get_rules_service),
    rules: RulesWrite,
) -> RulesRead:
    """Метод добавляет новые правила

    Args:
        rules (dict[str, str]): правила на добавление

    Raises:
        HTTPException: возвращает 500 если не удалось сохранить правила в редис

    Returns:
        dict[str, str]: добавленные правила
    """
    await rules_service.add_rules(name=RedisKeys.rules.value, rules=rules)
    return RulesRead(rules.dict())


@router.get("/", response_model=RulesRead)
async def get_rules(
    *,
    rules_service: RulesService = Depends(get_rules_service),
) -> RulesRead:
    """Метод возвращает все правила

    Raises:
        HTTPException: возвращает 500 если не удалось получить правила из редис

    Returns:
        dict[str, str]: имеющиеся правила"""
    return await rules_service.get_rules(name=RedisKeys.rules.value)


@router.delete("/{rule_name}")
async def delete_rule(
    *,
    rules_service: RulesService = Depends(get_rules_service),
    rule_name: str,
) -> None:
    """Метод Удаляет правило по rule_name.
    Если правило не найдено, метод вернет 204, как и в случае успешного удаления.

    Args:
        rule_name (str): имя правила на удаление

    Raises:
        HTTPException: возвращает 500 если не удалось удалить правило из редиса

    Returns:
        204 статус код"""
    await rules_service.delete_rule(name=RedisKeys.rules.value, rule_name=rule_name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
