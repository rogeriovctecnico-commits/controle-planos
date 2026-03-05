# debug.py (na pasta raiz do projeto)
from app import create_app

app = create_app()

with app.app_context():
    print("=== ROTAS REGISTRADAS ===")
    clientes_routes = []
    all_routes = []
    
    for rule in app.url_map.iter_rules():
        all_routes.append(f"{rule.endpoint:30} -> {rule.rule}")
        if 'clientes' in rule.endpoint:
            clientes_routes.append(f"{rule.endpoint:30} -> {rule.rule}")
    
    print("TODAS AS ROTAS:")
    for route in all_routes:
        print(route)
    
    print("\nROTAS DE CLIENTES:")
    if clientes_routes:
        for route in clientes_routes:
            print(route)
    else:
        print("NENHUMA ROTA DE CLIENTES ENCONTRADA!")