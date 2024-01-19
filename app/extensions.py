"""Contains extension initializations of the application."""
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

# Initialize SQLAlchemy for database operations
db = SQLAlchemy()

# Initialize API for building RESTful services
api = Api(version='1.0', title='Todo API',
    description='A simple Todo API',
    url_prefix='/api/v1'
)
