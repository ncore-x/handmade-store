from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.dependencies import get_db, get_admin_service, require_admin
from src.schemas.admin import AdminCreate, AdminUpdate, AdminResponse, AdminLogin, Token
from src.services.admin import AdminService


router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/register", response_model=AdminResponse)
async def admin_register(
    admin_data: AdminCreate,
    admin_service: AdminService = Depends(get_admin_service),
    db: AsyncSession = Depends(get_db),
    get_current_admin: AdminResponse = Depends(require_admin)
):
    """Создание нового администратора (требует аутентификации)"""
    try:
        return await admin_service.create(db, admin_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
async def admin_login(
    login_data: AdminLogin,
    admin_service: AdminService = Depends(get_admin_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Аутентификация администратора.
    Временная реализация - в продакшене заменить на JWT.
    """
    admin = await admin_service.authenticate(db, login_data)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # Временный токен (в реальном приложении генерировать JWT)
    return Token(access_token="admin-token", token_type="bearer")


@router.get("/me", response_model=AdminResponse)
async def get_current_admin_info(
    current_admin: AdminResponse = Depends(require_admin)
):
    """Получить информацию о текущем администраторе"""
    return current_admin


@router.put("/me", response_model=AdminResponse)
async def update_current_admin(
    admin_update: AdminUpdate,
    admin_service: AdminService = Depends(get_admin_service),
    db: AsyncSession = Depends(get_db),
    current_admin: AdminResponse = Depends(require_admin)
):
    """Обновить информацию текущего администратора"""
    updated_admin = await admin_service.update(db, current_admin.id, admin_update)
    if not updated_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )
    return updated_admin
