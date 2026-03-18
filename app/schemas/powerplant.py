from typing import Literal

from pydantic import BaseModel, Field


class PowerPlant(BaseModel):
    name: str = Field(min_length=1)
    type_: Literal["gasfired", "turbojet", "windturbine"] = Field(alias="type")
    efficiency: float = Field(gt=0)
    pmin: int = Field(ge=0)
    pmax: int = Field(gt=0)
    cost: float = 0.0
