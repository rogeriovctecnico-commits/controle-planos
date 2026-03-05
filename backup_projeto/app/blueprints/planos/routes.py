from flask import render_template, redirect, url_for, flash, request, Blueprint
from . import planos_bp
from ...extensions import db
from ...models import Plano, Operadora
from ...forms import PlanoForm
from sqlalchemy import or_

@planos_bp.route("/")
def list_planos():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("q", "")

    query = Plano.query

    if search_term:
        search_term = search_term.strip()
        query = query.filter(or_(
            Plano.nome_plano.ilike(f"%{search_term}%"),
            Plano.descricao.ilike(f"%{search_term}%")
        ))

    planos = query.order_by(Plano.nome_plano).paginate(page=page, per_page=10)
    return render_template("planos_list.html", planos=planos, search_term=search_term)

@planos_bp.route("/create", methods=["GET", "POST"])
def create_plano():
    form = PlanoForm()
    form.operadora_id.choices = [(o.id, o.nome_operadora) for o in Operadora.query.order_by(Operadora.nome_operadora).all()]
    if form.validate_on_submit():
        plano = Plano()
        plano.nome_plano=form.nome_plano.data
        plano.descricao=form.descricao.data
        plano.valor_base=form.valor_base.data
        plano.cobertura=form.cobertura.data
        plano.tipo_plano=form.tipo_plano.data
        plano.ativo=form.ativo.data
        plano.operadora_id=form.operadora_id.data
        plano.regiao=form.regiao.data
        plano.acomodacao=form.acomodacao.data
        plano.beneficios=form.beneficios.data
        plano.data_vigencia=form.data_vigencia.data
        plano.created_by_username=form.created_by_username.data
        
        db.session.add(plano)
        db.session.commit()
        flash("Plano criado com sucesso", "success")
        return redirect(url_for("planos.list_planos"))
    return render_template("planos_form.html", form=form, title="Novo Plano")

@planos_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_plano(id):
    plano = Plano.query.get_or_404(id)
    if request.method == 'POST':
        form = PlanoForm(original_nome_plano=plano.nome_plano)
    else:
        form = PlanoForm(obj=plano, original_nome_plano=plano.nome_plano)
    form.operadora_id.choices = [(o.id, o.nome_operadora) for o in Operadora.query.order_by(Operadora.nome_operadora).all()]
    if form.validate_on_submit():
        form.populate_obj(plano)
        db.session.commit()
        flash("Plano atualizado", "success")
        return redirect(url_for("planos.list_planos"))
    return render_template("planos_form.html", form=form, title="Editar Plano")

@planos_bp.route("/<int:id>/delete", methods=["POST"])
def delete_plano(id):
    plano = Plano.query.get_or_404(id)
    db.session.delete(plano)
    db.session.commit()
    flash("Plano removido", "warning")
    return redirect(url_for("planos.list_planos"))

@planos_bp.route("/<int:id>")
def detail_plano(id):
    plano = Plano.query.get_or_404(id)
    return render_template("planos_detail.html", plano=plano)
