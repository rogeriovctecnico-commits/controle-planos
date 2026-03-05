from flask import Blueprint

precos_bp = Blueprint("precos", __name__, url_prefix="/precos", template_folder="templates")

from . import routes