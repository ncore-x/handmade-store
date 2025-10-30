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
        result = await db.execute(select(self.model).where(self.model.slug == slug))
        return result.scalar_one_or_none()

    async def get_with_products(self, db: AsyncSession, id: int) -> Optional[CategoriesOrm]:
        result = await db.execute(
            select(self.model)
            .options(selectinload(CategoriesOrm.products))
            .where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_root_categories(self, db: AsyncSession) -> List[CategoriesOrm]:
        result = await db.execute(
            select(self.model)
            .where(self.model.parent_id.is_(None))
            .where(self.model.is_active == True)
            .order_by(self.model.sort_order)
        )
        return result.scalars().all()

    async def get_children(self, db: AsyncSession, parent_id: int) -> List[CategoriesOrm]:
        result = await db.execute(
            select(self.model)
            .where(self.model.parent_id == parent_id)
            .where(self.model.is_active == True)
            .order_by(self.model.sort_order)
        )
        return result.scalars().all()

    async def get_with_children(self, db: AsyncSession, id: int) -> Optional[CategoriesOrm]:
        result = await db.execute(
            select(self.model)
            .options(selectinload(self.model.children))
            .where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_active_categories(self, db: AsyncSession) -> List[CategoriesOrm]:
        result = await db.execute(
            select(self.model)
            .where(self.model.is_active == True)
            .order_by(self.model.sort_order, self.model.name)
        )
        return result.scalars().all()
