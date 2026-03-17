from pydantic import BaseModel, Field


class Fuels(BaseModel):
    gas: float = Field(alias="gas(euro/MWh)", gt=0)
    kerosine: float = Field(alias="kerosine(euro/MWh)", gt=0)
    co2: float = Field(alias="co2(euro/ton)", gt=0)
    wind: float = Field(alias="wind(%)", ge=0, le=100)
