from app.extensions import db


class User(db.Model):
    """
    Represents a user in the database.

    This class defines the User model using SQLAlchemy.

    Attributes:
        id (int): The unique identifier for the user (primary key).
        username (str): The username of the user (unique, cannot be null).
        password (str): The hashed password of the user (cannot be null).
        tasks (Relationship): One-to-Many relationship with the Todo model.

    :param username: The username of the user.
    :param password: The hashed password of the user.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Establish a one-to-many relationship with the Todo model
    # This creates a 'tasks' attribute on the User model,
    # allowing access to related Todo items.
    tasks = db.relationship("Todo", backref="user", lazy=True)
