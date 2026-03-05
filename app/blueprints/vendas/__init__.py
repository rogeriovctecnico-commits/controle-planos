from flask import Blueprint

vendas_bp = Blueprint("vendas", __name__, url_prefix="/vendas", template_folder="templates")

from . import routes