from src.schemas.base import BaseSchema, TimestampSchema, IDSchema

# Сначала импортируем базовые схемы без композитных типов
from src.schemas.admins import (
    AdminBase,
    AdminCreate,
    AdminUpdate,
    AdminResponse,
    AdminLogin,
    Token,
    TokenData,
)

from src.schemas.categories import (
    CategoryBase,
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryWithProducts,
    CategoryWithChildren,
)

from src.schemas.products import (
    ProductBase,
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductWithCategory,
    ProductWithImages,
    ProductFull,
    ProductImageBase,
    ProductImageCreate,
    ProductImageUpdate,
    ProductImageResponse,
    CustomizationRequest,
)

from src.schemas.orders import (
    OrderBase,
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderWithItems,
    OrderFull,
    OrderItemBase,
    OrderItemCreate,
    OrderItemResponse,
    OrderItemWithProduct,
    OrderStatusUpdate,
    PaymentStatusUpdate,
    OrderStats,
)

# Теперь разрешаем forward references
from src.schemas.categories import CategoryWithProducts, CategoryWithChildren
from src.schemas.products import ProductWithCategory, ProductWithImages, ProductFull

# Явно вызываем model_rebuild для схем с forward references
try:
    CategoryWithProducts.model_rebuild()
    CategoryWithChildren.model_rebuild()
    ProductWithCategory.model_rebuild()
    ProductWithImages.model_rebuild()
    ProductFull.model_rebuild()
    OrderItemWithProduct.model_rebuild()
except Exception as e:
    print(f"Warning: Could not rebuild some models: {e}")

__all__ = [
    # Base
    "BaseSchema",
    "TimestampSchema",
    "IDSchema",

    # Admins
    "AdminBase",
    "AdminCreate",
    "AdminUpdate",
    "AdminResponse",
    "AdminLogin",
    "Token",
    "TokenData",

    # Categories
    "CategoryBase",
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryResponse",
    "CategoryWithProducts",
    "CategoryWithChildren",

    # Products
    "ProductBase",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "ProductWithCategory",
    "ProductWithImages",
    "ProductFull",
    "ProductImageBase",
    "ProductImageCreate",
    "ProductImageUpdate",
    "ProductImageResponse",
    "CustomizationRequest",

    # Orders
    "OrderBase",
    "OrderCreate",
    "OrderUpdate",
    "OrderResponse",
    "OrderWithItems",
    "OrderFull",
    "OrderItemBase",
    "OrderItemCreate",
    "OrderItemResponse",
    "OrderItemWithProduct",
    "OrderStatusUpdate",
    "PaymentStatusUpdate",
    "OrderStats",
]
