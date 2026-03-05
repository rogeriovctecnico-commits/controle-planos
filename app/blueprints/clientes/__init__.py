# app/blueprints/clientes/__init__.py
from flask import Blueprint

clientes_bp = Blueprint(
    'clientes', 
    __name__, 
    template_folder='templates',
    url_prefix='/clientes'
)

# Importar as rotas DEPOIS de criar o blueprint
from . import routes