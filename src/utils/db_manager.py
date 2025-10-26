from src.repositories.admin import AdminRepository
from src.repositories.category import CategoryRepository
from src.repositories.product import ProductRepository, ProductImageRepository
from src.repositories.order import OrderRepository, OrderItemRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.admin = AdminRepository(self.session)
        self.category = CategoryRepository(self.session)
        self.product = ProductRepository(self.session)
        self.product_image = ProductImageRepository(self.session)
        self.order = OrderRepository(self.session)
        self.order_item = OrderItemRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
