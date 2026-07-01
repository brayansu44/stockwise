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

Responsible for configuring the platform, managing users, products, categories, inventory, and accessing business reports.

### Sales Representative

Responsible for registering sales and consulting product availability.

### Inventory Operator

Responsible for recording inventory entries, stock adjustments, and inventory movements.

---

## 4. Business Needs

The platform must allow users to:

- Manage products and categories.
- Register inventory entries and stock adjustments.
- Record sales transactions.
- Automatically update inventory levels.
- Generate low-stock alerts.
- Access operational reports.
- Control system access through user roles.
- Maintain complete traceability of inventory operations.

---

## 5. Business Rules

- Every product must belong to a category.
- Every product must define a minimum stock level.
- A sale cannot be completed if there is insufficient stock.
- Every completed sale must automatically decrease the available inventory.
- Every inventory entry must increase the available stock.
- The system must generate a low-stock alert whenever the current stock is less than or equal to the minimum stock.
- Only administrators are allowed to manage users.
- Only authenticated users may access the platform.

---

## 6. Version 1.0 Scope

The first version of StockWise will include:

- User authentication.
- Role-based access control.
- Category management.
- Product management.
- Inventory entry management.
- Sales registration.
- Low-stock alerts.
- Operational dashboard.
- REST API documentation using Swagger.

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