import os
from flask import Flask

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "fallback_key_insegura")

@app.route('/debug-routes')
def debug_routes():
    """Mostra todas as rotas disponíveis"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"{rule.endpoint} -> {rule}")
    return '<br>'.join(sorted(routes))