from typing import List, Optional, Dict, Any
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.order import OrdersOrm, OrdersItemsOrm
from src.repositories.base import BaseRepository


class OrderRepository(BaseRepository[OrdersOrm]):
    def __init__(self, session: AsyncSession):
        super().__init__(OrdersOrm, session)

    async def get_with_items(self, db: AsyncSession, id: int) -> Optional[OrdersOrm]:
        """Получить заказ с позициями"""
        result = await db.execute(
            select(OrdersOrm)
            .options(selectinload(OrdersOrm.items))
            .where(OrdersOrm.id == id)
        )
        return result.scalar_one_or_none()

    async def get_with_items_and_products(self, db: AsyncSession, id: int) -> Optional[OrdersOrm]:
        """Получить заказ с позициями и товарами"""
        result = await db.execute(
            select(OrdersOrm)
            .options(selectinload(OrdersOrm.items).selectinload(OrdersItemsOrm.product))
            .where(OrdersOrm.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_customer_email(
        self,
        db: AsyncSession,
        email: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[OrdersOrm]:
        result = await db.execute(
            select(OrdersOrm)
            .where(OrdersOrm.customer_email == email)
            .order_by(OrdersOrm.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_status(
        self,
        db: AsyncSession,
        status: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[OrdersOrm]:
        result = await db.execute(
            select(OrdersOrm)
            .where(OrdersOrm.status == status)
            .order_by(OrdersOrm.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def update_status(self, db: AsyncSession, order_id: int, status: str) -> bool:
        """Обновить статус заказа"""
        result = await db.execute(
            update(OrdersOrm)
            .where(OrdersOrm.id == order_id)
            .values(status=status)
        )
        await db.commit()
        return result.rowcount > 0

    async def update_payment_status(
        self,
        db: AsyncSession,
        order_id: int,
        payment_status: str,
        payment_id: Optional[str] = None
    ) -> bool:
        """Обновить статус оплаты"""
        values = {"payment_status": payment_status}
        if payment_id:
            values["payment_id"] = payment_id

        result = await db.execute(
            update(OrdersOrm)
            .where(OrdersOrm.id == order_id)
            .values(**values)
        )
        await db.commit()
        return result.rowcount > 0

    async def get_order_stats(self, db: AsyncSession) -> Dict[str, Any]:
        """Получить статистику по заказам"""
        total_orders = (await db.execute(select(func.count(OrdersOrm.id)))).scalar() or 0
        pending_orders = (await db.execute(select(func.count(OrdersOrm.id)).where(OrdersOrm.status == "pending"))).scalar() or 0
        completed_orders = (await db.execute(select(func.count(OrdersOrm.id)).where(OrdersOrm.status == "completed"))).scalar() or 0
        total_revenue = (await db.execute(
            select(func.coalesce(func.sum(OrdersOrm.total_amount), 0))
            .where(OrdersOrm.payment_status == "paid")
        )).scalar() or 0

        return {
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "completed_orders": completed_orders,
            "total_revenue": total_revenue
        }


class OrderItemRepository(BaseRepository[OrdersItemsOrm]):
    def __init__(self, session: AsyncSession):
        super().__init__(OrdersItemsOrm, session)

    async def get_by_order(self, db: AsyncSession, order_id: int) -> List[OrdersItemsOrm]:
        """Получить позиции заказа"""
        result = await db.execute(
            select(OrdersItemsOrm)
            .where(OrdersItemsOrm.order_id == order_id)
        )
        return result.scalars().all()

    async def get_by_product(self, db: AsyncSession, product_id: int) -> List[OrdersItemsOrm]:
        """Получить позиции заказа по товару"""
        result = await db.execute(
            select(OrdersItemsOrm)
            .where(OrdersItemsOrm.product_id == product_id)
        )
        return result.scalars().all()
