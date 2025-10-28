from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.category import CategoryRepository
from src.schemas.category import (
    CategoryCreate, CategoryResponse,
    CategoryWithChildren, CategoryWithProducts
)
from src.services.base import BaseService


class CategoryService(BaseService):
    def __init__(self):
        super().__init__(CategoryRepository())

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[CategoryResponse]:
        """Получить категорию по slug"""
        category = await self.repository.get_by_slug(db, slug)
        if category:
            return CategoryResponse.model_validate(category)
        return None

    async def get_with_products(self, db: AsyncSession, id: int) -> Optional[CategoryWithProducts]:
        """Получить категорию с товарами"""
        category = await self.repository.get_with_products(db, id)
        if category:
            return CategoryWithProducts.model_validate(category)
        return None

    async def get_with_children(self, db: AsyncSession, id: int) -> Optional[CategoryWithChildren]:
        """Получить категорию с дочерними категориями"""
        category = await self.repository.get_with_children(db, id)
        if category:
            category_data = CategoryWithChildren.model_validate(category)
            category_data.products_count = len(
                category.products) if category.products else 0
            return category_data
        return None

    async def get_root_categories(self, db: AsyncSession) -> List[CategoryResponse]:
        """Получить корневые категории"""
        categories = await self.repository.get_root_categories(db)
        return [CategoryResponse.model_validate(cat) for cat in categories]

    async def get_children(self, db: AsyncSession, parent_id: int) -> List[CategoryResponse]:
        """Получить дочерние категории"""
        categories = await self.repository.get_children(db, parent_id)
        return [CategoryResponse.model_validate(cat) for cat in categories]

    async def get_active_categories(self, db: AsyncSession) -> List[CategoryResponse]:
        """Получить все активные категории"""
        categories = await self.repository.get_active_categories(db)
        return [CategoryResponse.model_validate(cat) for cat in categories]

    async def create(self, db: AsyncSession, obj_in: CategoryCreate) -> CategoryResponse:
        """Создать категорию с проверкой уникальности slug"""
        existing = await self.repository.get_by_slug(db, obj_in.slug)
        if existing:
            raise ValueError(
                f"Category with slug '{obj_in.slug}' already exists")

        return await super().create(db, obj_in)
