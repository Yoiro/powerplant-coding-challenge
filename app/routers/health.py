from fastapi import APIRouter

health_router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@health_router.get("/", status_code=200)
def health():
    return {"status": "ok"}
