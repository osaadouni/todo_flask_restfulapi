"""Contains the blueprint for the users."""
from flask import Blueprint
from flask_restx import Api

from app.resources.user import UserLoginResource, UserRegistrationResource

# Create a Flask Blueprint named 'user_bp'
user_bp = Blueprint("user", __name__)

# Create a restful API using the 'user_bp' Blueprint
api = Api(user_bp)

# Add resources (endpoints) to the 'user_bp' API
api.add_resource(UserRegistrationResource, "/users")
api.add_resource(UserLoginResource, "/users")
