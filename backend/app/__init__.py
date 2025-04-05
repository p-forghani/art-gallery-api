from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import Config


db = SQLAlchemy()


# Initialize the Flask application
def create_app():

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)

    # Register blueprints
    from backend.app.routes import auth as auth_blueprint
    from backend.app.routes import admin as admin_blueprint
    from backend.app.routes import store as store_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(store_blueprint)

    return app
