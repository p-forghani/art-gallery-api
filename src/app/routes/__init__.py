from flask import Blueprint
from flask_restx import Namespace, Api

auth_bp = Blueprint('auth', __name__)
store_bp = Blueprint('store', __name__)
artist_bp = Blueprint('artist', __name__)

# Create separate api objects for each blueprint
auth_api = Api(auth_bp, doc='/doc/auth')
store_api = Api(store_bp, doc='/doc/store')
artist_api = Api(artist_bp, doc='/doc/artist')

auth_namespace = Namespace('auth')
store_namespace = Namespace('store')
artist_namespace = Namespace('artist')

auth_api.add_namespace(auth_namespace)
artist_api.add_namespace(artist_namespace)
store_api.add_namespace(store_namespace)

from src.app.routes import auth, artist, store  # noqa
