from app.domain.entities.sale import Sale
from app.domain.repositories.sale_repository import SaleRepository


class ListSalesUseCase:
    def __init__(
        self,
        sale_repository: SaleRepository,
    ):
        self.sale_repository = sale_repository

    def execute(self) -> list[Sale]:
        return self.sale_repository.list_all()