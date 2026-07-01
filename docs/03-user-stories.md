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