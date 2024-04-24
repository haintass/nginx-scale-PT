from typing import Annotated

from pydantic import BaseModel, Field, RootModel

from src.core.constants import MAX_VALUE_LENGTH, MAX_VALUES_COUNT

MaxLengthStr = Annotated[str, Field(max_length=MAX_VALUE_LENGTH)]


class ValuesWrite(BaseModel):
    values: list[MaxLengthStr] = Field(..., max_items=MAX_VALUES_COUNT)


class ValuesRead(RootModel):
    root: dict[str, int]
