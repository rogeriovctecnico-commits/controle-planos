from flask import render_template, redirect, url_for, flash, request, Blueprint
from . import operadoras_bp
from ...extensions import db
from ...models import Operadora
from ...forms import OperadoraForm
from sqlalchemy import or_

@operadoras_bp.route("/")
def list_operadoras():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("q", "")

    query = Operadora.query

    if search_term:
        search_term = search_term.strip()
        query = query.filter(Operadora.nome_operadora.ilike(f"%{search_term}%"))

    operadoras = query.order_by(Operadora.nome_operadora).paginate(page=page, per_page=10)
    return render_template("operadoras_list.html", operadoras=operadoras, search_term=search_term)

@operadoras_bp.route("/create", methods=["GET", "POST"])
def create_operadora():
    form = OperadoraForm()
    if form.validate_on_submit():
        op = Operadora(nome_operadora=form.nome_operadora.data) # type: ignore
        db.session.add(op)
        db.session.commit()
        flash("Operadora criada", "success")
        return redirect(url_for("operadoras.list_operadoras"))
    return render_template("operadoras_form.html", form=form, title="Nova Operadora")

@operadoras_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_operadora(id):
    op = Operadora.query.get_or_404(id)
    form = OperadoraForm(obj=op)
    if form.validate_on_submit():
        form.populate_obj(op)
        db.session.commit()
        flash("Operadora atualizada", "success")
        return redirect(url_for("operadoras.list_operadoras"))
    return render_template("operadoras_form.html", form=form, title="Editar Operadora")

@operadoras_bp.route("/<int:id>/delete", methods=["POST"])
def delete_operadora(id):
    op = Operadora.query.get_or_404(id)

    # Verifica se há planos vendidos para esta operadora
    planos_com_vendas = []
    for plano in op.planos:
        # Verifica se o plano tem vendas associadas
        if plano.vendas:
            planos_com_vendas.append(plano.nome_plano)

    if planos_com_vendas:
        flash(f"Não é possível excluir a operadora '{op.nome_operadora}' pois existem vendas associadas aos seguintes planos: {', '.join(planos_com_vendas)}", "danger")
        return redirect(url_for("operadoras.list_operadoras"))

    db.session.delete(op)
    db.session.commit()
    flash("Operadora removida", "warning")
    return redirect(url_for("operadoras.list_operadoras"))
