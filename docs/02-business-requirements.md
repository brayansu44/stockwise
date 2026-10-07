# StockWise - Business Requirements

## 1. Business Context

StockWise is designed for small and medium-sized businesses (SMBs) that need a centralized platform to manage inventory, sales, and operational information.

Many of these businesses still rely on spreadsheets or manual processes to control stock, making it difficult to maintain accurate inventory records and obtain reliable business insights.

StockWise aims to provide a modern, web-based solution that improves operational efficiency, inventory control, and business visibility.

---

## 2. Business Problem

Small businesses often struggle with inventory management due to manual processes, disconnected tools, and limited operational visibility.

These challenges frequently result in:

- Inventory inaccuracies.
- Stock shortages.
- Duplicate or inconsistent information.
- Operational inefficiencies.
- Limited reporting capabilities.
- Poor traceability of inventory movements and sales.

---

## 3. Stakeholders

### System Administrator

Responsible for managing users, products, categories, inventory, sales, and monitoring key operational information through the dashboard.

### Sales Representative

Responsible for registering sales and consulting product availability.

### Inventory Operator

Responsible for recording inventory entries, stock adjustments, and inventory movements.

---

## 4. Business Needs

The platform must allow users to:

- Manage system users and their access roles.
- Manage products and categories.
- Register inventory entries, exits, and stock adjustments.
- Maintain a historical record of inventory movements.
- Record and consult sales transactions.
- Automatically update inventory levels after inventory and sales operations.
- Cancel eligible sales while preserving their historical information.
- Restore inventory when a sale is cancelled.
- Identify products with low stock.
- Monitor key operational information through a dashboard.
- Control system access through authentication and user roles.
- Maintain traceability of inventory movements and sales.

---

## 5. Business Rules

- Every product must belong to a category.
- Every product must define a minimum stock level.
- A sale must contain at least one valid item.
- A sale cannot be completed if there is insufficient stock.
- Every completed sale must automatically decrease the available inventory.
- Cancelling an eligible sale must restore the corresponding inventory.
- Cancelled sales must remain available as historical records.
- Inventory movements must update product stock according to their movement type.
- Inventory and sales history must be preserved for traceability.
- A product is considered low stock when its current stock is less than or equal to its minimum stock level.
- Only administrators are allowed to manage users.
- User email addresses must be unique.
- Inactive users cannot authenticate.
- Only authenticated users may access protected platform features.
- Access to restricted operations must respect the user's assigned role.

---

## 6. Version 1.0 Scope

The first version of StockWise will include:

- User authentication.
- Role-based access control.
- User management.
- Category management.
- Product management.
- Inventory movement management.
- Inventory movement history.
- Sales registration.
- Sales history and detail consultation.
- Sale cancellation and stock restoration.
- Low-stock identification.
- Operational dashboard.
- REST API documentation using Swagger.
- Automated tests for critical application behavior.

---

## 7. Out of Scope (Version 1.0)

The following features are intentionally excluded from the first release:

- Electronic invoicing integration.
- Payment gateway integration.
- Accounting system integration.
- Multi-warehouse or multi-branch support.
- Mobile application.
- Advanced Artificial Intelligence features.
- Full microservices architecture.
- PDF report generation.
- Excel export.
- Email notifications.
- Exchange rate integration.
- Redis caching.
- Production containerization and deployment automation.