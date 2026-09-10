from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    SELLER = "seller"
    INVENTORY_OPERATOR = "inventory_operator"