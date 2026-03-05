from flask import Blueprint

planos_bp = Blueprint("planos", __name__, url_prefix="/planos", template_folder="templates")

from . import routes