# config.py

# Database URI for SQLAlchemy to connect to. Here, it's set to use a SQLite database named 'todo.db'.
SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'

# Disable Flask-SQLAlchemy modification tracking, as it's not needed in this application.
SQLALCHEMY_TRACK_MODIFICATIONS = False

# This module contains configuration settings for the Flask application.
# The 'SQLALCHEMY_DATABASE_URI' is set to use a SQLite database named 'todo.db'.
# 'SQLALCHEMY_TRACK_MODIFICATIONS' is set to False to disable Flask-SQLAlchemy modification tracking,
# which is unnecessary for this application.
