from src.repositories.mappers.base import DataMapper
from src.models.admin import AdminsOrm
from src.models.category import CategoriesOrm
from src.models.order import OrdersOrm
from src.models.product import ProductsOrm
from src.schemas.admin import Admin
from src.schemas.category import CategoryBase
from src.schemas.order import OrderBase
from src.schemas.product import ProductBase


class AdminDataMapper(DataMapper):
    db_model = AdminsOrm
    schema = Admin


class CategoryDataMapper(DataMapper):
    db_model = CategoriesOrm
    schema = CategoryBase


class ProductDataMapper(DataMapper):
    db_model = ProductsOrm
    schema = ProductBase


class OrderDataMapper(DataMapper):
    db_model = OrdersOrm
    schema = OrderBase
