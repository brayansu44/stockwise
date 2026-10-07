# StockWise

StockWise is a full-stack inventory and sales management platform designed for small and medium-sized businesses.

The project provides centralized management of products, categories, inventory movements, sales, users, and stock levels while applying modern software engineering practices such as Clean Architecture, REST API design, JWT authentication, role-based authorization, automated testing, and technical documentation.

StockWise is being developed progressively as a professional software engineering portfolio project, starting with a complete Version 1.0 MVP and evolving toward infrastructure, cloud, distributed systems, and applied AI capabilities in future releases.

---

## Features

Version 1.0 includes:

- User authentication with JWT.
- Role-based authorization.
- User management.
- Category management.
- Product management.
- Inventory movement management.
- Inventory movement history.
- Sales registration.
- Automatic stock updates after sales.
- Sales history and detail consultation.
- Sale cancellation with inventory restoration.
- Low-stock identification.
- Operational dashboard.
- Interactive API documentation with Swagger.
- Automated backend testing.
- Technical and functional documentation.

---

## User Roles

StockWise currently supports three roles:

### Administrator

Has access to administrative operations, including user management and sale cancellation.

### Seller

Can work with sales-related functionality according to the permissions defined by the application.

### Inventory Operator

Can work with inventory, products, and categories according to the permissions defined by the application.

Authorization rules are enforced by the backend and complemented by protected frontend routes and interface restrictions.

---

## Technology Stack

### Backend

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- JWT Authentication
- Pytest

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Axios
- React Router

### Development Tools

- Git
- GitHub
- Visual Studio Code

---

## Architecture

The StockWise backend follows Clean Architecture principles and separates responsibilities across different layers.

```text
backend/
└── app/
    ├── domain/
    ├── application/
    ├── infrastructure/
    └── presentation/
```

### Domain

Contains core business entities, rules, and repository abstractions.

### Application

Contains use cases, DTOs, and application-level orchestration.

### Infrastructure

Contains technical implementations such as SQLAlchemy models, repository implementations, database access, and authentication infrastructure.

### Presentation

Contains the FastAPI HTTP layer, routers, dependencies, authentication and authorization integration, and API responses.

This structure keeps business logic separated from frameworks and infrastructure concerns.

---

## Frontend Structure

The frontend is implemented as a React and TypeScript application.

Its responsibilities are organized into areas such as:

```text
frontend/src/
├── components/
├── contexts/
├── layouts/
├── pages/
├── routes/
├── services/
└── types/
```

API communication is centralized in service modules, while authentication state is managed through React context.

---

## Database

StockWise uses PostgreSQL as its relational database and SQLAlchemy as its persistence technology.

The Version 1.0 database contains the following main tables:

- `users`
- `categories`
- `products`
- `inventory_movements`
- `sales`
- `sale_items`

Database schema evolution is managed through Alembic migrations.

The Entity-Relationship design is documented in:

```text
docs/diagrams/database-er-diagram.md
```

---

## Inventory and Sales

Inventory changes are recorded through inventory movements to preserve operational traceability.

When a sale is registered:

1. The requested products and quantities are validated.
2. Available stock is verified.
3. The sale and its items are registered.
4. Product stock is reduced.
5. Related inventory movements are recorded.

When an eligible sale is cancelled by an administrator:

1. The sale remains stored as a historical record.
2. Its status is updated.
3. The corresponding inventory is restored.
4. The inventory changes remain traceable.

---

## Low-Stock Identification

StockWise does not require a separate persistent stock-alert entity in Version 1.0.

A product is considered low stock when:

```text
current_stock <= minimum_stock
```

This allows low-stock information to reflect the current inventory state directly.

---

## Authentication and Security

Version 1.0 includes:

- JWT-based authentication.
- Secure password hashing.
- Protected API endpoints.
- Role-based authorization.
- Inactive-user login prevention.
- Unique user email validation.
- Frontend protected routes.
- Automatic session handling for unauthorized API responses.

Sensitive configuration should be stored through environment variables and must not be committed to the repository.

---

## API Documentation

FastAPI provides interactive Swagger documentation for the backend REST API.

When the backend is running locally, Swagger is available at:

```text
http://localhost:8000/docs
```

The API includes functionality for authentication, users, categories, products, inventory, sales, dashboard information, and stock-related operations.

---

## Testing

The backend uses Pytest for automated verification.

The test suite covers critical behavior across areas such as:

- Application use cases.
- Repository implementations.
- API endpoints.
- Authentication.
- Authorization.
- User management.
- Inventory operations.
- Sales.
- Sale cancellation.
- Historical data consistency.
- Validation and error scenarios.

The project prioritizes automated verification as part of the Version 1.0 engineering foundation.

---

## Project Documentation

Detailed documentation is available in the `docs` directory:

```text
docs/
├── diagrams/
│   └── database-er-diagram.md
├── 00-project-methodology.md
├── 01-project-overview.md
├── 02-business-requirements.md
├── 03-user-stories.md
├── 04-use-cases.md
├── 05-requirements.md
├── 06-database-design.md
├── 07-architecture.md
├── 08-api-documentation.md
├── 09-testing-strategy.md
└── 10-product-roadmap.md
```

The documentation covers:

- Development methodology.
- Project vision and scope.
- Business requirements.
- User stories.
- Use cases.
- Functional and non-functional requirements.
- Database design.
- Entity-Relationship modeling.
- Software architecture.
- REST API reference.
- Testing strategy.
- Product evolution roadmap.

---

## Running the Project

### Prerequisites

Before running StockWise locally, make sure you have:

- Python
- Node.js
- PostgreSQL
- Git

### Backend

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a Python virtual environment and install the backend dependencies according to the project's dependency configuration.

Configure the required environment variables and database connection.

Apply the database migrations:

```bash
alembic upgrade head
```

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

### Frontend

From another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend development server will normally be available at:

```text
http://localhost:5173
```

The frontend API URL can be configured using:

```env
VITE_API_URL=http://localhost:8000
```

---

## Development Status

**Version 1.0 — Minimum Viable Product**

The core Version 1.0 functionality has been implemented.

The current phase focuses on final validation, documentation alignment, and preparing the MVP for formal Version 1.0 closure before beginning Version 2.0 development.

---

## Roadmap

### Version 1.0 — Minimum Viable Product

Focuses on the complete inventory and sales workflow, authentication, authorization, user management, automated testing, and technical documentation.

### Version 2.0 — Professional Engineering

Planned improvements include:

- Audit logging.
- PDF reports.
- Excel export.
- Email notifications.
- External API integration.
- Docker.
- Redis caching.
- CI/CD automation.

### Version 3.0 — Enterprise Architecture

Potential future capabilities include:

- Microservices.
- Event-driven communication.
- Cloud deployment.
- Observability.
- Distributed services.
- AI-powered inventory recommendations.

See the complete roadmap in:

```text
docs/10-product-roadmap.md
```

---

## Project Purpose

StockWise is both a functional software project and a long-term engineering learning platform.

Its objective is to demonstrate practical experience in backend development, frontend integration, relational databases, API design, authentication and authorization, automated testing, software architecture, technical documentation, and progressively more advanced engineering practices.

---

## Author

**Brayan Alexander Suárez Ropero**

Backend-focused Software Developer  
Python · FastAPI · Java · Spring Boot · C# · .NET

GitHub: `brayansu44`