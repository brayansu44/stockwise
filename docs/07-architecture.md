# StockWise - Software Architecture

## 1. Purpose

This document describes the software architecture of StockWise Version 1.0, including the main architectural principles, backend layers, frontend organization, dependency direction, and communication between the main components of the system.

---

## 2. Architecture Overview

StockWise Version 1.0 is implemented as a full-stack web application composed of:

- A React and TypeScript frontend.
- A REST API developed with FastAPI.
- A PostgreSQL relational database.
- SQLAlchemy for persistence.
- Alembic for database migrations.
- JWT-based authentication and role-based authorization.

The backend follows Clean Architecture principles and is implemented as a modular monolith.

```text
┌──────────────────────────┐
│        Frontend          │
│   React + TypeScript     │
└────────────┬─────────────┘
             │
             │ HTTP / REST
             ▼
┌──────────────────────────┐
│      Presentation        │
│        FastAPI           │
├──────────────────────────┤
│       Application        │
│        Use Cases         │
├──────────────────────────┤
│         Domain           │
│ Entities / Abstractions  │
├──────────────────────────┤
│      Infrastructure      │
│ SQLAlchemy / PostgreSQL  │
└──────────────────────────┘
```

---

## 3. Backend Architecture

The backend separates responsibilities into four main areas:

```text
backend/app/
├── domain/
├── application/
├── infrastructure/
└── presentation/
```

### 3.1 Domain Layer

The domain represents the core business concepts of StockWise.

Its responsibility is to define business entities, rules, and abstractions without depending directly on web frameworks, databases, or user-interface technologies.

Examples of business concepts include:

- Users.
- Categories.
- Products.
- Inventory movements.
- Sales.
- Sale items.

Repository abstractions belong to the inner architecture and allow the application to work without depending directly on SQLAlchemy implementations.

---

### 3.2 Application Layer

The application layer coordinates the business operations exposed by the system.

It contains application use cases and the data structures required to execute them.

Examples include operations related to:

- Authentication.
- User management.
- Category management.
- Product management.
- Inventory movements.
- Inventory history.
- Sales registration.
- Sales consultation.
- Sale cancellation.
- Dashboard information.
- Low-stock identification.

Use cases coordinate domain rules and repository abstractions without handling HTTP-specific behavior directly.

---

### 3.3 Infrastructure Layer

The infrastructure layer contains technical implementations required by the application.

Its responsibilities include:

- SQLAlchemy persistence models.
- PostgreSQL database access.
- Repository implementations.
- Database session management.
- Authentication infrastructure.
- Password hashing.
- JWT-related technical functionality.

Alembic manages the evolution of the relational database schema.

---

### 3.4 Presentation Layer

The presentation layer exposes StockWise functionality through FastAPI.

Its responsibilities include:

- REST endpoints.
- Request validation.
- Response serialization.
- Dependency injection integration.
- Authentication dependencies.
- Authorization validation.
- HTTP error handling.

FastAPI also exposes interactive Swagger documentation for the REST API.

---

## 4. Dependency Direction

The architecture is designed so that business rules remain separated from infrastructure concerns.

Conceptually, dependencies should point toward the core application and domain abstractions rather than making business logic depend directly on external technologies.

```text
Presentation ─────┐
                  ▼
             Application
                  │
                  ▼
               Domain
                  ▲
                  │
Infrastructure ───┘
```

Infrastructure implements abstractions required by the inner layers.

This approach improves:

- Maintainability.
- Testability.
- Separation of concerns.
- Technology independence.
- Future extensibility.

---

## 5. Repository Pattern

StockWise uses the Repository Pattern to separate persistence operations from application business logic.

The application depends on repository abstractions, while the infrastructure layer provides SQLAlchemy-based implementations.

Conceptually:

```text
Use Case
   │
   ▼
Repository Interface
   ▲
   │
SQLAlchemy Repository
   │
   ▼
PostgreSQL
```

This separation allows repository behavior and application use cases to be tested independently.

---

## 6. Request Flow

A typical backend request follows this flow:

```text
Frontend
   │
   ▼
FastAPI Endpoint
   │
   ▼
Authentication / Authorization
   │
   ▼
Application Use Case
   │
   ▼
Repository Abstraction
   │
   ▼
Repository Implementation
   │
   ▼
PostgreSQL
```

The result travels back through the corresponding layers until an HTTP response is returned to the frontend.

---

## 7. Frontend Architecture

The frontend is implemented with React and TypeScript.

The source code is organized into areas such as:

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

### Components

Reusable user-interface elements and feature-specific forms.

### Contexts

Shared application state such as authentication information.

### Layouts

Common visual structures used across application pages.

### Pages

Top-level screens associated with application functionality.

### Routes

Route protection and access-control behavior.

### Services

Communication with the backend REST API through Axios.

### Types

TypeScript definitions shared across frontend functionality.

---

## 8. Frontend-to-Backend Communication

The frontend communicates with the backend through HTTP requests to the FastAPI REST API.

```text
React Component / Page
        │
        ▼
Frontend Service
        │
        ▼
Axios API Client
        │
        ▼
FastAPI REST Endpoint
```

The API base URL is configurable through the frontend environment:

```env
VITE_API_URL=http://localhost:8000
```

Authentication requests use the JWT session established after login.

---

## 9. Authentication and Authorization Architecture

StockWise uses JWT-based authentication.

The general authentication flow is:

```text
Credentials
    │
    ▼
Login Endpoint
    │
    ▼
Credential Validation
    │
    ▼
JWT Generation
    │
    ▼
Frontend Session
    │
    ▼
Authenticated API Requests
```

Protected backend operations validate the authenticated user and enforce the required role.

The frontend additionally restricts navigation and protected routes according to the authenticated user's permissions.

Backend authorization remains the authoritative security control.

---

## 10. Persistence Architecture

StockWise Version 1.0 uses:

```text
Application
    │
    ▼
Repository
    │
    ▼
SQLAlchemy
    │
    ▼
PostgreSQL
```

The relational model contains:

- Users.
- Categories.
- Products.
- Inventory movements.
- Sales.
- Sale items.

The complete database design is documented in:

```text
docs/06-database-design.md
```

and:

```text
docs/diagrams/database-er-diagram.md
```

---

## 11. Architectural Decisions

Important Version 1.0 decisions include:

- Use a modular monolith before introducing distributed services.
- Apply Clean Architecture principles to the backend.
- Separate persistence through repository abstractions.
- Use application use cases to coordinate business operations.
- Use PostgreSQL as the relational persistence layer.
- Use JWT for stateless API authentication.
- Store user roles directly with the user.
- Calculate low-stock state from current inventory instead of persisting a separate alert entity.
- Preserve cancelled sales instead of deleting historical records.
- Preserve sale item pricing for historical consistency.
- Use database migrations for controlled schema evolution.
- Maintain automated tests as part of the architecture.

---

## 12. Version 1.0 Architectural Scope

Version 1.0 intentionally focuses on a well-structured modular application.

The following architectural capabilities are planned for later versions and are not part of the current MVP:

- Docker-based environments.
- Redis caching.
- CI/CD pipelines.
- Cloud deployment.
- Microservices.
- Message brokers.
- Event-driven architecture.
- Distributed observability.
- AI services.

These capabilities will be introduced progressively only when the project's complexity justifies them.

---

## 13. Architecture Evolution

StockWise is designed to evolve progressively:

```text
Version 1.0
Modular Monolith
      │
      ▼
Version 2.0
Infrastructure and Automation
      │
      ▼
Version 3.0
Distributed / Cloud Architecture
```

This strategy avoids unnecessary complexity during the MVP while maintaining a foundation suitable for future architectural growth.