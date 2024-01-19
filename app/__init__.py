"""Contains factory for application instances."""
from flask import Flask
from .extensions import db, api
from .blueprints.todo import todo_bp
import config


def create_app(app_config=None):
    """
    Factory function to create and configure the Flask application.

    This function initializes the Flask application, configures the database,
    registers extensions, creates database tables, and registers blueprints.

    :return: The configured Flask application instance.
    """
    app = Flask(__name__)


    # Configure the Flask application with the database URI and track modifications setting
    if app_config is None:
        app.config.from_object(config.DevelopmentConfig)
    else:
        app.config.from_object(app_config)

    # Initialize Flask extensions
    db.init_app(app)
    api.init_app(app)

    # Create database tables within the application context
    with app.app_context():
        db.create_all()

    # Register the 'todo_bp' blueprint, which may contain routes and views related to todo operations
    app.register_blueprint(todo_bp)

    return app
