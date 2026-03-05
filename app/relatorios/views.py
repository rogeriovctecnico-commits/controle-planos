from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import func, extract
from datetime import datetime
from ..models import Cliente, Venda, Plano, Operadora
from ..extensions import db
import plotly.express as px
import json
from plotly.utils import PlotlyJSONEncoder

bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')

@bp.route('/')
def index():
    return render_template('relatorios/index.html')

@bp.route('/clientes-ativos')
def clientes_ativos():
    ativos = Cliente.query.filter_by(status='ativo').all()
    inativos = Cliente.query.filter(Cliente.status != 'ativo').all()  # type: ignore
    return render_template('relatorios/clientes_ativos.html', ativos=ativos, inativos=inativos)

@bp.route('/vendas-periodo')
def vendas_periodo():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    query = Venda.query
    
    if data_inicio:
        query = query.filter(Venda.data_venda >= data_inicio)
    if data_fim:
        # Adiciona hora final para garantir que pegue o dia todo se for apenas data
        if len(data_fim) == 10: 
            data_fim += ' 23:59:59'
        query = query.filter(Venda.data_venda <= data_fim)
        
    vendas = query.order_by(Venda.data_venda.desc()).all()
    
    # Totais para o rodapé do relatório
    total_vendas = sum(v.valor_final for v in vendas if v.valor_final)
    total_comissao = sum(v.comissao for v in vendas if v.comissao)
    
    return render_template('relatorios/vendas_periodo.html', vendas=vendas, total_vendas=total_vendas, total_comissao=total_comissao)

@bp.route('/comissoes-pendentes')
def comissoes_pendentes():
    # Filtra vendas onde comissão OU premiação não foram pagas
    pendentes = Venda.query.filter(
        (Venda.comissao_paga == False) | (Venda.premiacao_paga == False)
    ).order_by(Venda.data_venda.asc()).all()
    
    return render_template('relatorios/comissoes_pendentes.html', pendentes=pendentes)

@bp.route('/aniversariantes')
def aniversariantes():
    mes = request.args.get('mes', datetime.now().month, type=int)
    clientes = Cliente.query.filter(extract('month', Cliente.data_nascimento) == mes).order_by(extract('day', Cliente.data_nascimento)).all()
    return render_template('relatorios/aniversariantes.html', clientes=clientes, mes=mes)

@bp.route('/marcar-parabens/<int:cliente_id>', methods=['POST'])
def marcar_parabens(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    cliente.ultimo_parabens_enviado = datetime.now().date()
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/performance-operadoras')
def performance_operadoras():
    resultados = db.session.query(
        Operadora.nome_operadora,
        func.count(Venda.id).label('qtd_vendas'),
        func.sum(Venda.valor_final).label('total_vendas')
    ).join(Plano, Venda.plano_id == Plano.id)\
     .join(Operadora, Plano.operadora_id == Operadora.id)\
     .group_by(Operadora.nome_operadora)\
     .order_by(func.sum(Venda.valor_final).desc()).all()

    return render_template('relatorios/performance_operadoras.html', resultados=resultados)

@bp.route('/graficos/<tipo>')
def graficos(tipo):
    if tipo == 'clientes-ativos':
        return grafico_clientes_ativos()
    elif tipo == 'vendas-periodo':
        return grafico_vendas_periodo()
    elif tipo == 'performance-operadoras':
        return grafico_performance_operadoras()
    elif tipo == 'aniversariantes':
        return grafico_aniversariantes()
    elif tipo == 'comissoes-pendentes':
        return grafico_comissoes_pendentes()
    else:
        return jsonify({'error': 'Tipo de gráfico não encontrado'}), 404

def grafico_clientes_ativos():
    ativos = Cliente.query.filter_by(status='ativo').count()
    inativos = Cliente.query.filter(Cliente.status != 'ativo').count()

    fig = px.pie(values=[ativos, inativos], names=['Ativos', 'Inativos'], title='Status dos Clientes')
    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
    return render_template('relatorios/grafico.html', graphJSON=graphJSON, titulo='Clientes Ativos vs Inativos')

def grafico_vendas_periodo():
    # Vendas por mês nos últimos 12 meses
    vendas_por_mes = db.session.query(
        func.strftime('%Y-%m', Venda.data_venda).label('mes'),
        func.count(Venda.id).label('qtd_vendas'),
        func.sum(Venda.valor_final).label('total_vendas')
    ).filter(Venda.data_venda >= func.date('now', '-12 months'))\
     .group_by(func.strftime('%Y-%m', Venda.data_venda))\
     .order_by(func.strftime('%Y-%m', Venda.data_venda)).all()

    # Converter para listas para Plotly
    meses = [v[0] for v in vendas_por_mes]
    valores = [float(v[2]) if v[2] else 0 for v in vendas_por_mes]

    fig = px.bar(x=meses, y=valores, title='Vendas por Mês (Últimos 12 Meses)')
    fig.update_xaxes(title='Mês')
    fig.update_yaxes(title='Valor Total (R$)')
    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
    return render_template('relatorios/grafico.html', graphJSON=graphJSON, titulo='Vendas por Período')

def grafico_performance_operadoras():
    resultados = db.session.query(
        Operadora.nome_operadora,
        func.count(Venda.id).label('qtd_vendas'),
        func.sum(Venda.valor_final).label('total_vendas')
    ).join(Plano, Venda.plano_id == Plano.id)\
     .join(Operadora, Plano.operadora_id == Operadora.id)\
     .group_by(Operadora.nome_operadora)\
     .order_by(func.sum(Venda.valor_final).desc()).all()

    # Converter para listas para Plotly
    operadoras = [r[0] for r in resultados]
    valores = [float(r[2]) if r[2] else 0 for r in resultados]

    fig = px.bar(x=operadoras, y=valores, title='Performance das Operadoras')
    fig.update_xaxes(title='Operadora')
    fig.update_yaxes(title='Valor Total de Vendas (R$)')
    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
    return render_template('relatorios/grafico.html', graphJSON=graphJSON, titulo='Performance das Operadoras')

def grafico_aniversariantes():
    # Aniversariantes por mês
    aniversariantes_por_mes = db.session.query(
        func.strftime('%m', Cliente.data_nascimento).label('mes'),
        func.count(Cliente.id).label('qtd_clientes')
    ).group_by(func.strftime('%m', Cliente.data_nascimento))\
     .order_by(func.strftime('%m', Cliente.data_nascimento)).all()

    meses = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    nomes_meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    qtd_por_mes = {mes: 0 for mes in meses}
    for mes, qtd in aniversariantes_por_mes:
        qtd_por_mes[mes] = qtd

    fig = px.bar(x=nomes_meses, y=[qtd_por_mes[mes] for mes in meses], title='Aniversariantes por Mês')
    fig.update_xaxes(title='Mês')
    fig.update_yaxes(title='Quantidade de Clientes')
    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
    return render_template('relatorios/grafico.html', graphJSON=graphJSON, titulo='Aniversariantes por Mês')

def grafico_comissoes_pendentes():
    # Comissões pendentes vs pagas (baseado no valor da comissão)
    pagas = db.session.query(func.sum(Venda.comissao)).filter(Venda.comissao_paga == True).scalar() or 0
    pendentes = db.session.query(func.sum(Venda.comissao)).filter(Venda.comissao_paga == False).scalar() or 0

    fig = px.pie(values=[float(pagas), float(pendentes)], names=['Pagas', 'Pendentes'], title='Valor das Comissões Pendentes vs Pagas')
    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
    return render_template('relatorios/grafico.html', graphJSON=graphJSON, titulo='Valor das Comissões Pendentes vs Pagas')
