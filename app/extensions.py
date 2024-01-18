"""Contains extension initializations of the application."""
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

# Initialize SQLAlchemy for database operations
db = SQLAlchemy()

# Initialize Flask-RESTful API for building RESTful services
api = Api()

