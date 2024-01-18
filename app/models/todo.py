from app.extensions import db


class Todo(db.Model):
    """
    Represents a Todo item in the database.

    This class defines the Todo model using SQLAlchemy. It includes fields for
    the unique identifier ('id') and the task description ('task').

    :param task: The task description for the Todo item.
    """
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255))

    def __init__(self, task):
        """
        Initializes a new Todo instance.

        :param task: The task description for the Todo item.
        """
        self.task = task

# The 'Todo' class is a SQLAlchemy model representing the 'todos' table in the database.
# It has two columns: 'id' (primary key) and 'task'. The '__init__' method is used to
# create new instances of the Todo class with the specified task.
