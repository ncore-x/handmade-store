from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.orders import OrderRepository, OrderItemRepository
from src.repositories.products import ProductRepository
from src.schemas.orders import (
    OrderCreate, OrderUpdate, OrderResponse, OrderWithItems, OrderFull,
    OrderItemCreate, OrderItemResponse, OrderStats
)
from src.services.base import BaseService


class OrderService(BaseService):
    def __init__(self):
        super().__init__(OrderRepository())
        self.item_repo = OrderItemRepository()
        self.product_repo = ProductRepository()

    async def get_with_items(self, db: AsyncSession, id: int) -> Optional[OrderWithItems]:
        """Получить заказ с позициями"""
        order = await self.repository.get_with_items(db, id)
        if order:
            return OrderWithItems.model_validate(order)
        return None

    async def get_with_items_and_products(self, db: AsyncSession, id: int) -> Optional[OrderFull]:
        """Получить заказ с позициями и товарами"""
        order = await self.repository.get_with_items_and_products(db, id)
        if order:
            return OrderFull.model_validate(order)
        return None

    async def get_by_customer_email(
        self,
        db: AsyncSession,
        email: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[OrderResponse]:
        """Получить заказы по email клиента"""
        orders = await self.repository.get_by_customer_email(db, email, skip, limit)
        return [OrderResponse.model_validate(order) for order in orders]

    async def get_by_status(
        self,
        db: AsyncSession,
        status: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[OrderResponse]:
        """Получить заказы по статусу"""
        valid_statuses = ["pending", "processing",
                          "shipped", "delivered", "cancelled"]
        if status not in valid_statuses:
            raise ValueError(
                f"Invalid status. Must be one of: {valid_statuses}")

        orders = await self.repository.get_by_status(db, status, skip, limit)
        return [OrderResponse.model_validate(order) for order in orders]

    async def create(self, db: AsyncSession, obj_in: OrderCreate) -> OrderResponse:
        """Создать заказ с валидацией и расчетами"""
        # Валидация товаров и расчет стоимости
        subtotal = 0
        order_items_data = []

        for item in obj_in.items:
            # Проверяем существование товара
            product = await self.product_repo.get(db, item.product_id)
            if not product:
                raise ValueError(
                    f"Product with id {item.product_id} not found")

            if not product.in_stock:
                raise ValueError(f"Product {product.name} is out of stock")

            if item.quantity > product.stock_quantity:
                raise ValueError(
                    f"Not enough stock for {product.name}. Available: {product.stock_quantity}")

            # Сохраняем данные товара на момент заказа
            item_data = item.model_dump()
            item_data["product_name"] = product.name
            item_data["product_price"] = product.price

            order_items_data.append(item_data)
            subtotal += product.price * item.quantity

        # Генерируем номер заказа
        from datetime import datetime
        order_number = f"ORD-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

        # Расчет итоговой суммы (можно добавить логику доставки)
        shipping_cost = 0  # В реальном приложении рассчитывается по адресу
        total_amount = subtotal + shipping_cost

        # Создаем заказ
        order_data = obj_in.model_dump(exclude={"items"})
        order_data.update({
            "order_number": order_number,
            "subtotal": subtotal,
            "shipping_cost": shipping_cost,
            "total_amount": total_amount,
            "status": "pending",
            "payment_status": "pending"
        })

        order = await self.repository.create(db, order_data)

        # Создаем позиции заказа
        for item_data in order_items_data:
            item_data["order_id"] = order.id
            await self.item_repo.create(db, item_data)

            # Обновляем остатки товара
            await self.product_repo.update_stock(
                db,
                item_data["product_id"],
                product.stock_quantity - item_data["quantity"]
            )

        return await self.get_with_items(db, order.id)

    async def update_status(
        self,
        db: AsyncSession,
        order_id: int,
        status: str
    ) -> bool:
        """Обновить статус заказа"""
        valid_statuses = ["pending", "processing",
                          "shipped", "delivered", "cancelled"]
        if status not in valid_statuses:
            raise ValueError(
                f"Invalid status. Must be one of: {valid_statuses}")

        return await self.repository.update_status(db, order_id, status)

    async def update_payment_status(
        self,
        db: AsyncSession,
        order_id: int,
        payment_status: str,
        payment_id: Optional[str] = None
    ) -> bool:
        """Обновить статус оплаты"""
        valid_statuses = ["pending", "paid", "failed", "refunded"]
        if payment_status not in valid_statuses:
            raise ValueError(
                f"Invalid payment status. Must be one of: {valid_statuses}")

        return await self.repository.update_payment_status(db, order_id, payment_status, payment_id)

    async def get_order_stats(self, db: AsyncSession) -> OrderStats:
        """Получить статистику по заказам"""
        stats = await self.repository.get_order_stats(db)
        return OrderStats(**stats)


class OrderItemService(BaseService):
    def __init__(self):
        super().__init__(OrderItemRepository())
