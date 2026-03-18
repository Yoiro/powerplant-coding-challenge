import enum


class FuelType(enum.StrEnum):
    GAS = "gas"
    KEROSINE = "kerosine"
    WIND = "wind"


class PlantType(enum.StrEnum):
    GASFIRED = "gasfired"
    TURBOJET = "turbojet"
    WINDTURBINE = "windturbine"
