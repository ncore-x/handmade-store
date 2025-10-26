from src.api.admin import router as admin_router
from src.api.category import router as categories_router
from src.api.product import router as products_router
from src.api.order import router as orders_router

__all__ = [
    "admin_router",
    "categories_router",
    "products_router",
    "orders_router",
]
