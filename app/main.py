from fastapi import FastAPI

from .routers import productionplan_router, health_router

app = FastAPI()

app.include_router(productionplan_router)
app.include_router(health_router)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, reload=True)
