from typing import Literal

from pydantic import BaseModel, Field


class PowerPlant(BaseModel):
    name: str
    type_: Literal["gasfired", "turbojet", "windturbine"] = Field(alias="type")
    efficiency: float
    pmin: int
    pmax: int
    cost: float = 0.0