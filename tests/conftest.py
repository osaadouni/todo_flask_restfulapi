"""Contains common fixtures for pytest."""

import pytest
from flask_jwt_extended import create_access_token

from app import create_app, db
from config import TestingConfig


# Fixture to create and configure the Flask app for testing
@pytest.fixture()
def app():
    """
    Fixture to create and configure the Flask app for testing.

    Returns:
        Flask app instance: The configured Flask app for testing.
    """
    app = create_app(app_config=TestingConfig)
    app.config.from_object(TestingConfig)

    # Create the database within the app context
    with app.app_context():
        db.create_all()

    # Other setup can go here

    yield app  # Yield the app for test use

    # Clean up / reset resources here
    with app.app_context():
        db.drop_all()


# Fixture to provide a test client for the Flask app
@pytest.fixture()
def client(app):
    """
    Fixture to provide a test client for the Flask app.

    Args:
        app (Flask): The Flask app instance.

    Returns:
        FlaskClient: The Flask test client.
    """
    return app.test_client()


@pytest.fixture
def auth_headers():
    # Create a JWT token with a mock user ID
    token = create_access_token(identity=1)
    return {"Authorization": f"Bearer {token}"}
