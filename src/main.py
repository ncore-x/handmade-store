# fmt: off
import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

sys.path.append(str(Path(__file__).parent.parent))

from src.middleware.json_error_handler import JSONErrorHandlerMiddleware
from src.api.product import router as router_products
from src.api.order import router as router_orders
from src.api.category import router as router_categories
from src.api.admin import router as router_admins
from src.exception_handlers import validation_exception_handler

app = FastAPI(
    title="Handmade Store API",
    description="API для магазина handmade браслетов",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_middleware(JSONErrorHandlerMiddleware)

app.include_router(router_admins)
app.include_router(router_categories)
app.include_router(router_orders)
app.include_router(router_products)


@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в Handmade Store API!",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
# fmt: on
