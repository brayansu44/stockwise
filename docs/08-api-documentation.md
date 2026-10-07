# StockWise - API Documentation

## 1. Overview

StockWise exposes a REST API implemented with FastAPI.

The API provides operations for:

- Authentication.
- User management.
- Category management.
- Product management.
- Inventory movements.
- Sales.
- Low-stock identification.
- Dashboard information.
- Application health verification.

Version 1.0 of the API uses OpenAPI 3.1 and provides interactive Swagger documentation.

When the backend is running locally:

```text
http://localhost:8000/docs
```

The OpenAPI specification is available at:

```text
http://localhost:8000/openapi.json
```

---

## 2. Base URL

The default local API URL is:

```text
http://localhost:8000
```

The frontend communicates with this API through its configured `VITE_API_URL`.

---

## 3. Authentication

StockWise uses JWT-based authentication.

After successful login, authenticated requests use the generated access token to access protected endpoints.

The API distinguishes between:

- Public endpoints.
- Authenticated endpoints.
- Role-restricted operations.

Backend authorization is the authoritative access-control mechanism.

---

## 4. Root and Health

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/` | Returns the API root response. | Public |
| GET | `/health/` | Verifies that the API is available. | Public |

---

## 5. Authentication Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/auth/login` | Authenticates a user and returns an access token. | Public |
| GET | `/auth/me` | Returns information about the currently authenticated user. | Required |

Inactive users are not allowed to authenticate.

---

## 6. User Endpoints

User-management operations are restricted to administrators.

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/users/` | Lists registered users. | Administrator |
| POST | `/users/` | Creates a new user. | Administrator |
| PUT | `/users/{user_id}` | Updates an existing user. | Administrator |
| PATCH | `/users/{user_id}/deactivate` | Deactivates a user. | Administrator |
| PATCH | `/users/{user_id}/activate` | Activates a user. | Administrator |

User emails must remain unique.

Passwords are stored securely and are never returned through user-management responses.

---

## 7. Category Endpoints

Category operations support the management of product classification information.

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/categories/` | Lists categories. | Required |
| POST | `/categories/` | Creates a category. | Required |
| GET | `/categories/{category_id}` | Returns a category by identifier. | Required |
| PATCH | `/categories/{category_id}` | Updates a category. | Required |
| PATCH | `/categories/{category_id}/activate` | Activates a category. | Required |
| PATCH | `/categories/{category_id}/deactivate` | Deactivates a category. | Required |

Role-based restrictions are enforced by the backend according to the operation.

---

## 8. Product Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/products/` | Lists products. | Required |
| POST | `/products/` | Creates a product. | Required |
| GET | `/products/low-stock` | Lists products whose current stock is at or below their configured minimum stock. | Required |
| GET | `/products/{code}` | Returns a product using its unique code. | Public |
| PATCH | `/products/{code}` | Updates a product. | Required |
| PATCH | `/products/{code}/activate` | Activates a product. | Required |
| PATCH | `/products/{code}/deactivate` | Deactivates a product. | Required |

A product is considered low stock when:

```text
current_stock <= minimum_stock
```

Low-stock state is calculated from current product information and is not stored as a separate alert entity.

---

## 9. Inventory Movement Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/inventory-movements/` | Registers an inventory movement and updates product stock accordingly. | Required |
| GET | `/inventory-movements/product/{product_code}` | Lists inventory movements associated with a product. | Required |

Inventory movements provide traceability for stock changes.

Supported business operations include stock entries, exits, and adjustments according to the application's inventory rules.

Sales and sale cancellations can also generate inventory movements automatically.

---

## 10. Sales Endpoints

| Method | Endpoint | Description | Authentication / Access |
|---|---|---|---|
| GET | `/sales/` | Lists registered sales. | Required |
| POST | `/sales/` | Registers a new sale. | Required |
| GET | `/sales/{sale_id}` | Returns the details of a sale. | Required |
| PATCH | `/sales/{sale_id}/cancel` | Cancels an eligible sale and restores inventory. | Administrator |

When a sale is created, the application validates available stock before completing the operation.

A completed sale reduces inventory and generates the corresponding inventory movements.

Cancelled sales are preserved as historical records rather than being deleted.

---

## 11. Dashboard Endpoint

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/dashboard/summary` | Returns the operational dashboard summary. | Required |

The dashboard provides aggregated operational information used by the StockWise frontend.

---

## 12. Main API Resources

The Version 1.0 API works with the following main resources:

```text
User
Category
Product
InventoryMovement
Sale
SaleItem
```

The main request and response schemas exposed through OpenAPI include:

```text
CategoryResponse
CreateCategoryRequest
CreateInventoryMovementRequest
CreateProductRequest
CreateSaleItemRequest
CreateSaleRequest
CreateUserRequest
DashboardSummary
InventoryMovementResponse
LoginRequest
MovementType
ProductResponse
SaleItemResponse
SaleResponse
SaleStatus
TokenResponse
UpdateCategoryRequest
UpdateProductRequest
UpdateUserRequest
UserResponse
UserRole
```

FastAPI also exposes validation-related schemas such as:

```text
HTTPValidationError
ValidationError
```

---

## 13. API Security

Protected endpoints require authentication using the access token generated by the login endpoint.

Security controls include:

- Password hashing.
- JWT authentication.
- Protected endpoints.
- Role-based authorization.
- User activation status validation.
- Unique user email validation.
- Business-rule validation.
- Request schema validation.

Frontend route restrictions improve the user experience, but backend authorization remains responsible for enforcing security.

---

## 14. Error Handling

The API validates incoming requests and business operations before completing them.

Possible failure scenarios include:

- Invalid credentials.
- Missing authentication.
- Insufficient permissions.
- Inactive users.
- Duplicate user emails.
- Invalid product or category information.
- Insufficient inventory.
- Invalid inventory movements.
- Invalid sale operations.
- Attempts to cancel an ineligible sale.
- Resource-not-found scenarios.
- Request validation errors.

FastAPI and the application layer return HTTP responses appropriate to the detected error.

---

## 15. Interactive Documentation

Swagger can be used during development to:

- Inspect available endpoints.
- Review request schemas.
- Review response schemas.
- Authenticate requests.
- Execute API operations manually.
- Inspect validation responses.

Local Swagger URL:

```text
http://localhost:8000/docs
```

This interactive documentation is generated automatically from the FastAPI application and therefore complements this high-level API reference.

---

## 16. Version 1.0 API Scope

The current API represents the StockWise Version 1.0 MVP.

Future versions may extend the API with capabilities such as:

- Audit logs.
- Report generation.
- Excel export.
- Email notifications.
- External integrations.
- Caching.
- Additional operational services.

These capabilities are intentionally outside the Version 1.0 API scope.