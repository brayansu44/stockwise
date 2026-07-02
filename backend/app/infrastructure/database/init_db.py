from app.infrastructure.database.database import Base, engine
from app.infrastructure.database.models.product_model import ProductModel


def init_db() -> None:
    Base.metadata.create_all(bind=engine)