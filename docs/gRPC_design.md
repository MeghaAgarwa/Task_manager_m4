
# gRPC Design

The gRPC API exposes services and methods rather than a single HTTP endpoint.
Clients invoke methods defined in the Protocol Buffers (.proto) contract.

The contract defines:
Service names and RPC methods.
Request message types.
Response message types.
Field names and data types.
Enums for fields such as role and priority.

Protocol Buffers are used to define the contract, and gRPC uses these definitions to generate client and server code.


## Enums

enum Role {
  ROLE_UNSPECIFIED = 0;
  USER = 1;
  ADMIN = 2;
}

enum Priority {
  PRIORITY_UNSPECIFIED = 0;
  LOW = 1;
  MEDIUM = 2;
  HIGH = 3;
}

--------------------


## User Messages

message User {
  int64 id = 1;
  string email = 2;
  Role role = 3;
}

message RegisterUserRequest {
  string email = 1;
  string password = 2;
}

message RegisterUserResponse {
  User user = 1;
}

message LoginRequest {
  string email = 1;
  string password = 2;
}

message TokenResponse {
  string access_token = 1;
  string token_type = 2;
}

message GetCurrentUserRequest {
  // No fields required.
}

message GetCurrentUserResponse {
  User user = 1;
}

// --------------------

## Task Messages

message Task {
  int64 id = 1;
  string title = 2;
  optional string description = 3;
  bool is_completed = 4;
  Priority priority = 5;
  optional google.protobuf.Timestamp due_date = 6;
  google.protobuf.Timestamp created_at = 7;
  int64 owner_id = 8;
}

message CreateTaskRequest {
  string title = 1;
  optional string description = 2;
  Priority priority = 3;
  optional google.protobuf.Timestamp due_date = 4;
}

message GetTaskRequest {
  int64 id = 1;
}

message UpdateTaskRequest {
  int64 id = 1;
  optional string title = 2;
  optional string description = 3;
  optional bool is_completed = 4;
  optional Priority priority = 5;
  optional google.protobuf.Timestamp due_date = 6;
}

message DeleteTaskRequest {
  int64 id = 1;
}

message DeleteTaskResponse {
  int64 id = 1;
  string detail = 2;
}

// --------------------

 ## Pagination

message PaginationRequest {
  int32 page = 1;
  int32 size = 2;
}

message TaskSearchRequest {
  int32 page = 1;
  int32 size = 2;
  optional string search = 3;
  optional bool is_completed = 4;
}

message TaskListResponse {
  repeated Task items = 1;
  int64 total = 2;
  int32 page = 3;
  int32 size = 4;
  int32 pages = 5;
}

// --------------------

## User Task Listing

message GetUserTasksRequest {
  int64 user_id = 1;
  int32 page = 2;
  int32 size = 3;
}

// --------------------
// Google Sign-In
// --------------------

message GoogleSignInRequest {
  string google_id_token = 1;
}

message GoogleSignInResponse {
  TokenResponse token = 1;
}

// --------------------
## Services


service AuthService {
  rpc RegisterUser(RegisterUserRequest)
      returns (RegisterUserResponse);

  rpc Login(LoginRequest)
      returns (TokenResponse);

}

service UserService {
  rpc GetCurrentUser(GetCurrentUserRequest)
      returns (GetCurrentUserResponse);

  
}

service TaskService {
  rpc CreateTask(CreateTaskRequest)
      returns (Task);

  rpc GetTask(GetTaskRequest)
      returns (Task);

  rpc GetMyTasks(TaskSearchRequest)
      returns (TaskListResponse);

  rpc UpdateTask(UpdateTaskRequest)
      returns (Task);

  rpc DeleteTask(DeleteTaskRequest)
      returns (DeleteTaskResponse);
}

service AdminService {
  rpc GetAllUsers(google.protobuf.Empty)
      returns (UserListResponse);
}

 --------------------

Admin Responses

message UserListResponse {
  repeated User users = 1;
}





# The intended flow is:

gRPC Client
     |
     | RPC request + authentication metadata
     v
gRPC Service
     |
     | Validate request and authenticate user
     v
Application / Business Logic
     |
     | SQLAlchemy queries and transactions
     v
PostgreSQL
     |
     | Database results
     v
Application / Business Logic
     |
     | Map database objects to protobuf messages
     v
gRPC Service
     |
     | RPC response
     v
gRPC Client


Implementation will require:

Saving the schema as task_manager.proto.
Generating Python protobuf message classes and gRPC service stubs.
Implementing the service methods.
Connecting each service to the existing SQLAlchemy database layer.
Implementing JWT authentication and role-based authorization.
Mapping database models to protobuf response messages.
Validating inputs, pagination, and optional update fields.
Testing the service methods and their error conditions.


# Example RPC Requests

These examples illustrate the logical messages exchanged between the client and server. They are not GraphQL queries or REST request bodies.

Example 1: Register a user

Request:

RegisterUserRequest {
  email: "user@example.com"
  password: "example-password"
}

Response:

RegisterUserResponse {
  user {
    id: 1
    email: "user@example.com"
    role: USER
  }
}

The response must not include the password or password hash.

Example 2: Log in

Request:

LoginRequest {
  email: "user@example.com"
  password: "example-password"
}

Response:

TokenResponse {
  access_token: "<application-jwt>"
  token_type: "Bearer"
}

Example 3: Create a task

Request:

CreateTaskRequest {
  title: "Learn gRPC"
  description: "Implement the Task Manager service"
  priority: HIGH
}

The JWT is supplied separately through gRPC metadata.

Response:

Task {
  id: 10
  title: "Learn gRPC"
  description: "Implement the Task Manager service"
  is_completed: false
  priority: HIGH
  owner_id: 1
}

The server obtains owner_id from the authenticated user's identity.

Example 4: Retrieve tasks with pagination and search

Request:

TaskSearchRequest {
  page: 1
  size: 10
  search: "GraphQL"
  is_completed: false
}

Response:

TaskListResponse {
  items {
    id: 10
    title: "Learn GraphQL"
    is_completed: false
    priority: MEDIUM
    owner_id: 1
  }
  total: 1
  page: 1
  size: 10
  pages: 1
}

The server returns only tasks owned by the authenticated user that match the search term and completion filter.


Example 5: Update a task

Request:

UpdateTaskRequest {
  id: 10
  is_completed: true
}

Only the specified field is updated; other task fields remain unchanged.

Example 6: Delete a task

Request:

DeleteTaskRequest {
  id: 10
}

Response:

DeleteTaskResponse {
  id: 10
  detail: "Task deleted."
}


