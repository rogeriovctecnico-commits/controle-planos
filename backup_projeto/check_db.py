# diag_db.py
import sys, os
from importlib import import_module

# garante que a raiz do projeto esteja no path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

candidates = [
    "Controle_de_Planos_Flask.app",
    "Controle_de_Planos_Flask",
    "app",
    "wsgi",
]

for name in candidates:
    try:
        mod = import_module(name)
    except Exception as e:
        # não interrompe, tenta próximo
        continue
    print(f"Importou módulo: {name}")
    # tenta localizar create_app ou app
    create_app = getattr(mod, "create_app", None)
    app_obj = getattr(mod, "app", None)
    try:
        if create_app:
            app = create_app()
            print("Usando create_app()")
        elif app_obj:
            app = app_obj
            print("Usando app direto do módulo")
        else:
            print("Módulo importado, mas sem create_app/app. Continuando.")
            continue

        with app.app_context():
            # imprime a configuração relevante
            print("SQLALCHEMY_DATABASE_URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))
            print("SQLALCHEMY_BINDS:", app.config.get("SQLALCHEMY_BINDS"))
            print("Chaves em app.extensions:", list(app.extensions.keys()))
            sa_ext = app.extensions.get("sqlalchemy")
            print("app.extensions['sqlalchemy'] repr:", repr(sa_ext))
            # tenta obter engine de formas seguras
            try:
                engine = getattr(sa_ext, "db", None)
                if engine is None:
                    # em algumas versões, a extensão expõe get_engine ou engine
                    engine = getattr(sa_ext, "get_engine", None)
                print("Atributo sqlalchemy.db/get_engine:", engine)
                # se possível, imprime a URL do engine
                if engine is not None:
                    try:
                        # se for callable get_engine(bind=None)
                        if callable(engine):
                            e = engine()
                        else:
                            e = engine
                        print("Engine URL:", getattr(e, "url", str(e)))
                    except Exception as ee:
                        print("Não foi possível obter engine.url:", ee)
            except Exception as e:
                print("Erro ao inspecionar extensão sqlalchemy:", e)
    except Exception as e:
        print("Erro ao criar app a partir do módulo:", e)
    print("-" * 60)