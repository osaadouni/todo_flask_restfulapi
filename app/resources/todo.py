"""Contains resource for the todo application."""
from flask_restx import Resource, reqparse, fields, abort, marshal
from flask import request, jsonify

from ..models.todo import Todo
from ..extensions import db, api

# Define a namespace for TODO operations
ns = api.namespace('todos', description='TODO operations')

# Define a data model for a TODO item
todo_model = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'uri': fields.Url('todo_resource', absolute=True),
})

resource_fields = {
    "start": fields.Integer(readonly=True, description="The start of pagination"),
    "limit": fields.Integer(readonly=True, description="The number todo items on each page"),
    "count": fields.Integer(readonly=True, description="The total of todo items."),
    "previous": fields.String(readonly=True, description="The previous list of todo items."),
    "next": fields.String(readonly=True, description="The next list of todo items."),
    'data': fields.List(fields.Nested(todo_model))
}
response_model = api.model("Result", resource_fields)

# Request parser for handling task input
parser = reqparse.RequestParser()
parser.add_argument('task', type=str, required=True)

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
        todo.task = args['task']
        db.session.commit()
        return todo


@ns.route('/')
class TodoListResource(Resource):
    """Handles a list of todos and adds new todos."""
    @ns.doc('list_todos')
    # @ns.marshal_list_with(todo_model)
    @ns.marshal_with(response_model)
    def get(self) -> list:
        """Get all todo items.

        :return: List of all todo items.
        """
        todos = Todo.query.all()
        return self.get_paginated_list(
            todos, '/todos',
            start=request.args.get('start', 1),
            limit=request.args.get('limit', 20)
        )

    @ns.doc('create_todo')
    @ns.expect(todo_model)
    @ns.marshal_with(todo_model, code=201)
    def post(self) -> tuple:
        """Create a new todo item.

        :return: Newly created todo item with status code 201.
        """
        args = parser.parse_args()
        todo = Todo(args['task'])
        db.session.add(todo)
        db.session.commit()
        return todo, 201

    def get_paginated_list(self, data, url, start, limit):
        start = int(start)
        limit = int(limit)
        count = len(data)
        if count < start or limit < 0:
            abort(404)

        result = {
            'start': start,
            'limit': limit,
            'count': count,
        }
        # make previous url
        if start == 1:
            result['previous'] = ''
        else:
            start_copy = max(1, start - limit)
            limit_copy = start - 1
            result['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
        # make next url
        if start + limit > count:
            result['next'] = ''
        else:
            start_copy = start + limit
            result['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
        # finally extract result according to bounds
        result['data'] = marshal(data[(start - 1):(start - 1 + limit)], todo_model)
        return result