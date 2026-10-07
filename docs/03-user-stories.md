# StockWise - User Stories

## Epic 1 - Authentication & User Management

---

### US-001 - User Login

**Priority:** High

**Version:** v1.0

**Actor:** Registered User

### Description

As a registered user,

I want to log into the platform,

So that I can access the system according to my assigned role.

### Acceptance Criteria

- The user must enter a valid email address and password.
- The system must validate the provided credentials.
- The system must generate a JWT access token after successful authentication.
- Only active users can log into the platform.
- Invalid credentials must display an appropriate error message.

### Business Rules

- The email address must be unique.
- Passwords must be securely encrypted.
- JWT tokens must expire according to the configured policy.

---

### US-002 - User Management

**Priority:** High

**Version:** v1.0

**Actor:** Administrator

### Description

As an administrator,

I want to create, update, activate, and deactivate users,

So that I can control access to the platform.

### Acceptance Criteria

- Only administrators can manage users.
- Each user must have a full name, email, password, and role.
- Email addresses must be unique.
- Users can be activated or deactivated.
- Inactive users cannot log into the system.

### Business Rules

- Every user must have exactly one role.
- Passwords must be stored using secure hashing algorithms.
- Email addresses cannot be duplicated.

---

## Epic 2 - Category Management

---

### US-003 - Create Category

**Priority:** High

**Version:** v1.0

**Actor:** Authorized User

### Description

As an authorized user,

I want to create product categories,

So that I can organize products within the inventory.

### Acceptance Criteria

- The user can create a category with a name and optional description.
- The category name must be valid.
- Newly created categories are active by default.
- The created category must be available for product assignment.

### Business Rules

- Categories are used to classify products.
- Category information must remain consistent across the system.

---

### US-004 - Manage Categories

**Priority:** High

**Version:** v1.0

**Actor:** Authorized User

### Description

As an authorized user,

I want to view, update, activate, and deactivate categories,

So that I can maintain the product classification structure.

### Acceptance Criteria

- The user can view the list of categories.
- The user can update category information.
- The user can activate an inactive category.
- The user can deactivate an active category.
- The category status must be visible to the user.

### Business Rules

- Deactivation must preserve the category record.
- Category status is represented as active or inactive.

---

## Epic 3 - Product Management

---

### US-005 - Create Product

**Priority:** High

**Version:** v1.0

**Actor:** Authorized User

### Description

As an authorized user,

I want to create products,

So that I can register the items managed in the inventory.

### Acceptance Criteria

- The user can create a product with its required information.
- Each product must be associated with a category.
- Product information must be validated before creation.
- Newly created products are active by default.
- The created product must be available for inventory operations.

### Business Rules

- Every product must belong to a category.
- Product data must remain consistent across inventory and sales operations.

---

### US-006 - Manage Products

**Priority:** High

**Version:** v1.0

**Actor:** Authorized User

### Description

As an authorized user,

I want to view, update, activate, and deactivate products,

So that I can maintain the product catalog.

### Acceptance Criteria

- The user can view the list of products.
- The user can view the details of a product.
- The user can update product information.
- The user can activate an inactive product.
- The user can deactivate an active product.
- The product status must be visible to the user.

### Business Rules

- Deactivation must preserve the product record.
- Product status is represented as active or inactive.
- Existing historical information associated with a product must be preserved.

---

## Epic 4 - Inventory Management

---

### US-007 - Register Inventory Movement

**Priority:** High

**Version:** v1.0

**Actor:** Authorized User

### Description

As an authorized user,

I want to register inventory movements,

So that I can keep product stock levels up to date.

### Acceptance Criteria

- The user can register inventory movements for a product.
- The movement must identify the product, movement type, and quantity.
- The system must update the product stock according to the movement.
- The system must validate the movement before applying the stock change.
- The movement must be stored for historical tracking.

### Business Rules

- Inventory movements must use valid products.
- Movement quantities must be valid positive values.
- Stock changes must remain consistent with registered movements.
- Inventory history must not be lost when product information changes.

---

### US-008 - View Inventory History

**Priority:** Medium

**Version:** v1.0

**Actor:** Authorized User

### Description

As an authorized user,

I want to view inventory movement history,

So that I can track changes made to product stock.

### Acceptance Criteria

- The user can view registered inventory movements.
- Each movement must display its associated product.
- Each movement must display its movement type and quantity.
- Historical movements must remain available for consultation.

### Business Rules

- Inventory movements represent historical records and must be preserved.
- Historical information must remain associated with the corresponding product.

---

## Epic 5 - Sales Management

---

### US-009 - Register Sale

**Priority:** High

**Version:** v1.0

**Actor:** Authorized User

### Description

As an authorized user,

I want to register sales with one or more products,

So that I can record transactions and automatically update inventory.

### Acceptance Criteria

- The user can create a sale containing one or more products.
- Each sale item must specify a valid product and quantity.
- The system must validate that sufficient stock is available.
- Product stock must be reduced after a successful sale.
- The system must calculate the sale total from the registered sale items.
- The sale must be stored for historical consultation.

### Business Rules

- A sale must contain at least one item.
- Sale quantities must be positive.
- A sale cannot reduce product stock below the allowed level.
- Sale information must preserve the product data required for historical consistency.

---

### US-010 - View Sales

**Priority:** High

**Version:** v1.0

**Actor:** Authorized User

### Description

As an authorized user,

I want to view registered sales and their details,

So that I can consult the transaction history.

### Acceptance Criteria

- The user can view the list of registered sales.
- The user can open the details of a sale.
- Sale details must display the products and quantities included in the transaction.
- The sale status and total must be visible.
- Historical sales information must remain available even if product information changes later.

### Business Rules

- Sales are historical business records and must be preserved.
- Historical product information associated with a sale must remain consistent.

---

### US-011 - Cancel Sale

**Priority:** High

**Version:** v1.0

**Actor:** Administrator

### Description

As an administrator,

I want to cancel a registered sale,

So that an invalid or reversed transaction can be recorded without deleting its history.

### Acceptance Criteria

- Only administrators can cancel a sale.
- The user must confirm the cancellation action.
- Cancelling a sale must restore the corresponding product stock.
- The cancelled sale must remain available in the sales history.
- The sale status must indicate that it has been cancelled.
- A cancelled sale cannot be cancelled again.

### Business Rules

- Sales must never be physically deleted when cancelled.
- Inventory restoration must correspond to the quantities recorded in the sale.
- Cancellation must preserve the original sale information.

---

## Epic 6 - Dashboard & Stock Alerts

---

### US-012 - View Dashboard

**Priority:** High

**Version:** v1.0

**Actor:** Authorized User

### Description

As an authorized user,

I want to view a dashboard with key business information,

So that I can quickly understand the current state of the system.

### Acceptance Criteria

- The user can access the dashboard after authentication.
- The dashboard displays summary information about the system.
- The displayed information must be obtained from current system data.
- Dashboard information must update as business data changes.

### Business Rules

- Dashboard information must only be available to authenticated users.
- Summary values must reflect the current persisted data.

---

### US-013 - View Low-Stock Alerts

**Priority:** High

**Version:** v1.0

**Actor:** Authorized User

### Description

As an authorized user,

I want to identify products with low stock,

So that I can take action before inventory becomes insufficient.

### Acceptance Criteria

- The system identifies products whose stock has reached the configured low-stock condition.
- Low-stock information is visible to the user.
- The alert information reflects current inventory levels.
- Stock changes must be reflected in the low-stock information.

### Business Rules

- Low-stock status is determined using the product's configured stock threshold.
- Alerts must be based on current inventory information.
- Inventory movements and sales can affect whether a product is considered low stock.

