from fastapi import FastAPI
from app.api.health import router as health_router

app = FastAPI(
    title="StockWise API",
    description="API principal para la plataforma StockWise",
    version="1.0.0"
)

app.include_router(health_router)


@app.get("/")
def read_root():
    return {
        "message": "StockWise API funcionando correctamente",
        "status": "ok"
    }