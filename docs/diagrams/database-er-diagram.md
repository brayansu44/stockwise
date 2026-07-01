erDiagram
    ROLE ||--o{ USER : has
    CATEGORY ||--o{ PRODUCT : contains
    USER ||--o{ INVENTORY_MOVEMENT : registers
    PRODUCT ||--o{ INVENTORY_MOVEMENT : has
    USER ||--o{ SALE : registers
    SALE ||--o{ SALE_ITEM : contains
    PRODUCT ||--o{ SALE_ITEM : sold_in
    PRODUCT ||--o{ STOCK_ALERT : generates

    ROLE {
        int id
        string name
        string description
    }

    USER {
        int id
        string full_name
        string email
        string password_hash
        int role_id
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    CATEGORY {
        int id
        string name
        string description
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    PRODUCT {
        int id
        string name
        string code
        string description
        int category_id
        decimal price
        int current_stock
        int minimum_stock
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    INVENTORY_MOVEMENT {
        int id
        int product_id
        int user_id
        string movement_type
        int quantity
        string reason
        datetime created_at
    }

    SALE {
        int id
        int user_id
        decimal total_amount
        datetime created_at
    }

    SALE_ITEM {
        int id
        int sale_id
        int product_id
        int quantity
        decimal unit_price
        decimal subtotal
    }

    STOCK_ALERT {
        int id
        int product_id
        string message
        string status
        datetime created_at
        datetime resolved_at
    }