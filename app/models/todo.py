"""Contains models for todo application."""
from datetime import datetime

from app.extensions import db


class Todo(db.Model):
    """
    Represents a Todo item in the database.

    This class defines the Todo model using SQLAlchemy. It includes fields for
    the unique identifier ('id'), the task description ('task'), the completion
    status ('done'), the creation timestamp ('created_at'), and the last
    modification timestamp ('updated_at').

    :param task: The task description for the Todo item.
    :param done: A boolean indicating whether the task is completed or not.
    :param created_at: The timestamp representing when the Todo item was created.
    :param updated_at: The timestamp representing when the Todo item was last updated.
    """
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255))
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, task, done=False):
        """
        Initializes a new Todo instance.

        :param task: The task description for the Todo item.
        :param done: A boolean indicating whether the task is completed or not. Defaults to False.
        """
        self.task = task
        self.done = done

# The 'Todo' class is a SQLAlchemy model representing the 'todos' table in the database.
# It has five columns: 'id' (primary key), 'task', 'done', 'created_at', and 'updated_at'.
# The '__init__' method is used to create new instances of the Todo class with the specified task.