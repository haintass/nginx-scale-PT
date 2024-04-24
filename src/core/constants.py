from enum import Enum

MAX_VALUES_COUNT = 1023
MAX_VALUE_LENGTH = 255


class RedisKeys(str, Enum):
    rules = "app_rules_key"
