from sqlalchemy.orm import Session

from app.domain.unit_of_work import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def commit(self) -> None:
        self.db_session.commit()

    def rollback(self) -> None:
        self.db_session.rollback()