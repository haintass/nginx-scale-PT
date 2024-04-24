from pydantic import RootModel


class RulesBase(RootModel):
    root: dict[str, str]


class RulesWrite(RulesBase):
    pass


class RulesRead(RulesBase):
    pass
