"""Contains resource for the todo application."""
from flask_restx import Resource, reqparse, fields, abort, marshal
from flask import request, jsonify

from ..models.todo import Todo
from ..extensions import db, api

# Define a namespace for TODO operations
ns = api.namespace('todos', description='TODO operations')

# Define resource_fields for the model
resource_fields = {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'done': fields.Boolean(required=False, description="The task status", default=False),
    'created_at': fields.DateTime(readonly=True, description="The time when the task was created"),
    'updated_at': fields.DateTime(readonly=True, description="The time when the task was modified"),
    # 'uri': fields.Url('todo_resource', readonly=True, absolute=True),
}

# Define a data model for a TODO item
todo_model = api.model('Todo', resource_fields)

response_resource_fields = {
    "first": fields.Integer(readonly=True, description="The start of pagination"),
    "last": fields.Integer(readonly=True, description="The last of pagination"),
    "num_per_page": fields.Integer(readonly=True, description="The number todo items per page"),
    "total_items": fields.Integer(readonly=True, description="The total of todo items."),
    "previous": fields.String(readonly=True, description="The previous list of todo items."),
    "next": fields.String(readonly=True, description="The next list of todo items."),
    'items': fields.List(fields.Nested(todo_model))
}
response_model = api.model("Result", response_resource_fields)

# Request parser for handling task input
parser = reqparse.RequestParser()
parser.add_argument('task', type=str, help='Description of the todo item')
parser.add_argument('done', type=bool, help='Completion status of the todo item')


@ns.route('/<int:todo_id>')
@ns.response(404, "Todo not found")
@ns.param('todo_id', 'The task identifier')
class TodoResource(Resource):
    """Handles managing a single todo item.

    Contains methods for retrieving, deleting, and updating a single todo item.
    """
    @ns.doc('get_todo')
    @ns.marshal_with(todo_model)
    def get(self, todo_id: int) -> dict:
        """Get details of a todo item.

        :param todo_id: The ID of a todo item.
        :return: The todo item if it exists.
        """
        todo = Todo.query.get_or_404(todo_id)
        return todo

    @ns.doc('delete_todo')
    @ns.response(204, "Todo deleted successfully")
    def delete(self, todo_id: int) -> tuple:
        """Delete an existing todo item.

        :param todo_id: The ID of a todo item to be deleted.
        :return: Empty response with status code 204.
        """
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return '', 204

    @ns.expect(todo_model)
    @ns.marshal_with(todo_model)
    def put(self, todo_id: int) -> tuple:
        """Update an existing todo item.

        :param todo_id: The ID of a todo item to be updated.
        :return: Updated todo item with status code 201.
        """
        args = parser.parse_args()
        todo = Todo.query.get_or_404(todo_id)
        if args.get('task') is not None:
            todo.task = args['task']
        if args.get('done') is not None:
            todo.done = args['done']
        db.session.commit()
        return todo


@ns.route('/')
class TodoListResource(Resource):
    """Handles a list of todos and adds new todos."""

    @ns.doc('list_todos')
    @ns.marshal_with(response_model)
    def get(self):

        # Pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        tasks_query = Todo.query.paginate(page=page, per_page=per_page, error_out=False)

        # Searching
        search_query = request.args.get('search')
        if search_query:
            tasks_query = Todo.query.filter(
                Todo.task.ilike(f'%{search_query}%')
            ).paginate(page=page, per_page=per_page, error_out=False)

        return {
            'total_items': tasks_query.total,
            'page': tasks_query.page,
            'num_per_page': tasks_query.per_page,
            'first': tasks_query.first,
            'last': tasks_query.last,
            'previous': tasks_query.prev_num,
            'next': tasks_query.next_num,
            'items': tasks_query.items
        }

    @ns.doc('create_todo')
    @ns.expect(todo_model)
    @ns.marshal_with(todo_model, code=201)
    def post(self) -> tuple:
        """Create a new todo item.

        :return: Newly created todo item with status code 201.
        """
        args = parser.parse_args()
        if args.get('task') is None:
            abort(400, "Task description is required!")
        todo = Todo(args['task'])

        if args.get('done') is not None:
            todo.done = args['done']

        db.session.add(todo)
        db.session.commit()
        return todo, 201
