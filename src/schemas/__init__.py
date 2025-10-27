from src.schemas.base import BaseSchema, TimestampSchema, IDSchema

from src.schemas.admin import (
    AdminRequestAdd,
    AdminAdd,
    Admin,
    AdminResponse,
    AdminWithHashedPassword,
)

from src.schemas.category import (
    CategoryBase,
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryWithProducts,
    CategoryWithChildren,
)

from src.schemas.product import (
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

from src.schemas.order import (
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
    "BaseSchema",
    "TimestampSchema",
    "IDSchema",

    "AdminRequestAdd",
    "AdminAdd",
    "Admin",
    "AdminResponse",
    "AdminWithHashedPassword",

    "CategoryBase",
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryResponse",
    "CategoryWithProducts",
    "CategoryWithChildren",

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
