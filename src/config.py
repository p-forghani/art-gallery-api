from datetime import timedelta
import os
from pathlib import Path


# store the db in the main app directory
base_dir = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL')
        or 'sqlite:///' + os.path.join(base_dir, 'app.db')
    )
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or 'your_jwt_secret_key'
    # FUTURE: Set the JWT expiration time to a lower value for production
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_BLOCKLIST_ENABLED = True
    # TODO: Add refresh token too.
    JWT_BLOCKLIST_TOKEN_CHECKS = ['access']


class TestingConfig(Config):
    """
    Testing configuration class for Flask application.
    Inherits from the base Config class.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = 'test-secret-key'
    SECRET_KEY = 'test-secret-key'
