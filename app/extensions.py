"""Contains extension initializations of the application."""
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy for database operations
db = SQLAlchemy()

# Initialize API for building RESTful services
authorizations = {
    "Bearer Auth": {"type": "apiKey", "in": "header", "name": "Authorization"},
}
api = Api(
    version="1.0",
    title="Task Management Application with Flask REST API",
    description="Welcom to the Swagger UI documentation!",
    doc="/swagger-ui",
    authorizations=authorizations,
    security="Bearer Auth",
)

bcrypt = Bcrypt()
jwt = JWTManager()
