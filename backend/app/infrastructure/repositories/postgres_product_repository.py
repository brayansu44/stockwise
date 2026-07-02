from decimal import Decimal

from sqlalchemy.orm import Session

from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.database.models.product_model import ProductModel


class PostgresProductRepository(ProductRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, product: Product) -> Product:
        product_model = ProductModel(
            name=product.name,
            code=product.code,
            description=product.description,
            price=Decimal(str(product.price)),
            current_stock=product.current_stock,
            minimum_stock=product.minimum_stock,
            is_active=product.is_active,
        )

        self.db_session.add(product_model)
        self.db_session.commit()
        self.db_session.refresh(product_model)

        return self._to_entity(product_model)

    def get_by_code(self, code: str) -> Product | None:
        product_model = (
            self.db_session.query(ProductModel)
            .filter(ProductModel.code == code)
            .first()
        )

        if not product_model:
            return None

        return self._to_entity(product_model)

    def list_all(self) -> list[Product]:
        products = self.db_session.query(ProductModel).all()

        return [self._to_entity(product) for product in products]

    def _to_entity(self, product_model: ProductModel) -> Product:
        return Product(
            id=product_model.id,
            name=product_model.name,
            code=product_model.code,
            description=product_model.description,
            price=float(product_model.price),
            current_stock=product_model.current_stock,
            minimum_stock=product_model.minimum_stock,
            is_active=product_model.is_active,
        )