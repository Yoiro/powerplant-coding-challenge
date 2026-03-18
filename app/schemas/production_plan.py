from pydantic import BaseModel


class ProductionPlan(BaseModel):
    name: str
    p: float
