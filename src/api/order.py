from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.order import (
    OrderCreate, OrderUpdate, OrderResponse, OrderWithItems, OrderFull,
    OrderStatusUpdate, PaymentStatusUpdate, OrderStats
)
from src.services.order import OrderService
from src.utils.dependencies import get_db, get_order_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderWithItems)
async def create_order(
    order_data: OrderCreate,
    order_service: OrderService = Depends(get_order_service),
    db: AsyncSession = Depends(get_db)
):
    """Создать новый заказ"""
    try:
        return await order_service.create(db, order_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    order_service: OrderService = Depends(get_order_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить список заказов (только для администраторов)"""
    return await order_service.get_multi(db, skip, limit)


@router.get("/customer/{email}", response_model=List[OrderResponse])
async def get_customer_orders(
    email: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    order_service: OrderService = Depends(get_order_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить заказы по email клиента"""
    return await order_service.get_by_customer_email(db, email, skip, limit)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    order_service: OrderService = Depends(get_order_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить заказ по ID"""
    order = await order_service.get(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order


@router.get("/{order_id}/full", response_model=OrderFull)
async def get_order_full(
    order_id: int,
    order_service: OrderService = Depends(get_order_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить заказ с позициями и товарами (только для администраторов)"""
    order = await order_service.get_with_items_and_products(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order


@router.get("/status/{status}", response_model=List[OrderResponse])
async def get_orders_by_status(
    status: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    order_service: OrderService = Depends(get_order_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить заказы по статусу (только для администраторов)"""
    try:
        return await order_service.get_by_status(db, status, skip, limit)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    order_service: OrderService = Depends(get_order_service),
    db: AsyncSession = Depends(get_db)
):
    """Обновить статус заказа"""
    try:
        success = await order_service.update_status(db, order_id, status_update.status)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return await order_service.get(db, order_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{order_id}/payment-status", response_model=OrderResponse)
async def update_payment_status(
    order_id: int,
    payment_update: PaymentStatusUpdate,
    order_service: OrderService = Depends(get_order_service),
    db: AsyncSession = Depends(get_db)
):
    """Обновить статус оплаты"""
    try:
        success = await order_service.update_payment_status(
            db, order_id, payment_update.payment_status, payment_update.payment_id
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return await order_service.get(db, order_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    order_service: OrderService = Depends(get_order_service),
    db: AsyncSession = Depends(get_db)
):
    """Обновить заказ"""
    updated_order = await order_service.update(db, order_id, order_update)
    if not updated_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return updated_order


@router.get("/admin/stats", response_model=OrderStats)
async def get_order_stats(
    order_service: OrderService = Depends(get_order_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить статистику по заказам (только для администраторов)"""
    return await order_service.get_order_stats(db)
