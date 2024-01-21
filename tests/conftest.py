"""Contains common fixtures for pytest."""

from app import db
from config import TestingConfig

import pytest
from app import create_app


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

