from typing import List, Optional
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class CategoriesOrm(BaseModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    meta_title: Mapped[Optional[str]] = mapped_column(String(150))
    meta_description: Mapped[Optional[str]] = mapped_column(String(500))

    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    parent: Mapped[Optional["CategoriesOrm"]] = relationship(
        "CategoriesOrm",
        remote_side="CategoriesOrm.id",
        backref="children"
    )

    products: Mapped[List["ProductsOrm"]] = relationship(  # type: ignore
        "ProductsOrm",
        back_populates="category"
    )
