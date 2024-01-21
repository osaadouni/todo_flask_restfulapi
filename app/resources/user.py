"""Contains resource for the users."""
from flask_jwt_extended import create_access_token
from flask_restx import Resource, fields, reqparse

from ..extensions import api, bcrypt, db
from ..models.user import User

# Define a namespace for User operations
ns = api.namespace("users", description="User operations (Register and Login)")


# Define register resource_fields for the model
resource_fields_register = {
    "id": fields.Integer(readonly=True, description="The user ID"),
    "username": fields.String(required=True, description="The user username"),
    "password": fields.String(required=True, description="The user password"),
}

# Define login resource_fields for the model
resource_fields_login = {
    # "id": fields.Integer(readonly=True, description="The user ID"),
    "access_token": fields.String(
        readonly=True, description="The access token for the user"
    ),
    "username": fields.String(required=True, description="The user username"),
}

# Define a data model for a User
register_user_model = api.model("User", resource_fields_register)
# login_user_model = api.model('User', resource_fields_login)

# User Registration Parser
user_registration_parser = reqparse.RequestParser()
user_registration_parser.add_argument(
    "username", type=str, required=True, help="Username is required"
)
user_registration_parser.add_argument(
    "password", type=str, required=True, help="Password is required"
)

# User Login Parser
user_login_parser = reqparse.RequestParser()
user_login_parser.add_argument(
    "username", type=str, required=True, help="Username is required"
)
user_login_parser.add_argument(
    "password", type=str, required=True, help="Password is required"
)


# User Registration Resource
@ns.route("/register")
class UserRegistrationResource(Resource):
    @ns.doc("register_user")
    @ns.expect(register_user_model)
    @ns.marshal_with(register_user_model, code=201)
    def post(self):
        args = user_registration_parser.parse_args()
        password = args["password"]
        hashed_passwd = bcrypt.generate_password_hash(password)
        decoded_passwd = hashed_passwd.decode("utf-8")
        new_user = User(username=args["username"], password=decoded_passwd)
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201


# User Login Resource
@ns.route("/login")
class UserLoginResource(Resource):
    @ns.doc("login_user")
    @ns.expect(register_user_model)
    @ns.response(401, "Invalid credentials")
    @ns.response(200, "Access token returned")
    def post(self):
        args = user_login_parser.parse_args()
        user = User.query.filter_by(username=args["username"]).first()
        password = args["password"]
        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token, "user": user.username}, 200
        else:
            return {"message": "Invalid credentials"}, 401
