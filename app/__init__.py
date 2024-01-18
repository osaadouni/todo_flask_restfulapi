"""Contains application initialization."""
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

from app.resources.todo import TodoList, Todo

api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<int:todo_id>')
