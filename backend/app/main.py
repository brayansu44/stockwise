from fastapi import FastAPI
from app.presentation.routers.health import router as health_router
from app.presentation.routers.products import router as products_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API principal para la plataforma StockWise",
    version=settings.PROJECT_VERSION
)

app.include_router(health_router)

app.include_router(products_router)

@app.get("/")
def read_root():
    return {
        "message": "StockWise API funcionando correctamente",
        "environment": settings.ENVIRONMENT,
        "status": "ok"
    }