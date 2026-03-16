import structlog
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from app.schemas import Forecast, ProductionPlan
from app.planner import create_model


logger = structlog.get_logger()
productionplan_router = APIRouter(
    prefix="/productionplan",
    tags=["Production Plan"],
    responses={
        500: {"description": "Internal Server Error"},
        400: {"description": "Bad Request"}
    }
)


@productionplan_router.post("/")
def production_plan(forecast: Forecast, solver: str | None = None) -> list[ProductionPlan]:
    logger.debug("Production plan request received", forecast=forecast)
    try:
        planner = create_model(forecast, solver)
        result = planner.solve()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    else:
        logger.info("Production plan computed", result=result)
        return result

