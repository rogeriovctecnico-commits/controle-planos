from flask import Flask, redirect, url_for, render_template, send_from_directory, session
from .extensions import db, migrate, mail
from .config import Config
from datetime import datetime, date, timezone
import os
import sys
from sqlalchemy import func
from .models import Cliente, Operadora, Plano, PrecoFaixaEtaria, Administradora, Venda


def create_app():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
        instance_dir = os.path.join(base_dir, 'instance')
        internal_dir = os.path.join(sys._MEIPASS, 'app')  # type: ignore
        app = Flask(
            __name__,
            instance_path=instance_dir,
            template_folder=os.path.join(internal_dir, 'templates'),
            static_folder=os.path.join(internal_dir, 'static')
        )
        
                # Correção de templates de blueprints
        blueprints_dir = os.path.join(internal_dir, 'blueprints')
        if os.path.exists(blueprints_dir):
            for root, dirs, files in os.walk(blueprints_dir):
                if 'templates' in dirs and app.jinja_loader:
                    app.jinja_loader.searchpath.append(os.path.join(root, 'templates')) # type: ignore
    else:
        # Modo desenvolvimento normal
        app = Flask(__name__)
        app.secret_key = os.environ.get("FLASK_SECRET_KEY", "fallback_key_insegura")

    # Configurações
    app.config.from_object(Config)

    if getattr(sys, 'frozen', False):
        db_path = os.path.join(app.instance_path, 'planos.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    mail.init_app(app)

    # Importa e registra blueprints (todos devem usar Blueprint, não importar app)
    from .blueprints.auth.routes import auth_bp
    from .blueprints.administradoras import administradoras_bp
    from .blueprints.clientes import clientes_bp
    from .blueprints.operadoras import operadoras_bp
    from .blueprints.planos import planos_bp
    from .blueprints.precos_faixa_etaria import precos_bp
    from .blueprints.vendas import vendas_bp
    from .relatorios.views import bp as relatorios_bp
    from .blueprints.auth.routes import test_bp 

    app.register_blueprint(auth_bp)
    app.register_blueprint(test_bp)

    app.register_blueprint(administradoras_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(operadoras_bp)
    app.register_blueprint(planos_bp)
    app.register_blueprint(precos_bp)
    app.register_blueprint(vendas_bp)
    app.register_blueprint(relatorios_bp)

    # Cria as tabelas
    with app.app_context():
        db.create_all()

    # Processador de contexto
    @app.context_processor
    def inject_now():
        return {'now': lambda: datetime.now(timezone.utc)}

    @app.template_filter('format_date')
    def format_date(value):
        if not value:
            return ""
        if isinstance(value, (datetime, date)):
            return value.strftime('%d/%m/%Y')
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value).strftime('%d/%m/%Y')
            except ValueError:
                return value
        return str(value)

    # Rota favicon
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )

    # ========================================
    # ROTA INICIAL - DASHBOARD
    # ========================================
    @app.route("/")
    @app.route("/index")
    @app.route("/dashboard")
    def index():
        # Verifica se está logado
        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        # Contagem de registros para os totalizadores
        total_operadoras = Operadora.query.count()
        total_planos = Plano.query.count()
        total_precos = PrecoFaixaEtaria.query.count()
        total_administradoras = Administradora.query.count()
        total_vendas = Venda.query.count()
        total_clientes = Cliente.query.count()

        # Dados para o Gráfico de Ganhos (Comissão + Premiação por Mês)
        ganhos_query = db.session.query(
            func.strftime('%Y-%m', Venda.data_venda).label('mes'),
            func.sum(Venda.comissao),
            func.sum(Venda.premiacao),
            func.sum(Venda.valor_final)
        ).group_by('mes').order_by('mes').all()

        grafico_labels = []
        grafico_comissao = []
        grafico_premiacao = []
        grafico_valor_final = []

        for row in ganhos_query:
            if row[0]:
                mes_formatado = datetime.strptime(row[0], '%Y-%m').strftime('%m/%Y')
                grafico_labels.append(mes_formatado)
                grafico_comissao.append(float(row[1] or 0))
                grafico_premiacao.append(float(row[2] or 0))
                grafico_valor_final.append(float(row[3] or 0))

        if not grafico_labels:
            grafico_labels = ["Sem dados"]
            grafico_comissao = [0]
            grafico_premiacao = [0]
            grafico_valor_final = [0]

        # Dados para o Gráfico de Total de Vendas por Mês
        vendas_mes_query = db.session.query(
            func.strftime('%Y-%m', Venda.data_venda).label('mes'),
            func.sum(Venda.valor_final)
        ).group_by('mes').order_by('mes').all()

        grafico_vendas_labels = []
        grafico_vendas_totais = []

        for row in vendas_mes_query:
            if row[0]:
                mes_formatado = datetime.strptime(row[0], '%Y-%m').strftime('%m/%Y')
                grafico_vendas_labels.append(mes_formatado)
                grafico_vendas_totais.append(float(row[1] or 0))

        if not grafico_vendas_labels:
            grafico_vendas_labels = ["Sem vendas"]
            grafico_vendas_totais = [0]

        return render_template(
            'dashboard.html',
            total_operadoras=total_operadoras,
            total_planos=total_planos,
            total_precos=total_precos,
            total_administradoras=total_administradoras,
            total_vendas=total_vendas,
            total_clientes=total_clientes,
            grafico_labels=grafico_labels,
            grafico_comissao=grafico_comissao,
            grafico_premiacao=grafico_premiacao,
            grafico_valor_final=grafico_valor_final,
            grafico_vendas_labels=grafico_vendas_labels,
            grafico_vendas_totais=grafico_vendas_totais
        )

    # ========================================
    # RETURN APP NO FINAL DE TUDO!
    # ========================================
    return app