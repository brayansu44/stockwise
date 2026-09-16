from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from app.presentation.dependencies.database_dependencies import get_db_session


def get_unit_of_work(
    db_session: Session = Depends(get_db_session),
) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(db_session)