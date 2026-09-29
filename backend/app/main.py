from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.routers.health import router as health_router
from app.presentation.routers.products import router as products_router
from app.presentation.routers import users
from app.core.config import settings
from app.presentation.routers import auth
from app.presentation.routers.inventory_movements import (
    router as inventory_movements_router,
)
from app.presentation.routers.sales import router as sales_router
from app.presentation.routers.dashboard import router as dashboard_router
from app.presentation.routers.categories import router as categories_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API principal para la plataforma StockWise",
    version=settings.PROJECT_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)

app.include_router(products_router)

app.include_router(users.router)

app.include_router(auth.router)

app.include_router(inventory_movements_router)

app.include_router(sales_router)

app.include_router(dashboard_router)

app.include_router(categories_router)

@app.get("/")
def read_root():
    return {
        "message": "StockWise API funcionando correctamente",
        "environment": settings.ENVIRONMENT,
        "status": "ok"
    }