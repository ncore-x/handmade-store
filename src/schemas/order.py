from typing import List, Optional, Dict, Any
from pydantic import Field, EmailStr

from src.schemas.base import BaseSchema, TimestampSchema, IDSchema
from src.schemas.product import ProductResponse


class OrderItemBase(BaseSchema):
    product_name: str = Field(..., max_length=200)
    product_price: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    customization_data: Dict[str, Any] = Field(default_factory=dict)


class OrderItemCreate(OrderItemBase):
    product_id: int = Field(..., gt=0)


class OrderItemResponse(OrderItemBase, IDSchema, TimestampSchema):
    order_id: int
    product_id: int


class OrderItemWithProduct(OrderItemResponse):
    product: ProductResponse


class OrderBase(BaseSchema):
    customer_email: EmailStr
    customer_phone: str = Field(..., min_length=5, max_length=20)
    customer_name: str = Field(..., min_length=1, max_length=200)
    shipping_method: str = Field(..., max_length=100)
    shipping_address: Dict[str, Any]
    payment_method: str = Field(..., max_length=100)
    customer_comment: Optional[str] = None


class OrderCreate(OrderBase):
    items: List[OrderItemCreate] = Field(..., min_items=1)


class OrderUpdate(BaseSchema):
    status: Optional[str] = Field(None, max_length=50)
    payment_status: Optional[str] = Field(None, max_length=50)
    payment_id: Optional[str] = Field(None, max_length=200)
    admin_notes: Optional[str] = None
    shipping_method: Optional[str] = Field(None, max_length=100)
    shipping_address: Optional[Dict[str, Any]] = None


class OrderResponse(OrderBase, IDSchema, TimestampSchema):
    status: str = "pending"
    order_number: str
    subtotal: int
    shipping_cost: int
    total_amount: int
    payment_status: str = "pending"
    payment_id: Optional[str] = None
    admin_notes: Optional[str] = None


class OrderWithItems(OrderResponse):
    items: List[OrderItemResponse] = []


class OrderFull(OrderWithItems):
    items: List[OrderItemWithProduct] = []


class OrderStatusUpdate(BaseSchema):
    status: str = Field(..., max_length=50)


class PaymentStatusUpdate(BaseSchema):
    payment_status: str = Field(..., max_length=50)
    payment_id: Optional[str] = Field(None, max_length=200)


class OrderStats(BaseSchema):
    total_orders: int
    pending_orders: int
    completed_orders: int
    total_revenue: int
