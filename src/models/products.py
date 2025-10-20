from src.models.base import BaseModel


class ProductsOrm(BaseModel):
    __tablename__ = "categories"


class ProductsImagesOrm(BaseModel):
    __tablename__ = "products_images"
