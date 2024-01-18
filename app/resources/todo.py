from flask_restful import reqparse, abort, Resource

from ..models.todo import Todo
from ..extensions import db


# Request parser for handling task input
parser = reqparse.RequestParser()
parser.add_argument('task', type=str, required=True)


class TodoResource(Resource):
    """Handles managing a single todo item.

    Contains methods for retrieving, deleting and updating a single todo item.
    """
    def get(self, todo_id: int) -> dict[str, str]:
        """Returns a single todo item.

        :param todo_id: The ID of a todo item.
        :return: The todo item if it exists.
        """
        todo = Todo.query.get_or_404(todo_id)
        return {'id': todo.id, 'task': todo.task}

    def delete(self, todo_id: int) -> tuple[str, int]:
        """Deletes an existing todo item.

        :param todo_id: The ID of a todo item to be deleted.
        :return: Empty response with status code 204.
        """
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return '', 204

    def put(self, todo_id: str) -> tuple[dict[str, str], int]:
        """Updates an existing todo item.

        :param todo_id: The ID of a todo item to be updated.
        :return: Updated todo item with status code 201.
        """
        args = parser.parse_args()
        todo = Todo.query.get_or_404(todo_id)
        todo.task = args['task']
        db.session.commit()
        return {'task': todo.task}, 200

class TodoListResource(Resource):
    """Handles list of todos and adds new todos."""
    def get(self) -> dict[int, dict[str, str]]:
        """Get a list of all todo items.

        :return: List of all todo items.
        """
        todos = Todo.query.all()
        return [{'id': todo.id, 'task': todo.task} for todo in todos]

    def post(self) -> tuple[dict[str, str], int]:
        """Creates a new todo item.

        :return: Newly created todo item with status code 201.
        """
        args = parser.parse_args()
        todo = Todo(args['task'])
        db.session.add(todo)
        db.session.commit()
        return {'task': todo.task, 'id': todo.id}, 201
