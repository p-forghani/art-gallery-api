from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')
admin = Blueprint('admin', __name__, url_prefix='/admin')
store = Blueprint('store', __name__)

from app.routes import auth_routes, admin_routes, store_routes  # noqa
