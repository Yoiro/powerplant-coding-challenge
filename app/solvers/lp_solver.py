import pulp
import structlog

from app.enums import PlantType
from app.solvers.abstract_solver import AbstractSolver
from app.schemas import PowerPlant, ProductionPlan, Fuels


class LPSolver(AbstractSolver):
    """
    Linear programming solver based on PuLP library. Uses their default COIN-OR CBC solver.
    """
    async def solve(self, plants: list[PowerPlant], costs: Fuels, load: int) -> list[ProductionPlan]:
        """
        Solves the power plant scheduling problem using linear programming.
        For more information on the generated variables, please refer to `_generate_variables`.
        For more information on the constraints and the objective function, please refer to `_generate_problem`.
        :param plants: List of power plants to consider in the production plan.
        :param costs: Fuels costs to calculate the cost of production for each plant.
        :param load: Total load that needs to be met by the production plan.
        :return: List of ProductionPlan indicating how much power each plant should produce.
        """
        result = []
        variables = self._generate_variables(plants, costs)
        problem = self._generate_problem(plants, costs, load, variables)

        problem.solve()

        # Ensuring that we round the values to 1 decimal place
        for var in [v for v in variables if v.startswith('p_')]:
            variables[var].value = round(variables[var].varValue, 1)

        # Creating the production plan with the results from the solver, in merit-order order.
        for plant in plants:
            result.append(ProductionPlan(name=plant.name, p=variables[f"p_{plant.name}"].varValue))

        return result

    def _generate_variables(self, plants: list[PowerPlant], costs: Fuels) -> dict[str, pulp.LpVariable]:
        """
        Helper function to generate the pulp variables for the problem.
        For each plant, we generate:
        - A binary variable to indicate if the plant is on or off.
        - A continuous variable to indicate the production of the plant, with a maximum bound equal to
          the plant's maximum production (multiplied by the wind percentage for wind turbines).
        - A variable to indicate the cost of production for the plant, which is calculated based on
          the fuel cost and the plant's efficiency. For wind turbines, the cost is set to 0, but we 
          set it to 1 for the purpose of the objective function calculation, since it is going to be
          multiplied by the production variable.

        :param plants: List of power plants to generate variables for.
        :param costs: Fuels costs to calculate the cost of production for each plant.
        :return: Dictionary of generated pulp variables.
        """
        variables = {}
        for plant in plants:
            if plant.type_ == PlantType.WINDTURBINE:
                # Ensuring that the wind turbine does not produce more power than the wind allows
                plant.pmax = plant.pmax * costs.wind / 100
                # We need to set the cost to 1 instead of 0 since it is going to multiply the production variable
                variables[f"cost_{plant.name}"] = 1  
            elif plant.type_ == PlantType.GASFIRED:
                variables[f"cost_{plant.name}"] = costs.gas / plant.efficiency 
            else:
                variables[f"cost_{plant.name}"] = costs.kerosine / plant.efficiency
            # Binary variable to indicate if the plant is on or off
            variables[f"up_{plant.name}"] = pulp.LpVariable(f"up_{plant.name}", lowBound=0, upBound=1, cat=pulp.LpBinary)
            variables[f"p_{plant.name}"] = pulp.LpVariable(f"p_{plant.name}", lowBound=0, upBound=plant.pmax, cat=pulp.LpContinuous)

        return variables

    def _generate_problem(self, plants: list[PowerPlant], costs: Fuels, load: int, variables: dict[str, pulp.LpVariable]) -> pulp.LpProblem:
        """
        Helper function to generate the linear programming problem with the given context.
        All constraints are added to the problem, including:
        - Minimum and maximum production constraints for each plant, linked to the binary variable that indicates if
            the plant is on or off.
        - Total production constraint to ensure that the total production matches the load.
        - Objective function to minimize the total cost, including a small epsilon to break ties between equally-costed plants.

        :param plants: List of power plants to consider in the problem.
        :param costs: Fuels costs to calculate the cost of production for each plant.
        :param load: Total load that needs to be met by the production plan.
        :param variables: Dictionary of pulp variables generated for the problem.
        :return: The generated pulp LpProblem ready to be solved.
        """
        problem = pulp.LpProblem("ProductionPlan", pulp.LpMinimize)
        for var in [k for k in variables if k.startswith("up_")]:
            # Finding the plant that corresponds to the current variable
            plant = next(filter(lambda p: p.name == var.split("_")[1], plants))
            problem += variables[var] * plant.pmin <= variables[f"p_{plant.name}"], f"Minimum production for {plant.name}"
            problem += variables[var] * plant.pmax >= variables[f"p_{plant.name}"], f"Maximum production for {plant.name}"

        epsilon = 1e-6
        problem += pulp.lpSum(
            [(variables[f'cost_{plant.name}'] + i * epsilon) * variables[f'p_{plant.name}'] for i, plant in enumerate(plants)]
            + [costs.co2 * 0.3 * variables[f'p_{plant.name}'] for plant in plants if plant.type_ == PlantType.GASFIRED]
        ), "Total Cost to Minimize"

        problem += pulp.lpSum(
            [variables[f"p_{plant.name}"] for plant in plants]
        ) == load, "Total Production to match"

        return problem