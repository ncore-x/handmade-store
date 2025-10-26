from typing import List, Optional
from sqlalchemy import JSON, Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class ProductsOrm(BaseModel):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    short_description: Mapped[Optional[str]] = mapped_column(String(500))

    price: Mapped[int] = mapped_column(Integer, nullable=False)
    compare_at_price: Mapped[Optional[int]] = mapped_column(Integer)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    material: Mapped[Optional[str]] = mapped_column(String(100))
    color: Mapped[Optional[str]] = mapped_column(String(50))
    width: Mapped[Optional[int]] = mapped_column(Integer)
    length: Mapped[Optional[str]] = mapped_column(String(50))
    clasp_type: Mapped[Optional[str]] = mapped_column(String(100))

    is_customizable: Mapped[bool] = mapped_column(Boolean, default=False)
    customizable_options: Mapped[List] = mapped_column(JSON, default=list)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False)

    category: Mapped["CategoriesOrm"] = relationship(  # type: ignore
        "CategoriesOrm", back_populates="products")
    images: Mapped[List["ProductsImagesOrm"]] = relationship(
        "ProductsImagesOrm", back_populates="product")
    orders: Mapped[List["OrdersItemsOrm"]] = relationship(  # type: ignore
        "OrdersItemsOrm", back_populates="product")


class ProductsImagesOrm(BaseModel):
    __tablename__ = "products_images"

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    alt_text: Mapped[Optional[str]] = mapped_column(String(200))
    is_main: Mapped[bool] = mapped_column(Boolean, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    product: Mapped["ProductsOrm"] = relationship(
        "ProductsOrm", back_populates="images")
