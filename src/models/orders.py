from src.models.base import BaseModel


class OrdersOrm(BaseModel):
    __tablename__ = "orders"


class OrdersItemsOrm(BaseModel):
    __tablename__ = "orders_items"
