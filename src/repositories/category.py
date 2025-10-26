from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.repositories.base import BaseRepository
from src.models.category import CategoriesOrm


class CategoryRepository(BaseRepository[CategoriesOrm]):
    def __init__(self):
        super().__init__(CategoriesOrm)

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[CategoriesOrm]:
        """Найти категорию по slug"""
        result = await db.execute(
            select(CategoriesOrm).where(CategoriesOrm.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_with_products(self, db: AsyncSession, id: int) -> Optional[CategoriesOrm]:
        """Получить категорию с товарами"""
        result = await db.execute(
            select(CategoriesOrm)
            .options(selectinload(CategoriesOrm.products))
            .where(CategoriesOrm.id == id)
        )
        return result.scalar_one_or_none()

    async def get_root_categories(self, db: AsyncSession) -> List[CategoriesOrm]:
        """Получить корневые категории (без parent_id)"""
        result = await db.execute(
            select(CategoriesOrm)
            .where(CategoriesOrm.parent_id.is_(None))
            .where(CategoriesOrm.is_active == True)
            .order_by(CategoriesOrm.sort_order)
        )
        return result.scalars().all()

    async def get_children(self, db: AsyncSession, parent_id: int) -> List[CategoriesOrm]:
        """Получить дочерние категории"""
        result = await db.execute(
            select(CategoriesOrm)
            .where(CategoriesOrm.parent_id == parent_id)
            .where(CategoriesOrm.is_active == True)
            .order_by(CategoriesOrm.sort_order)
        )
        return result.scalars().all()

    async def get_with_children(self, db: AsyncSession, id: int) -> Optional[CategoriesOrm]:
        """Получить категорию с дочерними категориями"""
        result = await db.execute(
            select(CategoriesOrm)
            .options(selectinload(CategoriesOrm.children))
            .where(CategoriesOrm.id == id)
        )
        return result.scalar_one_or_none()

    async def get_active_categories(self, db: AsyncSession) -> List[CategoriesOrm]:
        """Получить все активные категории"""
        result = await db.execute(
            select(CategoriesOrm)
            .where(CategoriesOrm.is_active == True)
            .order_by(CategoriesOrm.sort_order, CategoriesOrm.name)
        )
        return result.scalars().all()
