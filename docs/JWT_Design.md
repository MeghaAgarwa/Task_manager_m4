# JWT Authentication & Authorization Specification

This document details the architecture, payload structure, and claims used to secure the Task Manager Application using JSON Web Tokens (JWT) and Role-Based Access Control (RBAC).

## 1. Token Architecture Flow
The application uses short-lived asymmetric tokens passed via the standard HTTP `Authorization: Bearer <TOKEN>` header to securely identify users without querying the database for every single endpoint interaction.

[ Postman / Client ] ➔ Sends Credentials ➔ [ /auth/login Endpoint ]
▲                                             │
│ Checks Token validity                      ▼ Validates & Encrypts
└──────── Allows Request 🔐 Returns JWT Token String


## 2. JWT Token Structure & Target Claims

Every access token issued by this system consists of three parts separated by dots (`.`): Header, Payload, and Signature. The **Payload** contains the following mandated JSON claims:

### Standard Claims (Registered)
* **`sub` (Subject):** The unique identifier of the authenticated user (stores the user's primary `email`).
* **`exp` (Expiration Time):** Unix timestamp determining exactly when the token becomes invalid (set to 60 minutes from issuance).
* **`iat` (Issued At):** Unix timestamp marking the exact second the token was generated.

### Custom Claims (Application Specific)
* **`role` (RBAC Security Tier):** Determines user permissions. Must be one of: `admin`, `manager`, or `member`.
* **`is_active` (Status Flag):** A boolean confirming if the account is in a healthy, unblocked state.

### Complete Payload Example
```json
{
  "sub": "engineer@domain.com",
  "role": "manager",
  "is_active": true,
  "iat": 1791888000,
  "exp": 1791891600
}