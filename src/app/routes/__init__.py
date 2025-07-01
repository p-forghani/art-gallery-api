from flask import Blueprint
from flask_restx import Namespace, Api

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
store_bp = Blueprint('store', __name__, url_prefix='/store')
artist_bp = Blueprint('artist', __name__, url_prefix='/artist')

# Create separate api objects for each blueprint
auth_api = Api(auth_bp, doc='/doc/auth', title='Auth API', description='Authentication and user management endpoints')
store_api = Api(store_bp, doc='/doc/store', title='Store API', description='Artwork browsing, comments, and upvotes endpoints')
artist_api = Api(artist_bp, doc='/doc/artist', title='Artist API', description='Artist-specific endpoints for managing artworks')

auth_namespace = Namespace('', description='Authentication operations')
store_namespace = Namespace('', description='Store operations for browsing and interacting with artworks')
artist_namespace = Namespace('', description='Artist operations for managing artworks')

auth_api.add_namespace(auth_namespace)
artist_api.add_namespace(artist_namespace)
store_api.add_namespace(store_namespace)

from src.app.routes import auth, artist, store  # noqa
