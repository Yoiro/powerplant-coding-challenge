import structlog

from app.schemas import PowerPlant, ProductionPlan, Fuels
from app.enums import PlantType
from app.solvers.abstract_solver import AbstractSolver

logger = structlog.get_logger()


class NaiveBacktrackingSolver(AbstractSolver):
    """
    Backtracking solver based on a greedy algorithm.
    """
    async def solve(self, plants: list[PowerPlant], costs: Fuels, load: int) -> list[ProductionPlan]:
        """
        Solves the power plant scheduling problem using a greedy backtracking algorithm.
        This solver works as follows:
            1. Iterate through plants and set the plant's production to its min(pmax, the remaining load).
            2. If a plant cannot meet its minimum production, adjust the previous
               plant's production and assign the minimum production to the current plant.

        :param plants: List of power plants to consider in the production plan.
        :param costs: Fuels costs to calculate the cost of production for each plant.
        :param load: Total load that needs to be met by the production plan.
        :return: List of ProductionPlan indicating how much power each plant should produce.
        """
        remaining_load = load
        result = []
        for plant in plants:
            logger.debug("Processing plant", plant=plant, remaining_load=remaining_load)
            if plant.pmin > 0 and remaining_load > 0 and remaining_load < plant.pmin:
                delta = plant.pmin - remaining_load
                result[-1].p -= delta
                remaining_load += delta
            if plant.type_ == PlantType.WINDTURBINE:
                # in this case, the wind "cost" actually tells us how much wind there is.
                # 0% means no wind, 100% means full wind. Hence, it can be considered more like
                # the efficiency of the wind turbine rather than the cost of fuel.
                is_windy = int(costs.wind > 0)
                result.append(
                    ProductionPlan(
                        name=plant.name,
                        p=round(min(is_windy * plant.pmax * costs.wind / 100, remaining_load), 1)
                    )
                )
            elif plant.pmin > 0:
                result.append(
                    ProductionPlan(
                        name=plant.name,
                        p=round(min(plant.pmax, remaining_load), 1)
                    )
                )
            else:
                result.append(
                    ProductionPlan(
                        name=plant.name,
                        p=round(min(plant.pmax, remaining_load), 1)
                    )
                )
            remaining_load -= result[-1].p
            logger.debug("Processed plant", plant=plant, remaining_load=remaining_load, assigned_production=result[-1].p)
        return result