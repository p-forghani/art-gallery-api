from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
store_bp = Blueprint('store', __name__)

from backend.app.routes import auth, admin, store  # noqa
