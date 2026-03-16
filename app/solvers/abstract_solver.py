from abc import ABC, abstractmethod

from app.schemas import PowerPlant, ProductionPlan, Fuels


class AbstractSolver(ABC):
    """
    Abstract class for the solvers. It defines the interface that all solvers must implement.
    """
    @abstractmethod
    def solve(self, plants: list[PowerPlant], costs: Fuels, load: int) -> list[ProductionPlan]:
        raise NotImplementedError
