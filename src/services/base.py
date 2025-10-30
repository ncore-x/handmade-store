from typing import TypeVar, Generic, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
ResponseSchemaType = TypeVar("ResponseSchemaType")


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
    repository: any

    def __init__(self, repository):
        self.repository = repository

    async def get(self, db: AsyncSession, id: int) -> Optional[ResponseSchemaType]:
        db_obj = await self.repository.get(db, id)
        if db_obj:
            return ResponseSchemaType.model_validate(db_obj)
        return None

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ResponseSchemaType]:
        db_objs = await self.repository.get_multi(db, skip, limit)
        return [ResponseSchemaType.model_validate(obj) for obj in db_objs]

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ResponseSchemaType:
        obj_data = obj_in.model_dump()
        db_obj = await self.repository.create(db, obj_data)
        return ResponseSchemaType.model_validate(db_obj)

    async def update(self, db: AsyncSession, id: int, obj_in: UpdateSchemaType) -> Optional[ResponseSchemaType]:
        db_obj = await self.repository.get(db, id)
        if not db_obj:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)
        updated_obj = await self.repository.update(db, db_obj, update_data)
        return ResponseSchemaType.model_validate(updated_obj)

    async def delete(self, db: AsyncSession, id: int) -> bool:
        return await self.repository.delete(db, id)
