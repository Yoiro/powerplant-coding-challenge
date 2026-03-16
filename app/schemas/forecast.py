from pydantic import BaseModel

from app.schemas.powerplant import PowerPlant
from app.schemas.fuels import Fuels


class Forecast(BaseModel):
    load: int
    fuels: Fuels
    powerplants: list[PowerPlant]
