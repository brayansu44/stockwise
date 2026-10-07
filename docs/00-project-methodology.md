# StockWise Development Methodology

## 1. Purpose

This document defines the development standards, engineering practices, documentation guidelines, and workflow used throughout the StockWise project.

Its purpose is to ensure consistency, maintainability, and high-quality software development by establishing a single source of truth for every technical and organizational decision made during the project lifecycle.

All contributors must follow the standards described in this document.

---

## 2. Project Philosophy

StockWise is built around the following engineering principles:

### 2.1 Understand Before Implementing

Every technology, architectural decision, and design pattern must be understood before it is implemented.

Copying code without understanding its purpose is not acceptable.

---

### 2.2 Documentation Is Part of the Product

Documentation is considered a core deliverable of the project, not an optional task.

Every major feature must include the corresponding technical documentation.

---

### 2.3 Quality Over Speed

Building high-quality software is more important than delivering features quickly.

Clean architecture, readability, and maintainability always take priority.

---

### 2.4 Learn Through Practice

The objective of StockWise is not only to build a software product but also to strengthen professional software engineering skills through real-world practices.

---

### 2.5 Every Decision Must Have a Reason

Architectural and technical decisions should always be justified.

Whenever appropriate, important decisions will be documented using Architecture Decision Records (ADR).

---

## 3. Development Approach

StockWise follows an incremental and feature-oriented development approach.

Features are implemented progressively, prioritizing a functional and stable Version 1.0 before introducing infrastructure or architectural complexity planned for future releases.

The general development cycle for a feature is:

1. Define the business requirement.
2. Identify the corresponding user story or use case.
3. Define or update domain entities and business rules.
4. Implement the application use case.
5. Implement persistence and infrastructure components when required.
6. Expose the functionality through the REST API.
7. Add or update automated tests.
8. Validate the feature manually when appropriate.
9. Implement or integrate the frontend functionality.
10. Update the corresponding documentation.
11. Commit and push the completed change using Git.

A feature should be considered complete only when its implementation, validation, and relevant documentation are consistent.

---

## 4. Architecture Guidelines

The StockWise backend follows Clean Architecture principles and separates responsibilities into different layers.

### Domain

Contains core business entities, rules, and abstractions that should remain independent from frameworks and infrastructure concerns.

### Application

Contains application use cases, DTOs, and orchestration of business operations.

### Infrastructure

Contains technical implementations such as:

- SQLAlchemy database models.
- Repository implementations.
- PostgreSQL persistence.
- Authentication infrastructure.
- External technical dependencies.

### Presentation

Contains the FastAPI HTTP layer, including:

- Routers.
- Request handling.
- Dependency injection.
- Authentication and authorization dependencies.
- API responses.

Dependencies should point toward the core of the application whenever possible.

Business rules should not depend directly on FastAPI, SQLAlchemy, or frontend technologies.

---

## 5. Backend Development Standards

Backend development should follow these guidelines:

- Keep business logic outside API routers whenever possible.
- Use application use cases to coordinate business operations.
- Access persisted data through repository abstractions.
- Use DTOs or schemas to define application and API data contracts.
- Validate business rules before persisting state changes.
- Use dependency injection for repositories, authentication, and application services.
- Use SQLAlchemy for persistence.
- Use Alembic migrations for database schema changes.
- Use appropriate HTTP status codes and consistent error responses.
- Protect restricted endpoints using authentication and role-based authorization.

---

## 6. Frontend Development Standards

The StockWise frontend is implemented using React and TypeScript.

Frontend development should follow these guidelines:

- Organize responsibilities between pages, reusable components, services, contexts, routes, and types.
- Keep HTTP communication inside service modules.
- Use TypeScript types for application data contracts.
- Use the authentication context to manage the current session and authenticated user.
- Protect application routes according to authentication and authorization requirements.
- Provide clear loading, validation, success, and error states.
- Keep the interface consistent across modules.
- Avoid duplicating business rules that belong to the backend.
- Treat backend validation and authorization as the authoritative source for protected business operations.

---

## 7. Database Management

PostgreSQL is the relational database used by StockWise.

SQLAlchemy is used as the persistence technology, while Alembic manages database schema evolution.

Database changes must follow these principles:

- Structural changes must be represented through migrations.
- Database constraints should protect critical data integrity when appropriate.
- Application-level business rules should complement database constraints.
- Existing migration history should be preserved.
- Manual schema modifications should be avoided when a migration is required.
- Historical business information should not be removed when it is required for traceability.

---

## 8. Testing Strategy

Automated testing is part of the development process.

The backend test suite uses Pytest to verify critical behavior across different application layers.

Tests should cover, when applicable:

- Domain and business rules.
- Application use cases.
- Repository behavior.
- API endpoints.
- Authentication.
- Authorization.
- Validation and error scenarios.
- Inventory consistency.
- Sales behavior.
- Historical data preservation.

Tests should be executed after relevant changes and before considering a backend feature complete.

Version 1.0 prioritizes strong automated verification of critical backend behavior.

---

## 9. API Development

StockWise exposes its backend functionality through a REST API implemented with FastAPI.

API development should follow these principles:

- Use resource-oriented endpoints.
- Use appropriate HTTP methods.
- Return meaningful HTTP status codes.
- Validate incoming data.
- Require authentication for protected resources.
- Enforce authorization on the backend.
- Return consistent error information.
- Maintain compatibility between frontend data contracts and backend responses.

FastAPI automatically provides interactive API documentation through Swagger, which is used during development and manual API validation.

---

## 10. Security Practices

Security must be considered throughout the development lifecycle.

Version 1.0 applies the following practices:

- Passwords are stored using secure password hashing.
- Plain-text passwords are never persisted.
- Authentication is performed using JWT access tokens.
- Protected endpoints require authentication.
- Restricted operations enforce role-based authorization.
- Inactive users cannot authenticate.
- Sensitive authentication information must not be returned unnecessarily through API responses.
- Environment-specific configuration and secrets must not be committed to the repository.

---

## 11. Version Control Workflow

Git is used for source control and GitHub is used as the remote repository.

The project follows an incremental commit workflow.

Changes should generally be committed when a coherent unit of work is complete and validated.

Commit messages should clearly describe the purpose of the change.

Examples:

```text
feat: implement user management backend
feat: implement user management frontend
fix: preserve historical sale information
docs: update database design documentation
test: add sale cancellation coverage
```

Before committing significant changes:

1. Review modified files.
2. Run the relevant automated tests or build checks.
3. Confirm that generated or environment-specific files are not included.
4. Commit the coherent change.
5. Push the change to the remote repository.
6. Confirm that the working tree is clean when appropriate.

---

## 12. Documentation Standards

Documentation must evolve together with the implementation.

The project documentation includes:

- Project overview.
- Business requirements.
- User stories.
- Use cases.
- Functional and non-functional requirements.
- Database design.
- Entity-Relationship diagrams.
- Product roadmap.

Documentation must describe the current implementation accurately and distinguish implemented Version 1.0 capabilities from functionality planned for future versions.

Outdated design assumptions should be updated when the implementation changes.

---

## 13. Definition of Done

A feature can be considered complete when the applicable conditions below are satisfied:

- The business behavior is clearly defined.
- The backend implementation is complete.
- Required authorization rules are enforced.
- Database changes are represented through migrations when necessary.
- Relevant automated tests pass.
- The frontend integration is complete when the feature requires a user interface.
- Expected success and error scenarios have been validated.
- The application builds successfully when frontend changes are involved.
- Relevant documentation reflects the implemented behavior.
- The completed work is committed to version control.

---

## 14. Version Evolution

StockWise is developed through progressive releases.

### Version 1.0 — Minimum Viable Product

Focuses on delivering a complete inventory and sales management workflow with strong software engineering foundations.

### Version 2.0 — Professional Engineering

Will introduce additional infrastructure, integrations, reporting capabilities, automation, and operational improvements.

### Version 3.0 — Enterprise Architecture

May introduce distributed services, event-driven communication, cloud infrastructure, observability, and AI-assisted capabilities.

Future-version technologies should not be documented as already implemented until they are actually integrated into the project.