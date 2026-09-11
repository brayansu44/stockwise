from app.domain.entities.sale import Sale
from app.domain.repositories.sale_repository import SaleRepository


class GetSaleByIdUseCase:
    def __init__(
        self,
        sale_repository: SaleRepository,
    ):
        self.sale_repository = sale_repository

    def execute(
        self,
        sale_id: int,
    ) -> Sale:
        if sale_id <= 0:
            raise ValueError("Sale ID must be greater than zero")

        sale = self.sale_repository.get_by_id(sale_id)

        if not sale:
            raise ValueError("Sale not found")

        return sale