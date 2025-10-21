from typing import List, Optional
from sqlalchemy import JSON, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class OrdersOrm(BaseModel):
    __tablename__ = "orders"

    status: Mapped[str] = mapped_column(
        String(50), default="pending", index=True)
    order_number: Mapped[str] = mapped_column(
        String(100), unique=True, index=True)

    customer_email: Mapped[str] = mapped_column(
        String(200), nullable=False, index=True)
    customer_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    customer_name: Mapped[str] = mapped_column(String(200), nullable=False)

    subtotal: Mapped[int] = mapped_column(Integer, nullable=False)
    shipping_cost: Mapped[int] = mapped_column(Integer, default=0)
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)

    shipping_method: Mapped[str] = mapped_column(String(100))
    shipping_address: Mapped[dict] = mapped_column(JSON, nullable=False)

    payment_method: Mapped[str] = mapped_column(String(100))
    payment_status: Mapped[str] = mapped_column(String(50), default="pending")
    payment_id: Mapped[Optional[str]] = mapped_column(String(200))

    customer_comment: Mapped[Optional[str]] = mapped_column(Text)
    admin_notes: Mapped[Optional[str]] = mapped_column(Text)

    items: Mapped[List["OrdersItemsOrm"]] = relationship(
        "OrdersItemsOrm",
        back_populates="order"
    )


class OrdersItemsOrm(BaseModel):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False)

    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    product_price: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    customization_data: Mapped[List] = mapped_column(JSON, default=list)

    order: Mapped["OrdersOrm"] = relationship(
        "OrdersOrm", back_populates="items")
    product: Mapped["ProductsOrm"] = relationship(  # type: ignore
        "ProductsOrm", back_populates="orders")
