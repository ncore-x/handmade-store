from typing import List, Optional, ForwardRef
from pydantic import Field

from src.schemas.base import BaseSchema, TimestampSchema, IDSchema
from src.schemas.products import ProductResponse

# Для избежания циклических импортов
CategoryResponse = ForwardRef('CategoryResponse')


class CategoryBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    meta_title: Optional[str] = Field(None, max_length=150)
    meta_description: Optional[str] = Field(None, max_length=500)
    sort_order: int = Field(0, ge=0)
    is_active: bool = True


class CategoryCreate(CategoryBase):
    parent_id: Optional[int] = None


class CategoryUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    meta_title: Optional[str] = Field(None, max_length=150)
    meta_description: Optional[str] = Field(None, max_length=500)
    parent_id: Optional[int] = None
    sort_order: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase, IDSchema, TimestampSchema):
    parent_id: Optional[int] = None
    products_count: int = 0


class CategoryWithProducts(CategoryResponse):
    products: List[ProductResponse] = []


class CategoryWithChildren(CategoryResponse):
    children: List['CategoryResponse'] = []
    products_count: int = 0


CategoryResponse.model_rebuild()
CategoryWithChildren.model_rebuild()
