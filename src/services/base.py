from typing import TypeVar, Generic, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db_manager import DBManager

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
ResponseSchemaType = TypeVar("ResponseSchemaType")


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
    db: DBManager | None

    def __init__(self, db: DBManager | None = None) -> None:
        self.db = db

    async def get(self, db: AsyncSession, id: int) -> Optional[ResponseSchemaType]:
        """Получить одну запись"""
        db_obj = await self.repository.get(db, id)
        if db_obj:
            return ResponseSchemaType.model_validate(db_obj)
        return None

    async def get_multi(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[ResponseSchemaType]:
        """Получить несколько записей"""
        db_objs = await self.repository.get_multi(db, skip, limit)
        return [ResponseSchemaType.model_validate(obj) for obj in db_objs]

    async def create(
        self,
        db: AsyncSession,
        obj_in: CreateSchemaType
    ) -> ResponseSchemaType:
        """Создать новую запись"""
        obj_data = obj_in.model_dump()
        db_obj = await self.repository.create(db, obj_data)
        return ResponseSchemaType.model_validate(db_obj)

    async def update(
        self,
        db: AsyncSession,
        id: int,
        obj_in: UpdateSchemaType
    ) -> Optional[ResponseSchemaType]:
        """Обновить существующую запись"""
        db_obj = await self.repository.get(db, id)
        if not db_obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        updated_obj = await self.repository.update(db, db_obj, update_data)
        return ResponseSchemaType.model_validate(updated_obj)

    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Удалить запись"""
        return await self.repository.delete(db, id)
