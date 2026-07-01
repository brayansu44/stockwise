# StockWise - Functional and Non-Functional Requirements

## 1. Functional Requirements

### FR-001: Authentication
The system must allow registered users to log in using email and password.

### FR-002: Role-based access control
The system must restrict access to features based on the user's role.

### FR-003: User management
The system must allow administrators to create, edit, activate and deactivate users.

### FR-004: Category management
The system must allow authorized users to create, edit, list and deactivate product categories.

### FR-005: Product management
The system must allow authorized users to create, edit, list and deactivate products.

### FR-006: Inventory entries
The system must allow inventory entries to increase product stock.

### FR-007: Sales registration
The system must allow users to register sales and automatically decrease product stock.

### FR-008: Stock validation
The system must prevent sales when product stock is insufficient.

### FR-009: Stock alerts
The system must generate alerts when product stock is less than or equal to the minimum stock.

### FR-010: Dashboard
The system must display key business indicators such as total products, low stock products, recent sales and accumulated revenue.

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
The system should be executable locally using Docker in future versions.

### NFR-008: Reliability
The system must handle validation errors and business rule violations consistently.