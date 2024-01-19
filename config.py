"""Contains configurations for different environments."""

class Config:
    """
    Base configuration class.

    Attributes:
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Whether to track modifications in SQLAlchemy.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """
    Development configuration class.

    Attributes:
        DEBUG (bool): Whether to enable debugging.
        SQLALCHEMY_DATABASE_URI (str): The URI for the development database.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_todo.db'


class ProductionConfig(Config):
    """
    Production configuration class.

    Attributes:
        DEBUG (bool): Whether to enable debugging (typically set to False in production).
        SQLALCHEMY_DATABASE_URI (str): The URI for the production database.
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod_todo.db'


class TestingConfig(Config):
    """
    Testing configuration class.

    Attributes:
        DEBUG (bool): Whether to enable debugging.
        TESTING (bool): Whether the application is in testing mode.
        SQLALCHEMY_DATABASE_URI (str): The URI for the testing database.
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_todo.db'
