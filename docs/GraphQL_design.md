# GraphQL Design — Task Manager

This document specifies the GraphQL interface for the Task Manager application.

## 1. Overview
The application allows users to:

Register using an email address and password.
Log in using email and password.
Sign in using Google.
Retrieve their profile.
Create, view, update, and delete tasks.
Search tasks by title or description.
Retrieve tasks using pagination.

The application uses PostgreSQL for data persistence, SQLAlchemy as the ORM, and JWT for application authentication.

This document defines the GraphQL schema, queries, mutations, authentication requirements, and error-handling conventions. 

## 2. GraphQL Endpoint

The GraphQL API will be exposed through a single endpoint:
POST /graphql

All GraphQL queries and mutations will be sent to this endpoint.



Authenticated requests must include the application JWT in the HTTP Authorization header.
Authorization: Bearer <access_token>


## 3. Object Types

### User: Represents a registered application user.

enum Role {
  USER
  ADMIN
}

type User {
  id: ID!
  email: String!
  role: Role!=USER
  tasks(page: Int = 1, size: Int = 10): TaskConnection!
}

The task field returns only tasks belonging to the specified user. 

### Task: Represents a task belonging to a user.
enum Priority {
  LOW
  MEDIUM
  HIGH
}


type Task {
  id: ID!
  title: String!
  description: String
  isCompleted: Boolean!
  priority: Priority!
  dueDate: DateTime
  createdAt: DateTime!
  ownerID: User!
}

### 4. Pagination
The application uses pagination when retrieving tasks.
The GraphQL interface will expose pagination metadata alongside the task results.

type TaskConnection {
  items: [Task!]!
  total: Int!
  page: Int!
  size: Int!
  pages: Int!
}

type TaskDeleteResponse {
  id: ID!
  detail: String!
}

### 5. Input Types

User Registration Input

input RegisterUserInput {
  email: String!
  password: String!
}


Email/Password Login Input

input LoginInput {
  email: String!
  password: String!
}


Create Task Input

input CreateTaskInput {
  title: String!
  description: String
  priority: Priority = MEDIUM
  dueDate: DateTime
}


Update Task Input

input UpdateTaskInput {
  title: String
  description: String
  isCompleted: Boolean
  priority: Priority
  dueDate: DateTime
  
}

Delete Task Input

input DeleteTaskInput {
  id: ID!
}



### 6. Authentication Types

JWT Token Auth Payload

type Token {
  accessToken: String!
  tokenType: String!
}


### 7. Queries

Syntax:
fieldName(argumentName: ArgumentType!): ReturnType

type Query {
  currentUser: User!
  task(id: ID!): Task
  myAllTasks(page: Int = 1, size: Int = 10): TaskConnection!
  
}
* Can also use "extend" keyword to write more query definitions separately

Syntax for query request:
query {      
fieldName(arguments) {
        field1
        field2
        (any number of fields from the response contract)
    }
}

Example query 
query { 
    currentUser { 
        id 
        email 
        } 
    }


### 8. Mutations

Mutations create, update, or delete application data.

type Mutation {
  registerUser(input: RegisterUserInput!):User!         #  Register User

  login(input: LoginInput!): Token!                     # Login

  createTask(input:CreateTaskInput):Task!             # 3 Create Task

  updateTask(id:ID!, input:UpdateTaskInput):Task!     # 4 Update Task
  
  deleteTask(input:DeleteTaskInput): TaskDeleteResponse!   # 5 Delete Task
}


Note:  
The Response contracts define what data is client allowed to request 
The client chooses what data it wants to recieve via the query

Syntax:
mutation {
    mutationName(input: {
        requiredField: value    # any fields allowed in input + the required ones
        optionalField: value
    }) {
        returnedField1          # any fields allowed in response to be returned
        returnedField2
    }
}

Eg:
mutation {
    createTask(input: { title: "Learn GraphQL", priority: HIGH}) {
        id
        title
    }
}

### Scalars
Email
DateTime