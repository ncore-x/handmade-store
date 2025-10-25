import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.admin import router as router_admins
from src.api.categories import router as router_categories
from src.api.orders import router as router_orders
from src.api.products import router as router_products


sys.path.append(str(Path(__file__).parent.parent))

# Создание приложения FastAPI
app = FastAPI(
    title="Handmade Store API",
    description="API для магазина handmade браслетов",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(router_admins)
app.include_router(router_categories)
app.include_router(router_orders)
app.include_router(router_products)


@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "Добро пожаловать в Handmade Store API!",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
