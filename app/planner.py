import enum
import structlog

from app.schemas import Forecast, ProductionPlan, PowerPlant, Fuels
from app.enums import PlantType, FuelType
from app.solvers.backtrack import NaiveBacktrackingSolver
from app.solvers.lp_solver import LPSolver

logger = structlog.get_logger()


class Planner:
    FUEL_LOOKUP: dict = {
        PlantType.GASFIRED: FuelType.GAS,
        PlantType.TURBOJET: FuelType.KEROSINE,
        PlantType.WINDTURBINE: FuelType.WIND
    }

    def __init__(self, forecast: Forecast = None, solver = None):
        self.load: int = forecast.load
        self.plants: list[PowerPlant] = forecast.powerplants
        self.costs: Fuels = forecast.fuels
        self._solver = solver or NaiveBacktrackingSolver()

    def add_cost_to_plants(self) -> list[PowerPlant]:
        """
        Add cost to plants based on their type and efficiency. Wind turbines have a cost of 0.
        """
        logger.debug("Adding cost to plants", plants=self.plants, costs=self.costs)
        for plant in self.plants:
            if plant.type_ == PlantType.WINDTURBINE:
                plant.cost = 0
            else:
                plant.cost = getattr(self.costs, self.FUEL_LOOKUP[plant.type_]) / plant.efficiency
        return self.plants

    def sort_plants_by_cost(self) -> list[PowerPlant]:
        """
        Sort plants by cost in ascending order.
        The order determined here is further used as merit-order for the solvers.
        """
        plants = sorted(self.plants, key = lambda p: p.cost)
        logger.debug("Plants sorted by cost", plants=plants)
        return plants

    def solve(self) -> list[ProductionPlan]:
        """
        Calls the underlying solver to solve the problem. 
        The plants are first enriched with their cost and sorted by cost.
        """
        self.add_cost_to_plants()
        plants = self.sort_plants_by_cost()
        return self._solver.solve(plants, self.costs, self.load)


def create_model(forecast: Forecast, solver = None) -> Planner:
    """
    Factory function to create a Planner instance.
    The solver can be specified as a string, either "lp" or "backtracking".
    """
    match solver:
        case "lp":
            logger.debug("Using LP solver")
            solver = LPSolver()
        case _:
            logger.debug("No solver or backtracking specified.Using naive backtracking solver.")
            solver = NaiveBacktrackingSolver()
    planner = Planner(forecast, solver)
    logger.debug("Planner created", planner=planner)
    return planner
