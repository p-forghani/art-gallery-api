from flask import Blueprint
from flask_restx import Namespace, Api

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
store_bp = Blueprint('store', __name__, url_prefix='/store')
artist_bp = Blueprint('artist', __name__, url_prefix='/artist')

# # Wrap each blueprint in its own api
# auth_api = Api(
#     auth_bp, title='Auth API',
#     version='1.0', description='Auth operations')
# store_api = Api(
#     store_bp, title='Store API',
#     version='1.0', description='Store operations')
artist_api = Api(
    artist_bp, title='Artist API',
    version='1.0', description='Artist operations', doc='/docs')

# auth_namespace = Namespace('auth')
# store_namespace = Namespace('store')
artist_namespace = Namespace('', path='')

# # Register namespaces to their respective APIs
# auth_api.add_namespace(auth_namespace)
# store_api.add_namespace(store_namespace)
artist_api.add_namespace(artist_namespace)

from src.app.routes import auth, artist, store  # noqa
