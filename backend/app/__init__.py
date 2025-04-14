from flask_sqlalchemy import SQLAlchemy
from backend.scripts.initialize_roles import initialize_roles
from flask import request
from flask import Flask
from backend.config import Config
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS


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

    # Run the role initialization script
    with app.app_context():
        initialize_roles()

    # Register blueprints
    from backend.app.routes import auth_bp as auth_blueprint
    from backend.app.routes import artist_bp as artist_blueprint
    from backend.app.routes import store_bp as store_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(artist_blueprint)
    app.register_blueprint(store_blueprint)

    @app.before_request
    def log_request_payload():
        if request.method in ['POST', 'PUT', 'PATCH']:
            print(f"Request payload: {request.get_json()}")

    return app
