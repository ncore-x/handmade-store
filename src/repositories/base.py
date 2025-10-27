from typing import List, Optional, TypeVar, Generic, Type
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int) -> Optional[ModelType]:
        """Получить одну запись по ID"""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """Получить несколько записей с пагинацией"""
        result = await self.session.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create(self, obj_in: dict) -> ModelType:
        """Создать новую запись"""
        db_obj = self.model(**obj_in)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: dict
    ) -> ModelType:
        """Обновить существующую запись"""
        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)

        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: int) -> bool:
        """Удалить запись по ID"""
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def exists(self, id: int) -> bool:
        """Проверить существование записи"""
        result = await self.session.execute(
            select(self.model.id).where(self.model.id == id)
        )
        return result.scalar() is not None
