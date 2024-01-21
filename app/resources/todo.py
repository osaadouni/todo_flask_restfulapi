"""Contains resource for the todo application."""
from flask import request
from flask_restx import Resource, abort, fields, reqparse

from ..extensions import api, db
from ..models.todo import Todo

# Define a namespace for TODO operations
ns = api.namespace("todos", description="Todo operations")

# Define resource_fields for the model
resource_fields = {
    "id": fields.Integer(readonly=True, description="The task ID"),
    "task": fields.String(required=True, description="The task details"),
    "done": fields.Boolean(
        required=False, description="The task status", default=False
    ),
    "created_at": fields.DateTime(
        readonly=True, description="The time when the task was created"
    ),
    "updated_at": fields.DateTime(
        readonly=True, description="The time when the task was modified"
    ),
    # 'uri': fields.Url('todo_resource', readonly=True, absolute=True),
}

# Define a data model for a TODO item
todo_model = api.model("Todo", resource_fields)

response_resource_fields = {
    "first": fields.Integer(readonly=True, description="Start page"),
    "last": fields.Integer(readonly=True, description="Last page"),
    "num_per_page": fields.Integer(readonly=True, description="Num per page"),
    "total_items": fields.Integer(readonly=True, description="Total todos."),
    "previous": fields.String(readonly=True, description="Prev list todos."),
    "next": fields.String(readonly=True, description="Next list todos."),
    "items": fields.List(fields.Nested(todo_model)),
}
response_model = api.model("Result", response_resource_fields)

# Request parser for handling task input
parser = reqparse.RequestParser()
parser.add_argument("task", type=str, help="Description of todo item")
parser.add_argument("done", type=bool, help="Completion status of todo item")


@ns.route("/<int:todo_id>")
@ns.response(404, "Todo not found")
@ns.param("todo_id", "The task identifier")
class TodoResource(Resource):
    """Handles managing a single todo item.

    Contains methods for retrieving, deleting, and updating a single todo item.
    """

    @ns.doc("get_todo")
    @ns.marshal_with(todo_model)
    def get(self, todo_id: int) -> dict:
        """Get details of a todo item.

        :param todo_id: The ID of a todo item.
        :return: The todo item if it exists.
        """
        todo = Todo.query.get_or_404(todo_id)
        return todo

    @ns.doc("delete_todo")
    @ns.response(204, "Todo deleted successfully")
    def delete(self, todo_id: int) -> tuple:
        """Delete an existing todo item.

        :param todo_id: The ID of a todo item to be deleted.
        :return: Empty response with status code 204.
        """
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return "", 204

    @ns.expect(todo_model)
    @ns.marshal_with(todo_model)
    def put(self, todo_id: int) -> tuple:
        """Update an existing todo item.

        :param todo_id: The ID of a todo item to be updated.
        :return: Updated todo item with status code 201.
        """
        args = parser.parse_args()
        todo = Todo.query.get_or_404(todo_id)
        if args.get("task") is not None:
            todo.task = args["task"]
        if args.get("done") is not None:
            todo.done = args["done"]
        db.session.commit()
        return todo


@ns.route("/")
class TodoListResource(Resource):
    """Handles a list of todos and adds new todos."""

    @ns.doc("list_todos")
    @ns.marshal_with(response_model)
    def get(self):
        # 1. Filtering
        tasks_query = self._process_done_query_filter()

        # 2. Searching
        tasks_query = self._process_search_query_filter(tasks_query)

        # 3. Sorting
        tasks_query = self._process_sortby_query_filter(tasks_query)

        # 3. Pagination
        tasks_query = self._process_pagination(tasks_query)

        return {
            "total_items": tasks_query.total,
            "page": tasks_query.page,
            "num_per_page": tasks_query.per_page,
            "first": tasks_query.first,
            "last": tasks_query.last,
            "previous": tasks_query.prev_num,
            "next": tasks_query.next_num,
            "items": tasks_query.items,
        }

    @ns.doc("create_todo")
    @ns.expect(todo_model)
    @ns.marshal_with(todo_model, code=201)
    def post(self) -> tuple:
        """Create a new todo item.

        :return: Newly created todo item with status code 201.
        """
        args = parser.parse_args()
        if args.get("task") is None:
            abort(400, "Task description is required!")
        todo = Todo(args["task"])

        if args.get("done") is not None:
            todo.done = args["done"]

        db.session.add(todo)
        db.session.commit()
        return todo, 201

    def _process_done_query_filter(self):
        if request.args.get("filter_done", False):
            tasks_query = Todo.query.filter(Todo.done.is_(True))
        else:
            tasks_query = Todo.query.filter()
        return tasks_query

    def _process_search_query_filter(self, query):
        if (search_query := request.args.get("search")) is not None:
            query = query.filter(Todo.task.ilike(f"%{search_query}%"))
        return query

    def _process_sortby_query_filter(self, tasks_query):
        sort_by = request.args.get("sort_by", "id")
        sort_order = request.args.get("sort_order", "asc")
        return tasks_query.order_by(
            getattr(Todo, sort_by).desc()
            if sort_order == "desc"
            else getattr(Todo, sort_by)
        )

    def _process_pagination(self, query):
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        return query.paginate(page=page, per_page=per_page, error_out=False)
