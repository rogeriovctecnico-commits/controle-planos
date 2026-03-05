from flask import render_template, request, redirect, url_for, flash
from ...models import Venda, Cliente, Plano
from ...extensions import db
from ...forms import VendaForm
from . import vendas_bp
from sqlalchemy import or_

# Lista todas as vendas
@vendas_bp.route("/")
def list_vendas():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("q", "")
    sort_by = request.args.get("sort_by", "created_at")
    sort_order = request.args.get("sort_order", "desc")

    query = Venda.query.join(Cliente).join(Plano)

    if search_term:
        search_term = search_term.strip()
        query = query.filter(or_(
            Cliente.nome.ilike(f"%{search_term}%"),
            Plano.nome_plano.ilike(f"%{search_term}%")
        ))

    # Define sorting
    if sort_by == "id":
        order_column = Venda.id
    elif sort_by == "cliente":
        order_column = Cliente.nome
    elif sort_by == "numero_contrato":
        order_column = Venda.id  # Assuming numero_contrato is not a field, sort by id
    elif sort_by == "data_venda":
        order_column = Venda.data_venda
    elif sort_by == "vigencia":
        order_column = Venda.data_vigencia
    elif sort_by == "valor":
        order_column = Venda.valor_final
    elif sort_by == "status":
        order_column = Venda.status
    else:
        order_column = Venda.created_at

    if sort_order == "asc":
        query = query.order_by(order_column.asc())
    else:
        query = query.order_by(order_column.desc())

    vendas = query.paginate(page=page, per_page=10)

    def next_sort_order(col):
        if sort_by == col:
            return 'desc' if sort_order == 'asc' else 'asc'
        return 'asc'

    def sort_icon(col):
        if sort_by == col:
            return '↑' if sort_order == 'asc' else '↓'
        return ''

    return render_template("vendas_list.html", vendas=vendas, q=search_term, sort_by=sort_by, sort_order=sort_order, next_sort_order=next_sort_order, sort_icon=sort_icon, page=vendas.page, pages=vendas.pages)

# Cria nova venda
@vendas_bp.route("/create", methods=["GET", "POST"])
def create_venda():
    form = VendaForm()

    if request.method == "POST":
        # Pré-processa campos decimais para formato brasileiro
        decimal_fields = ['valor_venda', 'desconto', 'valor_final', 'comissao', 'premiacao']
        for field_name in decimal_fields:
            if field_name in request.form and request.form[field_name]:
                value = request.form[field_name]
                if isinstance(value, str) and ',' in value:
                    # Converte formato brasileiro para americano
                    form[field_name].data = float(value.replace('.', '').replace(',', '.'))

    if form.validate_on_submit():
        venda = Venda() # type: ignore
        form.populate_obj(venda)
        # Calcula valor_final se não estiver definido
        if venda.valor_final is None and venda.valor_venda is not None:
            venda.valor_final = venda.valor_venda - (venda.desconto or 0)
        db.session.add(venda)
        db.session.commit()
        flash("Venda registrada com sucesso!", "success")
        return redirect(url_for("vendas.list_vendas"))
    if form.errors:
        flash("Erro ao salvar venda. Verifique os campos obrigatórios destacados em vermelho.", "danger")
    return render_template("vendas_form.html", form=form, title="Nova Venda")

# Edita venda existente
@vendas_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_venda(id):
    venda = Venda.query.get_or_404(id)
    form = VendaForm(obj=venda)

    if request.method == "POST":
        # Pré-processa campos decimais para formato brasileiro
        decimal_fields = ['valor_venda', 'desconto', 'valor_final', 'comissao', 'premiacao']
        for field_name in decimal_fields:
            if field_name in request.form and request.form[field_name]:
                value = request.form[field_name]
                if isinstance(value, str) and ',' in value:
                    # Converte formato brasileiro para americano
                    form[field_name].data = float(value.replace('.', '').replace(',', '.'))

    if form.validate_on_submit():
        form.populate_obj(venda)
        # Calcula valor_final se não estiver definido
        if venda.valor_final is None and venda.valor_venda is not None:
            venda.valor_final = venda.valor_venda - (venda.desconto or 0)
        db.session.commit()
        flash("Venda atualizada com sucesso!", "success")
        return redirect(url_for("vendas.list_vendas"))
    if form.errors:
        flash("Erro ao atualizar venda. Verifique os campos obrigatórios destacados em vermelho.", "danger")
    return render_template("vendas_form.html", form=form, title="Editar Venda")

# Detalhes da venda
@vendas_bp.route("/<int:id>")
def detail_venda(id):
    venda = Venda.query.get_or_404(id)
    return render_template("vendas_detail.html", venda=venda)

# Exclui venda
@vendas_bp.route("/<int:id>/delete", methods=["POST"])
def delete_venda(id):
    venda = Venda.query.get_or_404(id)
    db.session.delete(venda)
    db.session.commit()
    flash("Venda excluída com sucesso!", "info")
    return redirect(url_for("vendas.list_vendas"))