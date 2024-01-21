# Task Management App with Flask RESTful API

This is a simple Flask REST API application for managing a task list.
The API provides basic operations for handling tasks,
including retrieving all tasks, getting a specific task,
adding a new task, and deleting an existing task. It also provides user
authentication and (given time) the goal is to enable authorization on
the appropriate access points.
The application comes with a Swagger-UI included for easy access and testing
the access points.

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

#### Filtering:

Tasks can be filtered based on specific criteria, enhancing the search functionality.

#### Sorting:

Tasks can be sorted based on various attributes, providing flexibility in viewing the task list.

#### Unit Testing

The application includes unit tests using pytest to ensure the reliability and correctness of the implemented features.

### Getting Started

#### Prerequisites

Python 3.x, Flask, Flask-restx, SQLAlchemy and
other dependencies (specified in requirements.txt)

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

> `curl http://localhost:5000/todos`

#### Retrieve a specific task:

> `curl http://localhost:5000/todos/1`

#### Add a new task:

> `curl -X POST -H "Content-Type: application/json" -d '{"task": "New Task"}' `http://localhost:5000/tasks

#### Delete a task:

> `curl -X DELETE http://localhost:5000/todos/1`


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
