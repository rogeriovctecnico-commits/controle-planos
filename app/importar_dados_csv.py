import csv
from decimal import Decimal
from datetime import datetime

from app.models import Cliente, Venda, Operadora, Plano

from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    print("Contexto Flask carregado com sucesso")


app = create_app()

CSV_FILE = "ControleClientes_corrigido.csv"


# =========================
# HELPERS
# =========================

def parse_int(valor, default=1):
    if not valor:
        return default

    valor = (
        str(valor)
        .replace(".", "")
        .replace(",", ".")
        .strip()
    )

    try:
        return int(Decimal(valor))
    except Exception:
        return default

def normalizar_email(row):
    raw = (row.get("EMAIL") or "").strip()

    if raw:
        return raw.replace("E-mail:", "").strip().lower()

    identificador = row.get("ID") or row.get("CLIENTE") or "desconhecido"
    identificador = identificador.replace(" ", "").lower()
    return f"sem-email-{identificador}@importacao.local"


def parse_date(data):
    if not data:
        return None
    try:
        return datetime.strptime(data.strip(), "%d/%m/%Y").date()
    except Exception:
        return None


def parse_decimal(valor):
    if not valor:
        return None

    valor = (
        str(valor)
        .replace("R$", "")
        .replace(".", "")
        .replace(",", ".")
        .replace(" ", "")
        .strip()
    )

    if valor == "":
        return None

    try:
        return Decimal(valor)
    except Exception:
        return None


def calcular_valor_final(row):
    total = parse_decimal(row.get("TOTAL GANHO"))
    if total is not None:
        return total

    valor = parse_decimal(row.get("VALOR"))
    desconto = parse_decimal(row.get("DESCONTO")) or Decimal("0.00")

    if valor is not None:
        return valor - desconto

    return Decimal("0.00")


def calcular_valor_venda(row):
    valor = parse_decimal(row.get("VALOR"))
    return valor if valor is not None else Decimal("0.00")


# =========================
# IMPORTAÇÃO
# =========================

with app.app_context():

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:

            # =====================
            # CLIENTE
            # =====================
            email = normalizar_email(row)

            with db.session.no_autoflush:
                cliente = Cliente.query.filter_by(email=email).first()

            if not cliente:
                cliente = Cliente(
                    nome=row.get("CLIENTE", "").strip(),
                    email=email,
                    telefone=row.get("TELEFONE"),
                    data_nascimento=parse_date(row.get("DT_NASCIMENTO")),
                )
                db.session.add(cliente)
                db.session.flush()
            else:
                cliente.nome = row.get("CLIENTE", "").strip()
                cliente.telefone = row.get("TELEFONE")
                cliente.data_nascimento = parse_date(row.get("DT_NASCIMENTO"))

            # =====================
            # OPERADORA
            # =====================
            nome_operadora = row.get("OPERADORA", "").strip().upper()

            operadora = Operadora.query.filter_by(
                nome_operadora=nome_operadora
            ).first()

            if not operadora:
                operadora = Operadora(nome_operadora=nome_operadora)
                db.session.add(operadora)
                db.session.flush()

            # =====================
            # PLANO
            # =====================
            plano_nome = f"PLANO {nome_operadora}"

            plano = Plano.query.filter_by(
                nome_plano=plano_nome,
                operadora_id=operadora.id
            ).first()

            if not plano:
                plano = Plano(
                    nome_plano=plano_nome,
                    valor_base=parse_decimal(row.get("VALOR")),
                    tipo_plano="individual",
                    operadora_id=operadora.id,
                    administradora=row.get("ADMINISTRADORA"),
                )
                db.session.add(plano)
                db.session.flush()

            # =====================
            # EVITAR DUPLICAÇÃO
            # =====================
            data_vigencia = parse_date(row.get("VIGENCIA"))

            venda_existente = Venda.query.filter_by(
                cliente_id=cliente.id,
                plano_id=plano.id,
                data_vigencia=data_vigencia
            ).first()

            if venda_existente:
                print(f"↩ Venda já existe para {cliente.nome}")
                continue

            # =====================
            # VENDA
            # =====================
            venda = Venda(
                cliente_id=cliente.id,
                plano_id=plano.id,
                data_vigencia=data_vigencia,
                origem=row.get("ORIGEM"),
                natureza=row.get("NATUREZA"),
                promocao=row.get("PROMOÇAO"),
                numeros_vida=int(row.get("VIDAS") or 1),
                valor_venda=calcular_valor_venda(row),
                desconto=parse_decimal(row.get("DESCONTO")) or Decimal("0.00"),
                valor_final=calcular_valor_final(row),
                administradora=row.get("ADMINISTRADORA"),
                titular_nome=cliente.nome,
                titular_valor=parse_decimal(row.get("VALOR")),
            )

            venda.calcular_comissao_regra_especifica()
            db.session.add(venda)

        db.session.commit()

print("✔ Importação finalizada com sucesso e sem duplicações.")
