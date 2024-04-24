from fastapi import APIRouter, Depends
from structlog import get_logger

from src.core.config.app_settings import AppSettings
from src.core.constants import RedisKeys
from src.schemas import RulesRead
from src.schemas.values import ValuesRead, ValuesWrite
from src.services.rules import RulesService, get_rules_service
from src.services.values import ValuesService, get_values_service

router = APIRouter()

app_config = AppSettings()
logger = get_logger(__name__)


@router.post("/", response_model=ValuesRead)
async def filter_values(
    *,
    rules_service: RulesService = Depends(get_rules_service),
    values_service: ValuesService = Depends(get_values_service),
    values: ValuesWrite,
) -> ValuesRead:
    """Метод проверяет список строк на соответствие правилам и возвращает результат в виде словаря,
    где ключом является название правила, а значением - количество соответствующих правилу строк.

    Общее количество строк должно быть меньше 1024, а длина каждой строки меньше 256

    Args:
        values (ValuesWrite): список строк для проверки

    Raises:
        HTTPException: возвращает 422 если входные параметры не соответствуют правилам валидации
        HTTPException: возвращает 500 если не удалось получить данные из редиса
    """
    rules: RulesRead = await rules_service.get_rules(name=RedisKeys.rules.value)
    values_result: ValuesRead = await values_service.filter_values_by_rules(values, rules.dict())

    return values_result
