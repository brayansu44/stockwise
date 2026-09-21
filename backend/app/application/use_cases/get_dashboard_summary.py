from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.sale_repository import SaleRepository
from app.application.dto.dashboard_dto import DashboardSummary
from app.domain.entities.sale_status import SaleStatus

class GetDashboardSummaryUseCase:
    def __init__(
        self,
        product_repository: ProductRepository,
        sale_repository: SaleRepository,
    ):
        self.product_repository = product_repository
        self.sale_repository = sale_repository
        
    def execute(self) -> DashboardSummary:
        products = self.product_repository.list_all()

        active_products = sum(
            1
            for product in products
            if product.is_active
        )
        
        low_stock_products = sum(
            1
            for product in products
            if product.is_active and product.is_low_stock()
        )
        
        sales = self.sale_repository.list_all()

        completed_sales = sum(
            1
            for sale in sales
            if sale.status == SaleStatus.COMPLETED
        )
        
        total_sales_amount = sum(
            sale.total
            for sale in sales
            if sale.status == SaleStatus.COMPLETED
        )

        return DashboardSummary(
            active_products=active_products,
            low_stock_products=low_stock_products,
            completed_sales=completed_sales,
            total_sales_amount=total_sales_amount,
        )