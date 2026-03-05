from flask import (
    render_template, request, redirect, url_for,
    flash, session, Blueprint, current_app
)
from sqlalchemy import func
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
import logging

from app import db
from app.models import Usuario, Venda
from app.extensions import mail

# Configuração básica de logging
logger = logging.getLogger(__name__)

# ============================
# BLUEPRINT
# ============================
auth_bp = Blueprint("auth", __name__, template_folder="templates")

# ============================
# LOGIN
# ============================
@auth_bp.route("/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Evitar múltiplos redirects se já estiver logado
    if "user_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        # Melhorar validação de entrada
        username = request.form.get("username")
        password = request.form.get("password")

        # Verificar se campos não estão vazios
        if not username or not password:
            flash("Preencha ambos os campos!", "warning")
            return render_template("login.html")

        # Remover espaços em branco
        username = username.strip()
        password = password.strip()

        try:
            user = Usuario.query.filter_by(username=username).first()

            if user and user.check_password(password):
                if user.ativo:
                    session["user_id"] = user.id
                    flash("Login realizado com sucesso!", "success")
                    return redirect(url_for("index"))
                else:
                    flash("Usuário inativo. Contate o administrador.", "danger")
            else:
                flash("Usuário ou senha inválidos!", "danger")

        except Exception as e:
            logger.error(f"Erro durante login: {str(e)}")
            flash("Erro interno. Tente novamente.", "danger")

    return render_template("login.html")

# ============================
# LOGOUT
# ============================
@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logout realizado com sucesso!", "info")
    return redirect(url_for("auth.login"))

# ============================
# REGISTER
# ============================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validações básicas
        if not username or not email or not password:
            flash("Todos os campos são obrigatórios!", "warning")
            return render_template("register.html")

        # Remover espaços e normalizar email
        username = username.strip()
        email = email.strip().lower()
        password = password.strip()

        try:
            if Usuario.query.filter((Usuario.username == username) | (Usuario.email == email)).first():
                flash("Usuário ou e-mail já existe!", "danger")
                return redirect(url_for("auth.register"))

            new_user = Usuario(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            flash("Usuário criado com sucesso! Faça login.", "success")
            return redirect(url_for("auth.login"))

        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro durante registro: {str(e)}")
            flash("Erro interno. Tente novamente.", "danger")

    return render_template("register.html")

# ============================
# RESET DE SENHA
# ============================
def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt="reset-senha")

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt="reset-senha", max_age=expiration)
    except Exception:
        return None
    return email

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        
        if not email:
            flash("E-mail é obrigatório!", "warning")
            return render_template("forgot_password.html")

        email = email.strip().lower()

        try:
            user = Usuario.query.filter_by(email=email).first()
            if user:
                token = generate_token(email)
                reset_url = url_for("auth.reset_password", token=token, _external=True)

                msg = Message("Recuperação de senha", recipients=[email])
                msg.body = f"Para redefinir sua senha, clique no link: {reset_url}"
                mail.send(msg)

                flash("Um link de recuperação foi enviado para seu e-mail.", "info")
                return redirect(url_for("auth.login"))
            else:
                flash("E-mail não encontrado!", "danger")

        except Exception as e:
            logger.error(f"Erro ao enviar email de recuperação: {str(e)}")
            flash("Erro ao enviar e-mail. Tente novamente.", "danger")

    return render_template("forgot_password.html")

@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = confirm_token(token)
    if not email:
        flash("Link inválido ou expirado.", "danger")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        password = request.form.get("password")
        
        if not password:
            flash("Senha é obrigatória!", "warning")
            return render_template("reset_password.html")

        password = password.strip()

        try:
            user = Usuario.query.filter_by(email=email).first()
            if user:
                user.set_password(password)
                db.session.commit()
                flash("Senha redefinida com sucesso! Faça login.", "success")
                return redirect(url_for("auth.login"))

        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao redefinir senha: {str(e)}")
            flash("Erro interno. Tente novamente.", "danger")

    return render_template("reset_password.html")

# ============================
# TESTE DE E-MAIL
# ============================
test_bp = Blueprint("test", __name__)

@test_bp.route("/send-test-email")
def send_test_email():
    try:
        msg = Message(
            subject="Teste Flask-Mail",
            recipients=["rogeriovctecnico@gmail.com"],  # ajuste para o e-mail real
            body="Este é um e-mail de teste enviado pelo Flask-Mail usando Gmail."
        )
        mail.send(msg)
        return "E-mail de teste enviado!"
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail de teste: {str(e)}")
        return f"Erro ao enviar e-mail: {str(e)}"