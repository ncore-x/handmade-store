from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now())
