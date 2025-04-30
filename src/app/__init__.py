from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from src.config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
cors = CORS()


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

    # Initialize Flask-CORS
    cors.init_app(app=app, supports_credentials=True)

    # Register blueprints
    from src.app.routes import artist_bp as artist_blueprint
    from src.app.routes import auth_bp as auth_blueprint
    from src.app.routes import store_bp as store_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(artist_blueprint)
    app.register_blueprint(store_blueprint)

    from src.scripts.initialize_currencies import initialize_currencies
    from src.scripts.initialize_roles import initialize_roles

    # Run the role and currency initialization scripts
    with app.app_context():
        db.create_all()
        initialize_roles(app, db)
        initialize_currencies(app, db)

    return app
