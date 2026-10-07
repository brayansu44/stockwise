# StockWise - Functional and Non-Functional Requirements

## 1. Functional Requirements

### FR-001: Authentication
The system must allow registered users to log in using email and password.

### FR-002: Role-based access control
The system must restrict access to features based on the user's role.

### FR-003: User management
The system must allow administrators to create, edit, activate and deactivate users.

### FR-004: Category management
The system must allow authorized users to create, edit, list, activate and deactivate product categories.

### FR-005: Product management
The system must allow authorized users to create, edit, list, activate and deactivate products.

### FR-006: Inventory entries
The system must allow inventory entries to increase product stock.

### FR-007: Sales registration
The system must allow users to register sales and automatically decrease product stock.

### FR-008: Stock validation
The system must prevent sales when product stock is insufficient.

### FR-009: Low-stock identification
The system must identify products as low stock when their current stock is less than or equal to their configured minimum stock.

### FR-010: Dashboard
The system must display key business indicators such as total products, low stock products, recent sales and accumulated revenue.

### FR-011: Inventory movements
The system must allow authorized users to register inventory movements and update product stock accordingly.

### FR-012: Inventory movement history
The system must preserve and display the history of registered inventory movements.

### FR-013: Sales history
The system must allow authorized users to list registered sales and consult the details of a specific sale.

### FR-014: Sale cancellation
The system must allow administrators to cancel eligible sales without deleting their historical record.

### FR-015: Stock restoration on sale cancellation
The system must restore the corresponding product stock when a sale is successfully cancelled.

### FR-016: Historical sales consistency
The system must preserve the relevant historical product information associated with registered sales even when product information changes later.

### FR-017: User status enforcement
The system must prevent inactive users from authenticating.

### FR-018: Unique user email
The system must prevent multiple users from being registered with the same email address.

---

## 2. Non-Functional Requirements

### NFR-001: Security
The system must protect endpoints using authentication and authorization mechanisms.

### NFR-002: Maintainability
The backend must follow a modular architecture to make future changes easier.

### NFR-003: Scalability
The system must be designed to evolve from a modular monolith to microservices.

### NFR-004: Performance
The system should respond to common API requests in an acceptable time under normal usage conditions.

### NFR-005: Documentation
The project must include technical documentation, API documentation and architecture decisions.

### NFR-006: Testability
The system must include automated tests for critical business logic.

### NFR-007: Portability
The application should maintain a configuration and architecture that facilitates execution across different development and deployment environments.

Docker-based execution is planned for a future version and is not a requirement of Version 1.0.

### NFR-008: Reliability
The system must handle validation errors and business rule violations consistently.

### NFR-009: Password security
User passwords must be stored using secure password hashing and must never be returned through user management API responses.

### NFR-010: API documentation
The backend API must expose interactive Swagger documentation for available endpoints.

### NFR-011: Data integrity
Operations that modify inventory, sales, users, products or categories must preserve the consistency of persisted business data.

### NFR-012: Automated verification
Critical application, repository and API behavior must be covered by automated tests.
