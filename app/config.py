from dotenv import load_dotenv
import os

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

# DEBUG: Mostra o caminho do banco
db_path = os.path.join(basedir, '..', 'planos.db')

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.abspath(db_path)}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "rogeriovctecnico@gmail.com"
    MAIL_PASSWORD = "kvjj fctu pnuy hxvs"
    MAIL_DEFAULT_SENDER = "rogeriovctecnico@gmail.com"

