# Task Management App with Flask RESTful API

This is a simple Flask REST API application for managing a task list.
The API provides basic operations for handling tasks,
including retrieving all tasks, getting a specific task,
adding a new task, and deleting an existing task. It also provides user
authentication and (given time) the goal is to enable authorization on
the appropriate access points.
The application comes with a Swagger-UI included for easy access and testing
the access points.
#### Multiple environment support:
The application is built to work with different environments:
development, production and testing, which can be customized to own
preferences.
#### Authentication and Authorization:
A user model has been implemented to support registration and authentication.

The registration process requires a username and a password and can be created through
the endpoint:
> `/users/register`
>
The login/authentication process requires a username and a password and can be created through
the endpoint:

> `/users/login`

**Example**:

Request:
> `curl -X 'POST'
  'http://127.0.0.1:5000/users/login'
  -H 'accept: application/json'
  -H 'Content-Type: application/json'
  -d '{
  "username": "omar",
  "password": "secretpass"
}'`

Response:
> `{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNTg3NzAxOCwianRpIjoiMjg4NWUxYTQtMzllNC00MTYwLTkzZmUtNDIxY2QyNmUzZDFlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzA1ODc3MDE4LCJjc3JmIjoiOTBjNmFkY2MtNDIxYy00ZTk5LTllMGUtMTlkYTQ3ZDE5NzA5In0.EPvUtYsOv_7Iiwm6vkzYq08lbhVxu03w44pB84j8Wxg",
  "user": "omar"
}`

The authentication is based on a **JWT token** generation. On a successful login an '**access_token**' is
returned which can be used for authorization in the request header as a **Bearer token** for subsequent requests.

> `Authorization: Bearer <access_token>`

## Features

### **Endpoints**

#### Retrieve all tasks:
    Endpoint: /todos
    Method: GET
    Description: Get a list of all tasks.

#### Retrieve a specific task:
    Endpoint: /todos/<todo_id>
    Method: GET
    Description: Get details of a specific task identified by its unique ID.

#### Add a new task:
    Endpoint: /todos
    Method: POST
    Description: Add a new task to the list.

#### Delete an existing task:

    Endpoint: /todos/<todo_id>
    Method: DELETE
    Description: Delete a task based on its unique ID.

### Additional Features

#### Search for tasks

You can search for tasks using appropriate query parameters.

#### Pagination:

The API supports pagination to efficiently handle a large number of tasks.
> `/todos?page=1&per_page=10`

#### Filtering:

Tasks can be filtered based on specific criteria, enhancing the search functionality.
> `/todos?search=foo`

#### Sorting:

Tasks can be sorted based on various attributes, providing flexibility in viewing the task list.
> `/todos?sort_by=id&sort_order=desc`

#### Unit Testing

The application includes unit tests using pytest to ensure the reliability and correctness of the implemented features.
> `pytest`

### Getting Started

#### Prerequisites

> `Flask==3.0.0`
> `flask-sqlalchemy==3.1.1`
> `flask-restx==1.3.0`
> `pytest==7.4.4`
> `pytest-flask==1.3.0`
> `pre-commit==3.6.0`
> `Flask-JWT-Extended==4.6.0`
> `Flask-Bcrypt==1.0.1`


### Installation

#### Clone the repository:

> `
git clone https://github.com/osaadouni/todo_flask_restfulapi.git
`

#### Install dependencies:

> `pip install -r requirements.txt`

#### Run the application:

> `python run.py`

### Usage

Once the application is running, you can use your preferred API client (e.g., Postman) or tools
like curl to interact with the API endpoints. Or you can use Swagger UI documentation by
accessing the UI at /swagger-ui/ .

### Examples

#### Retrieve all tasks:

> `curl -X 'GET'
  'http://127.0.0.1:5000/todos/'
  -H 'accept: application/json'
  -H 'Authorization: Bearer X.Y.Z'
 `

#### Retrieve a specific task:

> `curl -X 'GET'
  'http://127.0.0.1:5000/todos/2'
  -H 'accept: application/json'
  -H 'Authorization: Bearer X.Y.Z'`

#### Add a new task:

> `curl -X 'POST'
  'http://127.0.0.1:5000/todos/'
  -H 'accept: application/json'
  -H 'Authorization: Bearer X.Y.Z'
  -H 'Content-Type: application/json'
  -d '{
  "task": "Do something today",
  "done": false
}'`

#### Delete a task:

> `curl -X 'DELETE'
  'http://127.0.0.1:4000/todos/6'
  -H 'accept: application/json'
  -H 'Authorization: Bearer X.Y.Z'`

#### Update a task:
> `curl -X 'PUT'
  'http://127.0.0.1:5000/todos/2'
  -H 'accept: application/json'
  -H 'Authorization: Bearer x.y.z'
  -H 'Content-Type: application/json'
  -d '{
  "task": "Changes to task with ID 2",
  "done": true
}'`

### Swagger UI docs
Swagger UI provides access to a UI with all available endpoints
of the application (managing tasks operations and user registration
and authentication).

#### Access URL for Swagger API endpoints:
>`http://localhost:5000/swagger-ui/`


### Testing
The application has a couple of unit tests written in pytest (fixtures)
included for the most operations.

You can run tests locally by typing:

> `pytest`


### pre-commit
The application code comes with pre-commit support and configuration hooks
for the most code quality check tools available
(isort, flake8 , black, ruff ..etc)

Install
> `pip install pre-commit`

Run:
> `pre-commit install`
