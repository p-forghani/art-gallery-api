from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
artist_bp = Blueprint('artist', __name__, url_prefix='/artist')
store_bp = Blueprint('store', __name__, url_prefix='/store')

from src.app.routes import auth, artist, store  # noqa
