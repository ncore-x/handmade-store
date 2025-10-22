from src.schemas.base import BaseSchema, TimestampSchema, IDSchema

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
