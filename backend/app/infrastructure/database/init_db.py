from app.infrastructure.database.database import Base, engine

# Register all SQLAlchemy models
import app.infrastructure.database.models


def init_db() -> None:
    Base.metadata.create_all(bind=engine)