from flask import Blueprint

operadoras_bp = Blueprint("operadoras", __name__, url_prefix="/operadoras", template_folder="templates")

from . import routes