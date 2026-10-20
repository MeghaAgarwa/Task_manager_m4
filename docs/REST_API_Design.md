# REST API Specification: Task Manager API

This document details the REST API endpoints, resources, and contracts for the Task Manager application.

## Resource Structure
- **User**: Represents a user identity.
- **Task**: Represents an individual to-do item owned by a specific user.

## API URL Structure & Methods

| Method | Endpoint | Description | Auth Required |
|:---|:---|:---|:---|
| **POST** | `/users/` | Register a new user account | No |
| **POST** | `/auth/login` | Authenticate user and return a JWT access token | No |
| **GET** | `/users/` | Fetch current user profile details | Yes (Bearer Token) |
| **POST** | `/tasks/` | Create a new task for the authenticated user | Yes (Bearer Token) |
| **GET** | `/tasks/` | Fetch paginated slice of tasks for the logged-in user | Yes (Bearer Token) |
| **GET** | `/tasks/{task_id}` | Fetch a single task by its unique ID | Yes (Bearer Token) |
| **PUT** | `/tasks/{task_id}` | Update fields of an existing task  | Yes (Bearer Token) |
| **DELETE** | `/tasks/{task_id}` | Delete a specific task | Yes (Bearer Token) |

---

## Request / Response Contracts

### 1. User Registration
- **URL**: `/users/`
- **Method**: `POST`
- **Request Body (`UserCreate`)**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
- **Response Body (`UserResponse`):
```json
{
  "email": "user@example.com",
  "id": 1
}
```

### 2. User Authentication (Login)
- **URL**: `/auth/login`
- **Method**: `POST`
- **Request Body** (`application/x-www-form-urlencoded`):
```form-data
username: user@example.com
password: password123
```
- **Response Body**s:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Get Current User
- **URL**: `/users/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`

- **Response Body (`UserResponse`)** :
```json
{
  "email": "user@example.com",
  "id": 1
}
```


### 4. Create Task
- **URL**: `/tasks/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body (`TaskCreate`)**:
```json
{
  "title": "New Task",
  "description": "FastApi documentation",
  "priority": "high",
  "due_date": "2026-10-31T23:59:59Z"
}
```
- **Response Body (`TaskResponse`)**:
```json
{
  "title": "1111",
  "description": "11111",
  "priority": "medium",
  "due_date": "2026-10-20T14:18:36.675000",
  "id": 1,
  "is_completed": false,
  "created_at": "2026-10-20T14:19:29.846168",
  "owner_id": 1
}
```

### 5. Get All Tasks (Paginated)
- **URL**: `/tasks/?page=1&size=10`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Response Body (`List[TaskResponse]`)** :
```json
[
  {
    "title": "1111",
    "description": "11111",
    "priority": "medium",
    "due_date": "2026-10-20T14:18:36.675000",
    "id": 1,
    "is_completed": false,
    "created_at": "2026-10-20T14:19:29.846168",
    "owner_id": 1
  }
]
```

### 6. Get Task by id 
- **URL**: `/tasks/1`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Response Body (`TaskResponse`)**:
```json
{
  "title": "1111",
  "description": "11111",
  "priority": "medium",
  "due_date": "2026-10-20T14:18:36.675000",
  "id": 1,
  "is_completed": false,
  "created_at": "2026-10-20T14:19:29.846168",
  "owner_id": 1
}
```


### 7. Update task 
- **URL**: `/tasks/1`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Response Body (`TaskResponse`)**:
```json
{
  "title": "1111",
  "description": "11111",
  "priority": "medium",
  "due_date": "2026-10-20T14:18:36.675000",
  "id": 1,
  "is_completed": true,
  "created_at": "2026-10-20T14:19:29.846168",
  "owner_id": 1
}
```

### 8. Delete Task
- **URL**: `/tasks/1`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`

- **Response Body (`TaskResponse`)**:
```json
{
  "title": "string",
  "description": "string",
  "priority": "medium",
  "due_date": "2026-10-20T15:31:47.479000",
  "id": 1,
  "is_completed": false,
  "created_at": "2026-10-20T15:31:49.699328",
  "owner_id": 1,
  "detail": "Task deleted."
}
```