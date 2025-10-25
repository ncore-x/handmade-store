from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.categories import (
    CategoryCreate, CategoryUpdate, CategoryResponse,
    CategoryWithProducts, CategoryWithChildren
)
from src.services.categories import CategoryService
from src.utils.dependencies import get_db, get_category_service, require_admin

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category_service: CategoryService = Depends(get_category_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить список категорий"""
    return await category_service.get_multi(db, skip, limit)


@router.get("/active", response_model=List[CategoryResponse])
async def get_active_categories(
    category_service: CategoryService = Depends(get_category_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить активные категории"""
    return await category_service.get_active_categories(db)


@router.get("/root", response_model=List[CategoryResponse])
async def get_root_categories(
    category_service: CategoryService = Depends(get_category_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить корневые категории"""
    return await category_service.get_root_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить категорию по ID"""
    category = await category_service.get(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@router.get("/{category_id}/with-products", response_model=CategoryWithProducts)
async def get_category_with_products(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить категорию с товарами"""
    category = await category_service.get_with_products(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@router.get("/{category_id}/with-children", response_model=CategoryWithChildren)
async def get_category_with_children(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить категорию с дочерними категориями"""
    category = await category_service.get_with_children(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@router.get("/slug/{slug}", response_model=CategoryResponse)
async def get_category_by_slug(
    slug: str,
    category_service: CategoryService = Depends(get_category_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить категорию по slug"""
    category = await category_service.get_by_slug(db, slug)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category


@router.get("/{parent_id}/children", response_model=List[CategoryResponse])
async def get_category_children(
    parent_id: int,
    category_service: CategoryService = Depends(get_category_service),
    db: AsyncSession = Depends(get_db)
):
    """Получить дочерние категории"""
    return await category_service.get_children(db, parent_id)


# Админские endpoints
@router.post("/", response_model=CategoryResponse)
async def create_category(
    category_data: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service),
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin)
):
    """Создать новую категорию"""
    try:
        return await category_service.create(db, category_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    category_service: CategoryService = Depends(get_category_service),
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin)
):
    """Обновить категорию"""
    updated_category = await category_service.update(db, category_id, category_update)
    if not updated_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return updated_category


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin)
):
    """Удалить категорию"""
    success = await category_service.delete(db, category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return {"message": "Category deleted successfully"}
