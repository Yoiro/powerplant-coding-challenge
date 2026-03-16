# powerplant-coding-challenge

## Using the API
### Launch the API
Either use the following commands:
1. run `uv sync`
2. To launch the API in development mode, use `uv run fastapi dev --host 0.0.0.0 --port 8888` (those are the defaults).
3. To launch the API in production mode, use `uv run fastapi run --host 0.0.0.0 --port 8888` (once again, those are the defaults.)

or see the section [Running as a Docker container](#running-as-a-docker-container). 


Send the JSON payloads to the `/productionplan/` endpoint. By default, it will use the `NaiveBacktrackingSolver`, or you can ask the service to use a Linear Programming solver by sending your payload to `/productionplan/?solver=lp`.

You will receive the production plan for each plant, sorted in merit-order.

### Running the tests
To launch the tests, simply run `uv run pytest` in the root of the project. 

## Implemented Algorithms
The current service proposes two implementations: `NaiveBacktrackingSolver` and `LPSolver`.
They both use the same algorithm to setup the merit-order: Wind Turbines are activated first since they don't have production cost, the other type of plants are sorted based on their production cost (which, given the examples, typically is gasfired then turbojet).

`NaiveBacktrackingSolver` iterates over all plants, in merit-order and make it produce as much power as possible. If the remaining load is smaller than the current plant's pmin, then we lower the last plant's production by removing the delta between the current plant's pmin and the remaining load. Finally, we assign the remaining load to the current plant's production. Since we parse the list in merit-order, we are guaranteed to respect it.

`LPSolver` is an attempt at using linear programming in order to minimize the production cost. The used model is the following:


We want to minimize the cost of production of each plant, taking the price of generating CO2 into account. The i * 1^-6 term is used in order to ensure that all plants are activated in merit order by having low to no incidence on the final result
```
min Z = S(p_i * cost_i + i * 1^-6) for i in len(plants) + S(cost_co2 * 0.3 * p_j) for j in len(gasfired_plants)
```

**Constraints:**  
We want to ensure that the power produced by a plant is comprised between its pmin and pmax
```
up_i * pmin_i <= p_i <= up_i * pmax_i for i in len(plants)
```

The sum of the production of all plants must be equal to the required load.
```
S(p_i) = load for i in len(plants)
```

### Why two solvers?
I chose to implement two algorithms since the original FAQ specifically asks not to use an already existing solver. However, my first idea was to use linear programming. Knowing that implementing a solver myself would be way too much work, I came up with the `NaiveBacktrackSolver` approach as an "official" solution to the challenge, but still wanted to propose the `LPSolver` to show how I would have tackled the problem without such constraint. This is also why the default solver is `NaiveBacktrackSolver` instead of the LPSolver. 

## Structure of the project
All the service code lies in the `app` folder. You will find basic unit tests in the `tests` one.

```
app
├── ...
├── enums.py                # Contains enums used in the whole app (PlantType, FuelType)
├── main.py                 # Entrypoint containing the FastAPI app object
├── planner.py              # Defines the main object used to compute production planning
├── routers               
│   ├── health.py           # Simple liveness endpoints
│   └── productionplan.py   # ProductionPlan endpoints
├── schemas                 # Folder containing the different schemas used throughout the application
│   ├── forecast.py         # Describes the structure of the payload that has to be sent
│   ├── fuels.py            # Describes the structure of the "fuels" section in a forecast
│   ├── powerplant.py       # Describes the structure of a "powerplant" object in a forecast
│   └── production_plan.py  # Describes the structure of a production_plan for a given plant (this is the object that is returned by the endpoint)
└── solvers                 # Folder containing the different solver modules
    ├── __init__.py
    ├── abstract_solver.py  # Defines the interface for the solvers.
    ├── backtrack.py        # Contains the implementation of the NaiveBacktrackSolver algorithm
    └── lp_solver.py        # Contains the implementation of the LPSolver
```


## Running as a Docker container

Run `docker build --tag powerplant-coding-challenge:sdg --rm .`.  
Once built, run the command `docker run -dit --name ppc_test powerplant-coding-challenge:sdg`.


## Current limitations
* The project only supports three types of powerplants (windturbine, gasfired and turbojet). More may be added when needed.

* We currently don't have the choice of the solver used by the PuLP library, for the LPSolver.

* Basic logging is implemented (via structlog), but only to `stdout`. 