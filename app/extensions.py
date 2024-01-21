"""Contains extension initializations of the application."""
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy for database operations
db = SQLAlchemy()

# Initialize API for building RESTful services
token_attrs = {"type": "apiKey", "in": "header", "name": "Authorization"}
authorizations = {"Bearer": token_attrs}
api = Api(
    version="1.0",
    title="Flask Todo API with JWT-Based Authentication",
    description="Welcome to the Swagger UI documentation site!",
    doc="/ui",
    authorizations=authorizations,
)

bcrypt = Bcrypt()
jwt = JWTManager()
