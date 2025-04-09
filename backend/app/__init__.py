from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from backend.config import Config
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()


# Initialize the Flask application
def create_app(config_class=Config):

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Initialize the database
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate.init_app(app, db)

    # Initialize Flask-Bcrypt
    bcrypt.init_app(app)

    # Initialize Flask-JWT-Extended
    jwt.init_app(app)

    # Register blueprints
    from backend.app.routes import auth_bp as auth_blueprint
    from backend.app.routes import admin_bp as admin_blueprint
    from backend.app.routes import store_bp as store_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(store_blueprint)

    return app
