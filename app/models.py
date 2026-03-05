from .extensions import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from decimal import Decimal


class Operadora(db.Model):
    __tablename__ = "operadoras"
    id = db.Column(db.Integer, primary_key=True)
    nome_operadora = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    planos = db.relationship(
        "Plano", back_populates="operadora", cascade="all, delete-orphan"
    )


class Administradora(db.Model):
    __tablename__ = "administradoras"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    nome_administradora = db.Column(db.String(100), unique=True, nullable=False)


class Plano(db.Model):
    __tablename__ = "planos"
    id = db.Column(db.Integer, primary_key=True)
    nome_plano = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.Text)
    valor_base = db.Column(db.Numeric(10, 2), nullable=False)
    cobertura = db.Column(db.Text)
    tipo_plano = db.Column(db.String(50), nullable=False, default="individual")
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    operadora_id = db.Column(db.Integer, db.ForeignKey("operadoras.id"), nullable=False)
    regiao = db.Column(db.String(100))
    acomodacao = db.Column(db.String(50))
    administradora = db.Column(db.String(100))
    entidade = db.Column(db.String(100))
    beneficios = db.Column(db.Text)
    data_vigencia = db.Column(db.Date)
    created_by_username = db.Column(db.String(100))

    operadora = db.relationship("Operadora", back_populates="planos")
    precos_faixa = db.relationship(
        "PrecoFaixaEtaria", back_populates="plano", cascade="all, delete-orphan"
    )
    vendas = db.relationship(
        "Venda", back_populates="plano", cascade="all, delete-orphan"
    )


class PrecoFaixaEtaria(db.Model):
    __tablename__ = "precos_faixa_etaria"
    id = db.Column(db.Integer, primary_key=True)
    plano_id = db.Column(db.Integer, db.ForeignKey("planos.id"), nullable=False)
    idade_min = db.Column(db.Integer, nullable=False)
    idade_max = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    plano = db.relationship("Plano", back_populates="precos_faixa")


from .extensions import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    data_nascimento = db.Column(db.Date)
    data_aniversario_contrato = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cnpj = db.Column(db.String(18))  # Se for um cliente PJ
    responsavel = db.Column(db.String(120))  # Se for um cliente PJ
    status = db.Column(db.String(20), default="ativo")
    ultimo_parabens_enviado = db.Column(db.Date)

    vendas = db.relationship(
        "Venda", back_populates="cliente", cascade="all, delete-orphan"
    )


class Venda(db.Model):
    __tablename__ = "vendas"
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    plano_id = db.Column(db.Integer, db.ForeignKey("planos.id"), nullable=False)
    data_venda = db.Column(db.DateTime)
    data_vigencia = db.Column(db.Date)
    origem = db.Column(db.Text)
    natureza = db.Column(db.Text)
    promocao = db.Column(db.Text)
    numeros_vida = db.Column(db.Integer, default=1)
    comissao = db.Column(db.Numeric(10, 2))
    premiacao = db.Column(db.Numeric(10, 2))
    premiacao_paga = db.Column(db.Boolean, default=False)
    comissao_paga = db.Column(db.Boolean, default=False)
    valor_venda = db.Column(db.Numeric(10, 2), nullable=False)
    desconto = db.Column(db.Numeric(5, 2), default=0.0)
    valor_final = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="ativa")
    tipo_plano = db.Column(db.String(120))
    administradora = db.Column(db.String(120))
    titular_nome = db.Column(db.String(120))
    titular_valor = db.Column(db.Numeric(10, 2))
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    cliente = db.relationship("Cliente", back_populates="vendas")
    plano = db.relationship("Plano", back_populates="vendas")

    def calcular_comissao_regra_especifica(self):
        """
        Calcula automaticamente a comissão de 30% sobre o valor da venda
        se a operadora for Medsenior ou Best Senior.
        Retorna True se houve alteração.
        """
        if self.plano and self.plano.operadora:
            nome_op = self.plano.operadora.nome_operadora.lower()
            # Verifica se o nome da operadora contém os termos alvo
            if (
                "medsenior" in nome_op
                or "best senior" in nome_op
                or "bestsenior" in nome_op
                or "med senior" in nome_op
            ):
                if self.valor_venda:
                    self.comissao = self.valor_venda * Decimal("0.30")
                    return True
        return False


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
