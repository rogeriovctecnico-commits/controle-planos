# app/blueprints/clientes/routes.py
from flask import render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Cliente
from app.forms import ClienteForm
from datetime import datetime
from sqlalchemy import extract
from . import clientes_bp  # Importar o blueprint

@clientes_bp.route('/')
@clientes_bp.route('/list')
def list_clientes():
    """Lista todos os clientes com filtros opcionais"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Filtros
    nome_filter = request.args.get('nome', '')
    email_filter = request.args.get('email', '')
    status_filter = request.args.get('status', '')
    
    # Query base
    query = Cliente.query
    
    # Aplicar filtros
    if nome_filter:
        query = query.filter(Cliente.nome.ilike(f'%{nome_filter}%'))
    if email_filter:
        query = query.filter(Cliente.email.ilike(f'%{email_filter}%'))
    if status_filter:
        query = query.filter(Cliente.status == status_filter)
    
    # Paginação
    clientes = query.order_by(Cliente.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template(
        'clientes_list.html',
        title='Gestão de Clientes',
        clientes=clientes,
        nome_filter=nome_filter,
        email_filter=email_filter,
        status_filter=status_filter
    )

@clientes_bp.route('/novo', methods=['GET', 'POST'])
def add_cliente():
    """Adicionar novo cliente"""
    form = ClienteForm()
    
    if form.validate_on_submit():
        try:
            cliente = Cliente(
                nome=form.nome.data,
                cpf=form.cpf.data,
                email=form.email.data,
                telefone=form.telefone.data,
                endereco=form.endereco.data,
                data_nascimento=form.data_nascimento.data,
                cnpj=form.cnpj.data,
                responsavel=form.responsavel.data,
                status=form.status.data
            )
            
            db.session.add(cliente)
            db.session.commit()
            
            flash('Cliente cadastrado com sucesso!', 'success')
            return redirect(url_for('clientes.list_clientes'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar cliente: {str(e)}', 'error')
    
    return render_template(
        'clientes_form.html',
        title='Novo Cliente',
        form=form,
        action='Cadastrar'
    )

@clientes_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def edit_cliente(id):
    """Editar cliente existente"""
    cliente = Cliente.query.get_or_404(id)
    
    form = ClienteForm(
        obj=cliente,
        original_cpf=cliente.cpf,
        original_email=cliente.email
    )
    
    if form.validate_on_submit():
        try:
            cliente.nome = form.nome.data
            cliente.cpf = form.cpf.data
            cliente.email = form.email.data
            cliente.telefone = form.telefone.data
            cliente.endereco = form.endereco.data
            cliente.data_nascimento = form.data_nascimento.data
            cliente.cnpj = form.cnpj.data
            cliente.responsavel = form.responsavel.data
            cliente.status = form.status.data
            
            db.session.commit()
            
            flash('Cliente atualizado com sucesso!', 'success')
            return redirect(url_for('clientes.list_clientes'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar cliente: {str(e)}', 'error')
    
    return render_template(
        'clientes_form.html',
        title='Editar Cliente',
        form=form,
        cliente=cliente,
        action='Atualizar'
    )

@clientes_bp.route('/<int:id>/deletar', methods=['POST'])
def delete_cliente(id):
    """Deletar cliente"""
    cliente = Cliente.query.get_or_404(id)
    
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir cliente: {str(e)}', 'error')
    
    return redirect(url_for('clientes.list_clientes'))

@clientes_bp.route('/<int:id>')
def view_cliente(id):
    """Visualizar detalhes do cliente"""
    cliente = Cliente.query.get_or_404(id)
    return render_template(
        'clientes_view.html',
        title=f'Cliente: {cliente.nome}',
        cliente=cliente
    )

# APIs para AJAX
@clientes_bp.route('/api/clientes')
def api_clientes():
    """API para buscar clientes"""
    nome = request.args.get('nome', '')
    email = request.args.get('email', '')
    status = request.args.get('status', '')
    
    query = Cliente.query
    
    if nome:
        query = query.filter(Cliente.nome.ilike(f'%{nome}%'))
    if email:
        query = query.filter(Cliente.email.ilike(f'%{email}%'))
    if status:
        query = query.filter(Cliente.status == status)
    
    clientes = query.order_by(Cliente.id.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': c.id,
            'nome': c.nome,
            'email': c.email,
            'telefone': c.telefone,
            'cpf': c.cpf,
            'status': c.status,
            'data_nascimento': c.data_nascimento.strftime('%d/%m/%Y') if c.data_nascimento else None
        } for c in clientes],
        'total': len(clientes)
    })

@clientes_bp.route('/api/aniversariantes')
def api_aniversariantes():
    """API para buscar aniversariantes do mês"""
    mes_atual = datetime.now().month
    
    aniversariantes = Cliente.query.filter(
        extract('month', Cliente.data_nascimento) == mes_atual,
        Cliente.status == 'ativo'
    ).order_by(extract('day', Cliente.data_nascimento)).all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': c.id,
            'nome': c.nome,
            'email': c.email,
            'data_nascimento': c.data_nascimento.strftime('%d/%m/%Y') if c.data_nascimento else None
        } for c in aniversariantes]
    })