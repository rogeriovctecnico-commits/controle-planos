from flask import Blueprint

confiauto_bp = Blueprint("confiauto", __name__, url_prefix="/confiauto", template_folder="templates")

from . import routes