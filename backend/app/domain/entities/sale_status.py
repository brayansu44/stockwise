from enum import Enum


class SaleStatus(str, Enum):
    COMPLETED = "completed"
    CANCELLED = "cancelled"