from dataclasses import dataclass


@dataclass
class DashboardSummary:
    active_products: int
    low_stock_products: int
    completed_sales: int
    total_sales_amount: float