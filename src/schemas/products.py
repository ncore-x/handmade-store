from typing import List, Optional, Dict, Any
from pydantic import Field, HttpUrl

from src.schemas.base import BaseSchema, TimestampSchema, IDSchema
from src.schemas.categories import CategoryResponse


class ProductBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    short_description: Optional[str] = Field(None, max_length=500)
    price: int = Field(..., gt=0)
    compare_at_price: Optional[int] = Field(None, gt=0)
    stock_quantity: int = Field(0, ge=0)
    material: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=50)
    width: Optional[int] = Field(None, gt=0)
    length: Optional[str] = Field(None, max_length=50)
    clasp_type: Optional[str] = Field(None, max_length=100)
    is_customizable: bool = False
    customizable_options: Dict[str, Any] = Field(default_factory=dict)


class ProductCreate(ProductBase):
    category_id: int = Field(..., gt=0)


class ProductUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    short_description: Optional[str] = Field(None, max_length=500)
    price: Optional[int] = Field(None, gt=0)
    compare_at_price: Optional[int] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    material: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=50)
    width: Optional[int] = Field(None, gt=0)
    length: Optional[str] = Field(None, max_length=50)
    clasp_type: Optional[str] = Field(None, max_length=100)
    is_customizable: Optional[bool] = None
    customizable_options: Optional[Dict[str, Any]] = None
    category_id: Optional[int] = Field(None, gt=0)
    in_stock: Optional[bool] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase, IDSchema, TimestampSchema):
    category_id: int
    in_stock: bool = True
    is_active: bool = True


class ProductWithCategory(ProductResponse):
    category: 'CategoryResponse'


class ProductWithImages(ProductResponse):
    images: List['ProductImageResponse'] = []


class ProductFull(ProductWithCategory, ProductWithImages):
    pass


class ProductImageBase(BaseSchema):
    image_url: HttpUrl
    alt_text: Optional[str] = Field(None, max_length=200)
    is_main: bool = False
    sort_order: int = Field(0, ge=0)


class ProductImageCreate(ProductImageBase):
    product_id: int


class ProductImageUpdate(BaseSchema):
    alt_text: Optional[str] = Field(None, max_length=200)
    is_main: Optional[bool] = None
    sort_order: Optional[int] = Field(None, ge=0)


class ProductImageResponse(ProductImageBase, IDSchema, TimestampSchema):
    product_id: int


class CustomizationRequest(BaseSchema):
    engraving_text: Optional[str] = Field(None, max_length=100)
    initials: Optional[str] = Field(None, max_length=10)
    font_style: Optional[str] = None
    placement: Optional[str] = None
