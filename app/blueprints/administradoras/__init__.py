from flask import Blueprint

administradoras_bp = Blueprint("administradoras", __name__, url_prefix="/administradoras", template_folder="templates")

from . import routes