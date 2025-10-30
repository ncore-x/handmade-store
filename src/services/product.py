from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.product import ProductRepository, ProductImageRepository
from src.repositories.category import CategoryRepository
from src.schemas.product import (
    ProductCreate, ProductResponse,
    ProductWithImages, ProductFull,
    ProductImageCreate, ProductImageResponse
)
from src.services.base import BaseService


class ProductService(BaseService):
    def __init__(self):
        super().__init__(ProductRepository())
        self.category_repo = CategoryRepository()
        self.image_repo = ProductImageRepository()

    async def get_with_images(self, db: AsyncSession, id: int) -> Optional[ProductWithImages]:
        product = await self.repository.get_with_images(db, id)
        if product:
            return ProductWithImages.model_validate(product)
        return None

    async def get_with_category_and_images(self, db: AsyncSession, id: int) -> Optional[ProductFull]:
        product = await self.repository.get_with_category_and_images(db, id)
        if product:
            return ProductFull.model_validate(product)
        return None

    async def get_by_category(self, db: AsyncSession, category_id: int, skip=0, limit=100) -> List[ProductResponse]:
        category = await self.category_repo.get(db, category_id)
        if not category:
            raise ValueError(f"Category with id {category_id} not found")
        products = await self.repository.get_by_category(db, category_id, skip, limit)
        return [ProductResponse.model_validate(prod) for prod in products]

    async def search_products(self, db: AsyncSession, query: str, skip=0, limit=100) -> List[ProductResponse]:
        if not query or len(query.strip()) < 2:
            raise ValueError("Search query must be at least 2 characters long")
        products = await self.repository.search_products(db, query.strip(), skip, limit)
        return [ProductResponse.model_validate(prod) for prod in products]

    async def get_available_products(self, db: AsyncSession, skip=0, limit=100) -> List[ProductResponse]:
        products = await self.repository.get_available_products(db, skip, limit)
        return [ProductResponse.model_validate(prod) for prod in products]

    async def create(self, db: AsyncSession, obj_in: ProductCreate) -> ProductResponse:
        category = await self.category_repo.get(db, obj_in.category_id)
        if not category:
            raise ValueError(
                f"Category with id {obj_in.category_id} not found")
        return await super().create(db, obj_in)

    async def update_stock(self, db: AsyncSession, product_id: int, new_quantity: int) -> bool:
        if new_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        return await self.repository.update_stock(db, product_id, new_quantity)

    async def add_image(self, db: AsyncSession, image_data: ProductImageCreate) -> ProductImageResponse:
        product = await self.repository.get(db, image_data.product_id)
        if not product:
            raise ValueError(
                f"Product with id {image_data.product_id} not found")
        db_image = await self.image_repo.create(db, image_data.model_dump())
        return ProductImageResponse.model_validate(db_image)

    async def get_product_images(self, db: AsyncSession, product_id: int) -> List[ProductImageResponse]:
        images = await self.image_repo.get_by_product(db, product_id)
        return [ProductImageResponse.model_validate(img) for img in images]

    async def set_main_image(self, db: AsyncSession, image_id: int) -> bool:
        return await self.image_repo.set_main_image(db, image_id)


class ProductImageService(BaseService):
    def __init__(self):
        super().__init__(ProductImageRepository())

    async def get_by_product(
        self,
        db: AsyncSession,
        product_id: int
    ) -> List[ProductImageResponse]:
        """Получить все изображения товара"""
        images = await self.repository.get_by_product(db, product_id)
        return [ProductImageResponse.model_validate(img) for img in images]

    async def set_main(
        self,
        db: AsyncSession,
        image_id: int
    ) -> bool:
        """Сделать изображение главным"""
        return await self.repository.set_main_image(db, image_id)
