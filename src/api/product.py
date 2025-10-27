from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse,
    ProductFull,
    ProductImageCreate, ProductImageResponse
)
from src.services.product import ProductService
from src.utils.dependencies import get_db, get_product_service

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    product_service: ProductService = Depends(get_product_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить список товаров"""
    return await product_service.get_multi(db, skip, limit)


@router.get("/available", response_model=List[ProductResponse])
async def get_available_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    product_service: ProductService = Depends(get_product_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить доступные товары (в наличии)"""
    return await product_service.get_available_products(db, skip, limit)


@router.get("/search", response_model=List[ProductResponse])
async def search_products(
    query: str = Query(..., min_length=2),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    product_service: ProductService = Depends(get_product_service),
    db: AsyncSession = Depends(get_db)
):
    """Поиск товаров"""
    try:
        return await product_service.search_products(db, query, skip, limit)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/category/{category_id}", response_model=List[ProductResponse])
async def get_products_by_category(
    category_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    product_service: ProductService = Depends(get_product_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить товары по категории"""
    try:
        return await product_service.get_by_category(db, category_id, skip, limit)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить товар по ID"""
    product = await product_service.get(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.get("/{product_id}/full", response_model=ProductFull)
async def get_product_full(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить товар с категорией и изображениями"""
    product = await product_service.get_with_category_and_images(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.get("/{product_id}/images", response_model=List[ProductImageResponse])
async def get_product_images(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить изображения товара"""
    return await product_service.get_product_images(db, product_id)


# Админские endpoints
@router.post("/", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    product_service: ProductService = Depends(get_product_service),
    db: AsyncSession = Depends(get_db)
):
    """Создать новый товар"""
    try:
        return await product_service.create(db, product_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    product_service: ProductService = Depends(get_product_service),
    db: AsyncSession = Depends(get_db)
):
    """Обновить товар"""
    updated_product = await product_service.update(db, product_id, product_update)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return updated_product


@router.put("/{product_id}/stock")
async def update_product_stock(
    product_id: int,
    new_quantity: int = Query(..., ge=0),
    product_service: ProductService = Depends(get_product_service),
    db: AsyncSession = Depends(get_db)
):
    """Обновить количество товара на складе"""
    try:
        success = await product_service.update_stock(db, product_id, new_quantity)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return {"message": "Stock updated successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
    db: AsyncSession = Depends(get_db)
):
    """Удалить товар"""
    success = await product_service.delete(db, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return {"message": "Product deleted successfully"}


# Работа с изображениями
@router.post("/{product_id}/images", response_model=ProductImageResponse)
async def add_product_image(
    product_id: int,
    image_url: str,  # В реальном приложении загружать файлы
    alt_text: str = None,
    product_service: ProductService = Depends(get_product_service),
    db: AsyncSession = Depends(get_db)
):
    """Добавить изображение к товару"""
    image_data = ProductImageCreate(
        product_id=product_id,
        image_url=image_url,
        alt_text=alt_text
    )

    try:
        return await product_service.add_image(db, image_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/images/{image_id}/set-main")
async def set_main_image(
    image_id: int,
    product_service: ProductService = Depends(get_product_service),
    db: AsyncSession = Depends(get_db)
):
    """Установить изображение как главное"""
    success = await product_service.set_main_image(db, image_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    return {"message": "Image set as main successfully"}
