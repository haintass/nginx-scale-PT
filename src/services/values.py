import re
from collections import defaultdict

from structlog import get_logger

from src.core.config.app_settings import AppSettings
from src.schemas.values import ValuesRead, ValuesWrite

logger = get_logger(__name__)
config = AppSettings()


class ValuesService:
    @staticmethod
    async def filter_values_by_rules(values: ValuesWrite, rules: dict[str, str]) -> ValuesRead:
        """Метод подсчитываем значения по заданным правилам и возвращает результат в виде словаря"""
        filtered_values: dict[str, int] = defaultdict(int)
        reversed_rules = {value: key for key, value in rules.items()}
        combined_pattern = "|".join(rules.values())
        pattern = re.compile(combined_pattern)

        for value in values.values:
            matches = pattern.finditer(value)
            for match in matches:
                value_key = reversed_rules[match.group()]
                filtered_values[value_key] += 1

        return ValuesRead(filtered_values)


def get_values_service() -> ValuesService:
    return ValuesService()
