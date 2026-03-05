from app import create_app
from app.extensions import db
from sqlalchemy import text
app = create_app()
with app.app_context():
    uri = app.config.get("SQLALCHEMY_DATABASE_URI")
    print("SQLALCHEMY_DATABASE_URI:", uri)
    # tenta obter engine de forma compatível
    engine = getattr(db, "engine", None)
    if engine is None:
        engine = db.get_engine()
    print("Engine URL:", getattr(engine, "url", str(engine)))
    with engine.connect() as conn:
        res = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"))
        rows = [r[0] for r in res.fetchall()]
        print("Tabelas (via SQLAlchemy engine):", rows)
