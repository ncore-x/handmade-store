from typing import List, Optional
from sqlalchemy import select, or_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.repositories.base import BaseRepository
from src.models.product import ProductsOrm, ProductsImagesOrm


class ProductRepository(BaseRepository[ProductsOrm]):
    def __init__(self):
        super().__init__(ProductsOrm)

    async def get_with_images(self, db: AsyncSession, id: int) -> Optional[ProductsOrm]:
        result = await db.execute(
            select(self.model)
            .options(selectinload(self.model.images))
            .where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_with_category_and_images(self, db: AsyncSession, id: int) -> Optional[ProductsOrm]:
        result = await db.execute(
            select(self.model)
            .options(selectinload(self.model.category), selectinload(self.model.images))
            .where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_category(self, db: AsyncSession, category_id: int, skip=0, limit=100) -> List[ProductsOrm]:
        result = await db.execute(
            select(self.model)
            .where(self.model.category_id == category_id)
            .where(self.model.is_active == True)
            .offset(skip).limit(limit)
            .order_by(self.model.created_at.desc())
        )
        return result.scalars().all()

    async def search_products(self, db: AsyncSession, query: str, skip=0, limit=100) -> List[ProductsOrm]:
        search_term = f"%{query}%"
        result = await db.execute(
            select(self.model)
            .where(
                or_(
                    self.model.name.ilike(search_term),
                    self.model.description.ilike(search_term),
                    self.model.short_description.ilike(search_term)
                )
            )
            .where(self.model.is_active == True)
            .offset(skip).limit(limit)
            .order_by(self.model.created_at.desc())
        )
        return result.scalars().all()

    async def get_available_products(self, db: AsyncSession, skip=0, limit=100) -> List[ProductsOrm]:
        result = await db.execute(
            select(self.model)
            .where(self.model.is_active == True)
            .where(self.model.in_stock == True)
            .offset(skip).limit(limit)
            .order_by(self.model.created_at.desc())
        )
        return result.scalars().all()

    async def update_stock(self, db: AsyncSession, product_id: int, new_quantity: int) -> bool:
        result = await db.execute(
            update(self.model)
            .where(self.model.id == product_id)
            .values(stock_quantity=new_quantity, in_stock=new_quantity > 0)
        )
        await db.commit()
        return result.rowcount > 0


class ProductImageRepository(BaseRepository[ProductsImagesOrm]):
    def __init__(self):
        super().__init__(ProductsImagesOrm)

    async def get_by_product(self, db: AsyncSession, product_id: int) -> List[ProductsImagesOrm]:
        result = await db.execute(
            select(self.model).where(self.model.product_id == product_id).order_by(
                self.model.sort_order, self.model.id)
        )
        return result.scalars().all()

    async def get_main_image(self, db: AsyncSession, product_id: int) -> Optional[ProductsImagesOrm]:
        result = await db.execute(
            select(self.model)
            .where(self.model.product_id == product_id)
            .where(self.model.is_main == True)
        )
        return result.scalar_one_or_none()

    async def set_main_image(self, db: AsyncSession, image_id: int) -> bool:
        image = await self.get(db, image_id)
        if not image:
            return False

        await db.execute(
            update(self.model)
            .where(self.model.product_id == image.product_id)
            .values(is_main=False)
        )
        result = await db.execute(
            update(self.model)
            .where(self.model.id == image_id)
            .values(is_main=True)
        )
        await db.commit()
        return result.rowcount > 0
