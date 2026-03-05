from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_mail import Mail

# Define a convenção de nomenclatura para todas as constraints do banco de dados.
# Isso evita erros do Alembic com o SQLite.
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db: SQLAlchemy = SQLAlchemy(metadata=metadata)

from flask_migrate import Migrate
migrate = Migrate()
mail = Mail()