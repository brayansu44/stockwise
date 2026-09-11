from abc import ABC, abstractmethod

from app.domain.entities.sale import Sale


class SaleRepository(ABC):
    @abstractmethod
    def create(
        self,
        sale: Sale,
    ) -> Sale:
        pass

    @abstractmethod
    def create_without_commit(
        self,
        sale: Sale,
    ) -> Sale:
        pass

    @abstractmethod
    def get_by_id(
        self,
        sale_id: int,
    ) -> Sale | None:
        pass

    @abstractmethod
    def list_all(self) -> list[Sale]:
        pass
    
    @abstractmethod
    def commit(self) -> None:
        pass