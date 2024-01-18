from flask_restful import reqparse, abort, Resource


# Initial todo items
TODOS: dict[int, dict[str, str]] = {
    1: {'task': 'Spin up an initial flask app.'},
    2: {'task': 'Add RESTful API resources and endpoints.'},
    3: {'task': 'Add db storage'},
    4: {'task': 'Add Unit tests'},
    5: {'task': 'Add docstrings'},
}

# Request parser for handling task input
parser = reqparse.RequestParser()
parser.add_argument('task')

def abort_if_todo_doesnt_exist(todo_id: int) -> None:
    """Abort the request if the specified todo_id doesn't exist.

    :param todo_id: The ID of a todo item.
    """
    try:
        todo_id = int(todo_id)
    except ValueError:
        abort(404, message=f"Todo with ID {todo_id} is not a valid integer")

    if todo_id not in TODOS:
        abort(404, message=f"Todo with ID {todo_id} doesn't exist")


class Todo(Resource):
    """Handles managing a single todo item.

    Contains methods for retrieving, deleting and updating a single todo item.
    """
    def get(self, todo_id: int) -> dict[str, str]:
        """Returns a single todo item.

        :param todo_id: The ID of a todo item.
        :return: The todo item if it exists.
        """
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id: int) -> tuple[str, int]:
        """Deletes an existing todo item.

        :param todo_id: The ID of a todo item to be deleted.
        :return: Empty response with status code 204.
        """
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id: str) -> tuple[dict[str, str], int]:
        """Updates an existing todo item.

        :param todo_id: The ID of a todo item to be updated.
        :return: Updated todo item with status code 201.
        """
        args = parser.parse_args()
        task: dict[str, str] = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201

class TodoList(Resource):
    """Handles list of todos and adds new todos."""
    def get(self) -> dict[int, dict[str, str]]:
        """Get a list of all todo items.

        :return: List of all todo items.
        """
        return TODOS

    def post(self) -> tuple[dict[str, str], int]:
        """Creates a new todo item.

        :return: Newly created todo item with status code 201.
        """
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = f'todo{todo_id}'
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201
