from typing import List, Optional, Dict, Any
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.repositories.base import BaseRepository
from src.models.products import ProductsOrm, ProductsImagesOrm


class ProductRepository(BaseRepository[ProductsOrm]):
    def __init__(self):
        super().__init__(ProductsOrm)

    async def get_with_images(self, db: AsyncSession, id: int) -> Optional[ProductsOrm]:
        """Получить товар с изображениями"""
        result = await db.execute(
            select(ProductsOrm)
            .options(selectinload(ProductsOrm.images))
            .where(ProductsOrm.id == id)
        )
        return result.scalar_one_or_none()

    async def get_with_category_and_images(self, db: AsyncSession, id: int) -> Optional[ProductsOrm]:
        """Получить товар с категорией и изображениями"""
        result = await db.execute(
            select(ProductsOrm)
            .options(
                selectinload(ProductsOrm.category),
                selectinload(ProductsOrm.images)
            )
            .where(ProductsOrm.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_category(
        self,
        db: AsyncSession,
        category_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProductsOrm]:
        """Получить товары по категории"""
        result = await db.execute(
            select(ProductsOrm)
            .where(ProductsOrm.category_id == category_id)
            .where(ProductsOrm.is_active == True)
            .offset(skip)
            .limit(limit)
            .order_by(ProductsOrm.created_at.desc())
        )
        return result.scalars().all()

    async def search_products(
        self,
        db: AsyncSession,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProductsOrm]:
        """Поиск товаров по названию и описанию"""
        search_term = f"%{query}%"
        result = await db.execute(
            select(ProductsOrm)
            .where(
                or_(
                    ProductsOrm.name.ilike(search_term),
                    ProductsOrm.description.ilike(search_term),
                    ProductsOrm.short_description.ilike(search_term)
                )
            )
            .where(ProductsOrm.is_active == True)
            .offset(skip)
            .limit(limit)
            .order_by(ProductsOrm.created_at.desc())
        )
        return result.scalars().all()

    async def get_available_products(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProductsOrm]:
        """Получить доступные товары (в наличии и активные)"""
        result = await db.execute(
            select(ProductsOrm)
            .where(ProductsOrm.is_active == True)
            .where(ProductsOrm.in_stock == True)
            .offset(skip)
            .limit(limit)
            .order_by(ProductsOrm.created_at.desc())
        )
        return result.scalars().all()

    async def update_stock(
        self,
        db: AsyncSession,
        product_id: int,
        new_quantity: int
    ) -> bool:
        """Обновить количество товара на складе"""
        from sqlalchemy import update

        result = await db.execute(
            update(ProductsOrm)
            .where(ProductsOrm.id == product_id)
            .values(
                stock_quantity=new_quantity,
                in_stock=new_quantity > 0
            )
        )
        await db.commit()
        return result.rowcount > 0


class ProductImageRepository(BaseRepository[ProductsImagesOrm]):
    def __init__(self):
        super().__init__(ProductsImagesOrm)

    async def get_by_product(self, db: AsyncSession, product_id: int) -> List[ProductsImagesOrm]:
        """Получить все изображения товара"""
        result = await db.execute(
            select(ProductsImagesOrm)
            .where(ProductsImagesOrm.product_id == product_id)
            .order_by(ProductsImagesOrm.sort_order, ProductsImagesOrm.id)
        )
        return result.scalars().all()

    async def get_main_image(self, db: AsyncSession, product_id: int) -> Optional[ProductsImagesOrm]:
        """Получить главное изображение товара"""
        result = await db.execute(
            select(ProductsImagesOrm)
            .where(ProductsImagesOrm.product_id == product_id)
            .where(ProductsImagesOrm.is_main == True)
        )
        return result.scalar_one_or_none()

    async def set_main_image(self, db: AsyncSession, image_id: int) -> bool:
        """Установить изображение как главное"""
        from sqlalchemy import update

        # Сначала сбросим все главные изображения для этого товара
        image = await self.get(db, image_id)
        if not image:
            return False

        await db.execute(
            update(ProductsImagesOrm)
            .where(ProductsImagesOrm.product_id == image.product_id)
            .values(is_main=False)
        )

        # Установим новое главное изображение
        result = await db.execute(
            update(ProductsImagesOrm)
            .where(ProductsImagesOrm.id == image_id)
            .values(is_main=True)
        )
        await db.commit()
        return result.rowcount > 0
