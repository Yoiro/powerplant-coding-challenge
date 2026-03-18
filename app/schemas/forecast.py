from pydantic import BaseModel, Field

from app.schemas.fuels import Fuels
from app.schemas.powerplant import PowerPlant


class Forecast(BaseModel):
    load: int = Field(gt=0)
    fuels: Fuels
    powerplants: list[PowerPlant] = Field(min_length=1)
