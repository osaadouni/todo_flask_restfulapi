from flask import Blueprint
from flask_restful import Api
from app.resources.todo import TodoResource, TodoListResource

# Create a Flask Blueprint named 'todo_bp'
todo_bp = Blueprint('todo', __name__)

# Create a Flask-RESTful API using the 'todo_bp' Blueprint
api = Api(todo_bp)

# Add resources (endpoints) to the 'todo_bp' API
api.add_resource(TodoListResource, '/todos')
api.add_resource(TodoResource, '/todos/<int:todo_id>')

# The 'todo_bp' Blueprint is intended to group related routes and views for todo functionality.
# The 'api' object is an instance of Flask-RESTful Api, associated with the 'todo_bp' Blueprint.

# Two resources ('TodoListResource' and 'TodoResource') are added to the API, defining the behavior
# for the '/todos' and '/todos/<int:todo_id>' endpoints, respectively.
